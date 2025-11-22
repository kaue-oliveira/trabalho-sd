from fastapi import APIRouter, Depends, HTTPException
import httpx
from app.clients.price_client import get_price_agent_client
from app.utils.jwt_utils import verify_token


# =====================================================
# ROTAS DO AGENTE DE PREÇO
# =====================================================
router = APIRouter(prefix="/price", tags=["price"])


@router.get("/{tipo_cafe}")
async def get_coffee_price(tipo_cafe: str, price_client: httpx.AsyncClient = Depends(get_price_agent_client)):
    """
    Obtém análise histórica de preços de um tipo específico de café.

    - **tipo_cafe**: Tipo do café (arábica, robusta)
    
    **Funcionamento:**
    - Analisa os últimos 90 dias de dados de preço
    - Calcula 30 médias móveis, cada uma representando 3 dias
    
    **Retorno:**
    - 30 pontos de dados, cada um com média de 3 dias
    
    **Tipos suportados:** arábica, robusta
    """
    try:
        response = await price_client.get(f"/preco/{tipo_cafe}")
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        if e.response.status_code in [400, 404]:
            detail = e.response.json().get("detail", "Erro no price agent")
            raise HTTPException(status_code=e.response.status_code, detail=detail)
        raise HTTPException(status_code=e.response.status_code, detail=f"Erro no price agent: {e.response.text}")
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Price Agent não disponível: {str(e)}")