import httpx
import os
import asyncio
import time
import json
from agronomic_agent import (
    analyze_climate_factors,
    analyze_price_trends, 
    analyze_market_reports,
    calculate_decision_score,
    build_ai_prompt
)

client = httpx.AsyncClient(timeout=None)

GATEWAY_URL = os.getenv("GATEWAY_URL", "http://gateway:3000")

# --------- CLIMA / PREÇO EM PARALELO ---------

async def get_climate_async(payload: dict) -> dict:
    """Busca dados climáticos via Gateway"""
    if payload.get("clima"):
        return payload["clima"]
    if not GATEWAY_URL:
        return {}
    
    cidade = payload.get("cidade", "")
    estado = payload.get("estado", "")
    
    if not cidade or not estado:
        return {}
    
    try:
        r = await client.get(
            f"{GATEWAY_URL}/climate/forecast",
            params={"cidade": cidade, "estado": estado}
        )
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"[ERROR] Falha ao buscar clima: {e}")
        return {}

async def get_price_async(payload: dict) -> dict:
    """Busca dados de preço via Gateway"""
    if payload.get("preco"):
        return payload["preco"]
    if not GATEWAY_URL:
        return {}
    
    tipo_cafe = payload.get("tipo_cafe", "arabica")
    
    try:
        r = await client.get(f"{GATEWAY_URL}/price/{tipo_cafe}")
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"[ERROR] Falha ao buscar preço: {e}")
        return {}

# --------- RAG ---------

async def rag_search_async(query: str, k: int = 4):
    """Busca semântica em relatórios técnicos"""
    r = await client.post(f"{GATEWAY_URL}/rag/search", json={"query": query, "k": k})
    r.raise_for_status()
    return r.json().get("results", [])

# --------- OLLAMA ---------

async def solicitar_decisao_ollama_async(payload: dict):   
    """
    Solicita explicação ao modelo Ollama para a decisão tomada pelo agente
    
    Este método:
    1. Analisa os dados usando as funções do agente agronômico
    2. Calcula scores para clima, preço e mercado
    3. Toma a decisão final
    4. Constrói prompt pedindo explicação
    5. Envia ao Ollama para gerar explicação detalhada
    
    """
    clima = payload.get("clima", {})
    preco = payload.get("preco", {})
    relatorios = payload.get("relatorios", [])
    
    # Análise quantitativa usando funções do agente agronômico
    climate_score = analyze_climate_factors(clima)
    price_score = analyze_price_trends(preco)
    market_score = analyze_market_reports(relatorios)
    
    # Calcula score final e toma a decisão final
    decision_score = calculate_decision_score(climate_score, price_score, market_score)
    decision_final = "vender" if decision_score >= 0.6 else "aguardar"
    
    # Log das análises
    print(f"[ANÁLISE] Climate Score: {climate_score:.3f}, Price Score: {price_score:.3f}, Market Score: {market_score:.3f}")
    print(f"[DECISÃO] Score: {decision_score:.3f} -> {decision_final.upper()} (limiar: 0.6)")
    
    # Constrói prompt usando a função do agente agronômico
    prompt = build_ai_prompt(
        payload, clima, preco, relatorios,
        climate_score, price_score, market_score,
        decision_score, decision_final
    )

    try:
        start = time.perf_counter()
        
        # Log dos dados climáticos que estão sendo enviados ao Ollama
        print(f"[CLIMA] Dados climáticos enviados ao Ollama: {clima}")
        print(f"[PREÇO] Dados de preço enviados ao Ollama: {preco}")
        print(f"[OLLAMA] Solicitando explicação para decisão: {decision_final.upper()}")
        
        r = await client.post(
            f"{GATEWAY_URL}/ollama/generate",
            json={
                "model": "phi3:mini",
                "prompt": prompt,
                "stream": False,
                "format": "json"
            }
        )
        duration = time.perf_counter() - start
        r.raise_for_status()

        raw = r.json().get("response", "")
        ollama_response = json.loads(raw)
        explicacao = ollama_response.get("explicacao", "")
        
        return {
            "decisao": decision_final,  # SEMPRE a decisão do agente
            "explicacao": explicacao if explicacao else f"Decisão de {decision_final} baseada em análise quantitativa (score: {decision_score:.3f})",
            "ollama_time_seconds": round(duration, 3),
            "decision_score": decision_score,
            "climate_score": climate_score,
            "price_score": price_score,
            "market_score": market_score
        }

    except Exception as e:
        print(f"[ERROR] Erro ao consultar Ollama: {e}")
        # Mesmo com erro, retorna a decisão do agente com explicação padrão
        return {
            "decisao": decision_final,  # SEMPRE a decisão do agente
            "explicacao": f"Decisão de {decision_final} baseada em análise quantitativa. Score final: {decision_score:.3f} (clima: {climate_score:.3f}, preço: {price_score:.3f}, mercado: {market_score:.3f}). Limiar para venda: 0.5",
            "ollama_time_seconds": None,
            "decision_score": decision_score,
            "climate_score": climate_score,
            "price_score": price_score,
            "market_score": market_score
        }

# --------- BUSCA EM PARALELO ---------
async def fetch_all_parallel(payload: dict, rag_query: str) -> tuple[dict, dict, list]:
    """
    Busca clima, preço e RAG em paralelo usando asyncio.gather
    Retorna: (clima, preco, relatorios)
    """
    async def safe_get_climate():
        try:
            return await get_climate_async(payload)
        except Exception:
            return {}
    
    async def safe_get_price():
        try:
            return await get_price_async(payload)
        except Exception:
            return {}
    
    async def safe_get_rag():
        try:
            return await rag_search_async(rag_query, k=4)
        except Exception:
            return []
    
    clima, preco, rels = await asyncio.gather(
        safe_get_climate(),
        safe_get_price(),
        safe_get_rag()
    )
    
    return clima, preco, rels
