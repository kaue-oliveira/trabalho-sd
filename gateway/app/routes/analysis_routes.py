from fastapi import APIRouter, Depends, HTTPException
import httpx
from app.clients.data_client import get_data_service_client
from app.utils.jwt_utils import verify_token
from datetime import date
from pydantic import BaseModel


# =====================================================
# SCHEMAS DE ANÁLISES
# =====================================================
class AnalysisCreateRequest(BaseModel):
    tipo_cafe: str
    data_colheita: date
    quantidade: float
    cidade: str
    estado: str
    estado_cafe: str
    data_analise: date
    decisao: str
    explicacao_decisao: str

    class Config:
        schema_extra = {
            "example": {
                "tipo_cafe": "Arábica",
                "data_colheita": "2024-05-20",
                "quantidade": 2500.75,
                "cidade": "Carmo de Minas",
                "estado": "MG",
                "estado_cafe": "verde",
                "data_analise": "2024-05-25",
                "decisao": "VENDER",
                "explicacao_decisao": "Qualidade excelente, preço favorável no mercado"
            }
        }


class AnalysisResponse(BaseModel):
    id: int
    tipo_cafe: str
    data_colheita: str
    quantidade: float
    cidade: str
    estado: str
    estado_cafe: str
    data_analise: str
    decisao: str
    explicacao_decisao: str
    usuario_id: int

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "tipo_cafe": "Arábica",
                "data_colheita": "2024-05-20",
                "quantidade": 2500.75,
                "cidade": "Carmo de Minas",
                "estado": "MG",
                "estado_cafe": "verde",
                "data_analise": "2024-05-25",
                "decisao": "VENDER",
                "explicacao_decisao": "Qualidade excelente, preço favorável no mercado",
                "usuario_id": 1
            }
        }


# =====================================================
# ROTAS DE ANÁLISES
# =====================================================
router = APIRouter(prefix="/analises", tags=["analises"])


@router.get("")
async def listar_analises(payload: dict = Depends(verify_token), data_client: httpx.AsyncClient = Depends(get_data_service_client)):
    """
    Lista todas as análises do usuário autenticado.
    
    Retorna um histórico completo das análises realizadas
    pelo usuário atual, ordenadas por data de análise.
    """
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
    """
    Cria uma nova análise de café para o usuário autenticado.

    - **tipo_cafe**: Tipo do café (Arábica, Robusta, etc.)
    - **data_colheita**: Data da colheita (YYYY-MM-DD)
    - **quantidade**: Quantidade em kg
    - **cidade**: Cidade de origem
    - **estado**: Estado de origem (sigla)
    - **estado_cafe**: Estado do café (verde, seco, etc.)
    - **data_analise**: Data da análise (YYYY-MM-DD)
    - **decisao**: Decisão tomada (VENDER, ARMAZENAR, etc.)
    - **explicacao_decisao**: Explicação detalhada da decisão
    
    Retorna os dados da análise criada com ID gerado.
    """
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
