from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
import httpx
import time
from app.clients.ollama_client import get_ollama_client
from app.utils.jwt_utils import verify_token


# =====================================================
# ROTAS PARA O OLLAMA
# =====================================================
router = APIRouter(prefix="/ollama", tags=["ollama"])


@router.post("/generate")
async def proxy_ollama_generate(request: Request, ollama_client: httpx.AsyncClient = Depends(get_ollama_client)):
    """
    Proxy para geração de texto usando modelos Ollama.
    
    Retorna resposta gerada pelo modelo com métricas de tempo
    incluindo duração do proxy no gateway.
    
    Usado pelos agentes para processamento de linguagem natural.
    """
    body = await request.json()
    try:
        start = time.perf_counter()
        response = await ollama_client.post("/api/generate", json=body)
        response.raise_for_status()

        duration = time.perf_counter() - start

        resp_json = response.json()
        if isinstance(resp_json, dict):
            resp_json.setdefault("timings", {})
            resp_json["timings"]["gateway_proxy_seconds"] = round(duration, 3)

        return JSONResponse(content=resp_json, headers={"X-Proxy-Duration": f"{duration:.3f}"})

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Ollama não disponível: {str(e)}")
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Ollama timeout")


@router.post("/api/embeddings")
async def proxy_ollama_embeddings(request: Request, ollama_client: httpx.AsyncClient = Depends(get_ollama_client)):
    """
    Proxy para geração de embeddings usando modelos Ollama.
    
    Retorna vetor de embeddings para o texto fornecido.
    
    Usado pelo RAG service para busca semântica e similaridade.
    """
    body = await request.json()

    try:
        response = await ollama_client.post("/api/embeddings", json=body)
        response.raise_for_status()
        return JSONResponse(content=response.json())
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Ollama não disponível: {str(e)}")
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Ollama embeddings timeout")
