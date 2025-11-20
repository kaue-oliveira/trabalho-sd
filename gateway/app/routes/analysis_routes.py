from fastapi import APIRouter, Depends, HTTPException
import httpx
from app.clients.data_client import get_data_service_client
from app.utils.jwt_utils import verify_token


# =====================================================
# ROTAS DE ANÁLISES
# =====================================================
router = APIRouter(prefix="/analises", tags=["analises"])


@router.get("")
async def listar_analises(payload: dict = Depends(verify_token), data_client: httpx.AsyncClient = Depends(get_data_service_client)):
    user_id = int(payload.get("sub"))
    try:
        resp = await data_client.get(f"/analises/usuario/{user_id}")
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Data Service não disponível: {str(e)}")


@router.post("")
async def criar_analise(analise_data: dict, payload: dict = Depends(verify_token), data_client: httpx.AsyncClient = Depends(get_data_service_client)):
    user_id = int(payload.get("sub"))
    analise_payload = { **analise_data, "usuario_id": user_id }
    try:
        resp = await data_client.post("/analises", json=analise_payload)
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Data Service não disponível: {str(e)}")
