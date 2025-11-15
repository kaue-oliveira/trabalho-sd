import httpx
from fastapi import HTTPException

# Conectar DIRETAMENTE ao Data Service
DATA_SERVICE_URL = "http://localhost:8001"

async def salvar_preco(tipo_cafe: str, preco_info: dict):
    """
    Envia o preço obtido via scraping DIRETAMENTE para o Data Service
    """
    # Converter formato do scraper para formato do Data Service
    payload = {
        "price_date": preco_info["data"],
        "price": float(preco_info["preco"])
    }
    
    endpoint = f"/precos/{tipo_cafe}/"

    async with httpx.AsyncClient(timeout=20.0) as client:
        try:
            response = await client.post(DATA_SERVICE_URL + endpoint, json=payload)
            if response.status_code != 200:
                raise HTTPException(response.status_code, response.text)
            return response.json()
        except Exception as e:
            raise HTTPException(500, f"Erro ao conectar com Data Service: {str(e)}")

async def buscar_historico(tipo_cafe: str):
    """
    Recupera DIRETAMENTE do Data Service 90 dias de preços do tipo solicitado
    """
    endpoint = f"/precos/{tipo_cafe}/"

    async with httpx.AsyncClient(timeout=20.0) as client:
        try:
            response = await client.get(DATA_SERVICE_URL + endpoint)
            if response.status_code != 200:
                raise HTTPException(response.status_code, response.text)

            # O Data Service retorna todos os registros
            historico = response.json()
            # Ordenar por data decrescente
            historico.sort(key=lambda x: x.get('price_date', ''), reverse=True)
            # Pegar os 90 mais recentes
            return historico[:90]
        except Exception as e:
            raise HTTPException(500, f"Erro ao buscar histórico: {str(e)}")