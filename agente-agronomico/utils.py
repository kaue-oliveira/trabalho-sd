import httpx
import os
import asyncio

# Cliente assíncrono compartilhado com timeout padrão de 210s
client = httpx.AsyncClient(timeout=210)

GATEWAY_URL = os.getenv("GATEWAY_URL", "http://gateway:3000")
RAG_URL = os.getenv("RAG_URL", "http://rag_service:8002")
OLLAMA_SERVICE_URL = os.getenv("OLLAMA_SERVICE_URL", "http://ollama_service:8004/generate")

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
    """Gera decisão via Ollama service"""
    r = await client.post(OLLAMA_SERVICE_URL, json=payload)
    r.raise_for_status()
    return r.json()

# --------- 🚀 PARALELIZAÇÃO: Buscar tudo em paralelo ---------

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
    
    # Executar todas as 3 requisições em paralelo
    clima, preco, rels = await asyncio.gather(
        safe_get_climate(),
        safe_get_price(),
        safe_get_rag()
    )
    
    return clima, preco, rels
