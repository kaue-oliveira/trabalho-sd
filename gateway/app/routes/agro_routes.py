from fastapi import APIRouter, Depends, HTTPException, status
import httpx
from app.clients.agro_client import get_agro_agent_client
from app.utils.jwt_utils import verify_token
from pydantic import BaseModel


# =====================================================
# SCHEMAS DO AGENTE AGRONÔMICO
# =====================================================
class AgroAnalysisRequest(BaseModel):
    tipo_cafe: str
    data_colheita: str
    quantidade: float
    cidade: str
    estado: str
    estado_cafe: str

    class Config:
        schema_extra = {
            "example": {
                "tipo_cafe": "arábica",
                "data_colheita": "2025-11-01",
                "quantidade": 12.5,
                "cidade": "Barueri",
                "estado": "SP",
                "estado_cafe": "verde"
            }
        }


class AgroAnalysisResponse(BaseModel):
    decisao: str
    explicacao_decisao: str

    class Config:
        schema_extra = {
            "example": {
                "decisao": "vender",
                "explicacao_decisao": "Qualidade alta; preço favorável no mercado atual."
            }
        }



# =====================================================
# ROTAS DO AGENTE AGRONÔMICO
# =====================================================
router = APIRouter(prefix="/agro", tags=["agro"])


@router.post("/recommend", response_model=AgroAnalysisResponse)
async def analyze_coffee(analysis_data: AgroAnalysisRequest, payload: dict = Depends(verify_token), agro_client: httpx.AsyncClient = Depends(get_agro_agent_client)):
    """
    Analisa um lote de café e retorna uma recomendação de venda/aguardar.

    - **tipo_cafe**: Tipo do café (ex: arábica, robusta)
    - **data_colheita**: Data da colheita no formato YYYY-MM-DD
    - **quantidade**: Quantidade em KG
    - **cidade**: Cidade de origem
    - **estado**: Estado de origem (sigla)
    - **estado_cafe**: Estado atual do café (verde, torrada, moído)
    
    Retorna decisão e explicação detalhada do agente agronômico.
    """
    try:
        response = await agro_client.post("/recommend", json=analysis_data.dict())
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Agro Agent não disponível: {str(e)}")