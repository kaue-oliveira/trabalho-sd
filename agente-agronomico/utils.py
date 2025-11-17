import httpx
import os
import asyncio
import time
import json

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
    clima = payload.get("clima", {})
    preco = payload.get("preco", {})
    relatorios = payload.get("relatorios", [])
    
    tipo_cafe = payload.get("tipo_cafe", "")
    cidade = payload.get("cidade", "")
    estado = payload.get("estado", "")
    data_colheita = payload.get("data_colheita", "")
    quantidade = payload.get("quantidade", 0)
    estado_cafe = payload.get("estado_cafe", "")

    prompt = f"""
        Você é um especialista em cafeicultura e comercialização de café.
        Use os dados abaixo para recomendar: VENDER ou AGUARDAR.

        Informações da produção:
        - Tipo de café: {tipo_cafe}
        - Cidade: {cidade}
        - Estado: {estado}
        - Data de colheita: {data_colheita}
        - Quantidade: {quantidade} sacas
        - Estado do café: {estado_cafe}

        Dados climáticos:
        {clima}

        Preços de mercado:
        {preco}

        Relatórios técnicos consultados:
        {relatorios}

        Baseado nestas informações, forneça uma recomendação fundamentada.

        Responda APENAS um JSON válido no formato:
        {{
        "decisao": "vender" ou "aguardar",
        "explicacao": "justificativa detalhada da recomendação em português (máximo 200 palavras)"
        }}
        """

    try:
        start = time.perf_counter()
        
        # Log dos dados climáticos que estão sendo enviados ao Ollama
        print(f"[CLIMA] Dados climáticos enviados ao Ollama: {clima}")
        print(f"[PREÇO] Dados de preço enviados ao Ollama: {preco}")
        
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
        decision_data = json.loads(raw)

        return {
            "decisao": decision_data.get("decisao", "aguardar").lower(),
            "explicacao": decision_data.get("explicacao", ""),
            "ollama_time_seconds": round(duration, 3)
        }

    except Exception as e:
        print(f"[ERROR] Erro ao consultar Ollama: {e}")
        return {
            "decisao": "aguardar",
            "explicacao": f"Erro ao consultar modelo: {e}",
            "ollama_time_seconds": None
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
