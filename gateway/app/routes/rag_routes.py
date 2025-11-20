from fastapi import APIRouter, Depends, HTTPException
import httpx
from app.clients.rag_client import get_rag_service_client
from app.utils.jwt_utils import verify_token


# =====================================================
# **ROTAS PARA O RAG SERVICE**
# =====================================================
router = APIRouter(prefix="/rag", tags=["rag"])


@router.post("/search")
async def rag_search_proxy(request: dict, rag_client: httpx.AsyncClient = Depends(get_rag_service_client)):
    """
    Proxy para o RAG service - busca semântica em documentos
    Sem autenticação pois é usado internamente pelos agentes
    """
    try:
        response = await rag_client.post("/rag/search", json=request)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"RAG Service não disponível: {str(e)}")