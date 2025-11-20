from fastapi import APIRouter, Depends, HTTPException
import httpx
from app.clients.data_client import get_data_service_client
from app.utils.jwt_utils import verify_token

# =====================================================
# ROTAS DE USUÁRIOS
# =====================================================
router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@router.get("")
async def listar_usuarios(data_client: httpx.AsyncClient = Depends(get_data_service_client)):
    try:
        resp = await data_client.get("/usuarios")
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Data Service não disponível: {str(e)}")
    
    
@router.post("")
async def criar_usuario(user_data: dict, data_client: httpx.AsyncClient = Depends(get_data_service_client)):
    try:
        resp = await data_client.post("/usuarios", json=user_data)
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Data Service não disponível: {str(e)}")


@router.put("/me")
async def atualizar_usuario(user_data: dict, token_payload: dict = Depends(verify_token), data_client: httpx.AsyncClient = Depends(get_data_service_client)):
    user_id = int(token_payload.get("sub"))
    try:
        resp = await data_client.put(f"/usuarios/{user_id}", json=user_data)
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Data Service não disponível: {str(e)}")


@router.delete("/me")
async def deletar_usuario(token_payload: dict = Depends(verify_token), data_client: httpx.AsyncClient = Depends(get_data_service_client)):
    user_id = int(token_payload.get("sub"))
    try:
        resp = await data_client.delete(f"/usuarios/{user_id}")
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Data Service não disponível: {str(e)}")
