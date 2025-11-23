from fastapi import APIRouter, Depends
from datetime import datetime, timezone
import httpx

from app.clients.climate_client import get_climate_agent_client
from app.clients.data_client import get_data_service_client
from app.clients.price_client import get_price_agent_client
from app.clients.agro_client import get_agro_agent_client
from app.clients.rag_client import get_rag_service_client
from app.clients.ollama_client import get_ollama_client


router = APIRouter(tags=["health"])


@router.get("/")
async def root():
    """
    Endpoint raiz do Gateway.
    
    Retorna status básico confirmando que o serviço está rodando.
    """
    return {
        "message": "CafeQuality Gateway está rodando!",
        "service": "gateway"
    }


@router.get("/health")
async def health_check():
    """
    Health check básico do gateway.
    
    Verifica apenas o status do próprio serviço Gateway.
    Retorna status e timestamp atual.
    """
    return {
        "status": "healthy",
        "service": "gateway",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@router.get("/health/full")
async def full_health_check(
    climate_client: httpx.AsyncClient = Depends(get_climate_agent_client),
    data_client: httpx.AsyncClient = Depends(get_data_service_client),
    price_client: httpx.AsyncClient = Depends(get_price_agent_client),
    agro_client: httpx.AsyncClient = Depends(get_agro_agent_client),
    rag_client: httpx.AsyncClient = Depends(get_rag_service_client),
    ollama_client: httpx.AsyncClient = Depends(get_ollama_client)
):
    """
    Health check completo verificando todos os serviços dependentes.
    
    Verifica a conectividade com:
    - Data Service
    - Climate Agent
    - Price Agent  
    - Agro Agent
    - RAG Service
    - Ollama
    
    Retorna status detalhado de cada serviço.
    """

    def check(response):
        return "healthy" if response == 200 else "unhealthy"

    try:
        climate_status = check((await climate_client.get("/health")).status_code)
    except Exception:
        climate_status = "unreachable"

    try:
        data_status = check((await data_client.get("/health")).status_code)
    except Exception:
        data_status = "unreachable"

    try:
        price_status = check((await price_client.get("/health")).status_code)
    except Exception:
        price_status = "unreachable"

    try:
        agro_status = check((await agro_client.get("/health")).status_code)
    except Exception:
        agro_status = "unreachable"

    try:
        rag_status = check((await rag_client.get("/health")).status_code)
    except Exception:
        rag_status = "unreachable"

    try:
        ollama_status = check((await ollama_client.get("/api/tags")).status_code)
    except Exception:
        ollama_status = "unreachable"

    return {
        "gateway": "healthy",
        "data_service": data_status,
        "climate_agent": climate_status,
        "price_agent": price_status,
        "agro_agent": agro_status,
        "rag_service": rag_status,
        "ollama": ollama_status,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
