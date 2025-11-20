from fastapi import APIRouter, Depends, HTTPException
import httpx
from app.clients.climate_client import get_climate_agent_client
from app.utils.jwt_utils import verify_token


# =====================================================
# ROTAS DO AGENTE CLIMÁTICO
# =====================================================
router = APIRouter(prefix="/climate", tags=["climate"])


@router.get("/forecast")
async def get_climate_forecast(cidade: str, estado: str, client: httpx.AsyncClient = Depends(get_climate_agent_client)):
    try:
        location = f"{cidade},{estado}"
        response = await client.get(f"/climate/forecast/{location}")
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Climate Agent não disponível: {str(e)}")

