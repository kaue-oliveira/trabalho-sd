import httpx
import os
import asyncio

client = httpx.AsyncClient(timeout=None)

GATEWAY_URL = os.getenv("GATEWAY_URL", "http://api-gateway:3000")

# --------- CLIMA / PREÇO EM PARALELO ---------

async def get_climate_async(payload: dict) -> dict:
    """Busca dados climáticos via Gateway"""
    if payload.get("clima"):
        return payload["clima"]
    if not GATEWAY_URL:
        return {}
    
    params = {
        "localidade": payload.get("localidade"),
        "data_colheita": payload.get("data_colheita")
    }
    r = await client.get(f"{GATEWAY_URL}/climate", params=params)
    r.raise_for_status()
    return r.json()

async def get_price_async(payload: dict) -> dict:
    """Busca dados de preço via Gateway"""
    if payload.get("preco"):
        return payload["preco"]
    if not GATEWAY_URL:
        return {}
    
    params = {"tipo_grao": payload.get("tipo_grao", "arabica")}
    r = await client.get(f"{GATEWAY_URL}/price", params=params)
    r.raise_for_status()
    return r.json()

# --------- RAG ---------

async def rag_search_async(query: str, k: int = 4):
    """Busca semântica em relatórios técnicos"""
    r = await client.post(f"{GATEWAY_URL}/rag/search", json={"query": query, "k": k})
    r.raise_for_status()
    return r.json().get("results", [])

# --------- OLLAMA ---------

async def solicitar_decisao_ollama_async(payload: dict):
    """Gera decisão via Ollama direto - sem service intermediário"""
    import time
    import json
    
    clima = payload.get("clima", {})
    preco = payload.get("preco", {})
    relatorios = payload.get("relatorios", [])
    localidade = payload.get("localidade", "")
    data_colheita = payload.get("data_colheita", "")

    prompt = f"""
        Você é um especialista em cafeicultura.
        Use os dados abaixo para recomendar: VENDER ou AGUARDAR.

        Localidade: {localidade}
        Data de colheita: {data_colheita}

        Clima:
        {clima}

        Preços:
        {preco}

        Relatórios técnicos:
        {relatorios}

        Responda APENAS um JSON válido:
        {{
        "decision": "vender / aguardar",
        "explanation": "máximo 200 palavras"
        }}
        """

    try:
        start = time.perf_counter()
        
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
            "decision": decision_data.get("decision", "aguardar").lower(),
            "explanation": decision_data.get("explanation", ""),
            "ollama_time_seconds": round(duration, 3)
        }

    except Exception as e:
        return {
            "decision": "aguardar",
            "explanation": f"Erro ao consultar modelo: {e}",
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
