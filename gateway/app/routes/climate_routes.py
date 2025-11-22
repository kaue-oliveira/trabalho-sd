from fastapi import APIRouter, Depends, HTTPException
import httpx
from app.clients.climate_client import get_climate_agent_client
from app.utils.jwt_utils import verify_token
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import date


# =====================================================
# SCHEMAS DO AGENTE CLIMÁTICO
# =====================================================
class DailyForecast(BaseModel):
    date: date
    temperature_2m_max: float
    temperature_2m_min: float
    precipitation_sum: float
    precipitation_hours: Optional[float]
    windspeed_10m_max: float
    winddirection_10m_dominant: Optional[float]
    weathercode: int

    class Config:
        schema_extra = {
            "example": {
                "date": "2024-01-15",
                "temperature_2m_max": 28.5,
                "temperature_2m_min": 18.2,
                "precipitation_sum": 5.2,
                "precipitation_hours": 3.0,
                "windspeed_10m_max": 15.8,
                "winddirection_10m_dominant": 180.0,
                "weathercode": 61
            }
        }


class MonthlyAverage(BaseModel):
    temperature_max_avg: float
    temperature_min_avg: float
    precipitation_avg: float
    windspeed_max_avg: float

    class Config:
        schema_extra = {
            "example": {
                "temperature_max_avg": 26.8,
                "temperature_min_avg": 16.5,
                "precipitation_avg": 8.3,
                "windspeed_max_avg": 12.1
            }
        }


class ClimateResponse(BaseModel):
    location: str
    latitude: float
    longitude: float
    timezone: str
    elevation: float
    daily_forecast: List[DailyForecast]
    past_month_averages: Dict[str, MonthlyAverage]
    generated_time: str

    class Config:
        schema_extra = {
            "example": {
                "location": "Lavras, MG",
                "latitude": -21.248,
                "longitude": -45.001,
                "timezone": "America/Sao_Paulo",
                "elevation": 919.0,
                "generated_time": "2024-01-15T10:30:00Z",
                "daily_forecast": [
                    {
                        "date": "2024-01-15",
                        "temperature_2m_max": 28.5,
                        "temperature_2m_min": 18.2,
                        "precipitation_sum": 5.2,
                        "precipitation_hours": 3.0,
                        "windspeed_10m_max": 15.8,
                        "winddirection_10m_dominant": 180.0,
                        "weathercode": 61
                    }
                ],
                "past_month_averages": {
                    "1_mes_atras": {
                        "temperature_max_avg": 26.8,
                        "temperature_min_avg": 16.5,
                        "precipitation_avg": 8.3,
                        "windspeed_max_avg": 12.1
                    },
                    "2_meses_atras": {
                        "temperature_max_avg": 25.2,
                        "temperature_min_avg": 15.8,
                        "precipitation_avg": 6.5,
                        "windspeed_max_avg": 11.3
                    },
                    "3_meses_atras": {
                        "temperature_max_avg": 23.9,
                        "temperature_min_avg": 14.2,
                        "precipitation_avg": 4.8,
                        "windspeed_max_avg": 10.7
                    }
                }
            }
        }


# =====================================================
# ROTAS DO AGENTE CLIMÁTICO
# =====================================================
router = APIRouter(prefix="/climate", tags=["climate"])


@router.get("/forecast")
async def get_climate_forecast(cidade: str, estado: str, client: httpx.AsyncClient = Depends(get_climate_agent_client)):
    """
    Obtém análise climática completa para uma localização específica.

    - **cidade**: Nome da cidade (ex: Lavras, Carmo de Minas, Varginha)
    - **estado**: Sigla do estado (ex: MG, SP, PR)
    
    **Funcionamento:**
    
    **1. Previsão Futura (14 dias):**
    - Temperaturas máxima e mínima diárias
    - Precipitação acumulada (mm)
    - Horas de precipitação
    - Velocidade máxima do vento
    - Direção predominante do vento
    - Código meteorológico (WMO)
    
    **2. Histórico Comparativo:**
    - Médias do mês atual há 1, 2 e 3 meses atrás
    - Temperaturas máximas e mínimas médias
    - Precipitação média
    - Velocidade do vento média
    
    **3. Metadados:**
    - Coordenadas geográficas precisas
    - Fuso horário local
    - Elevação do terreno
    
    **Ideal para:** Planejamento de colheita, irrigação e manejo do café \
    **Fonte:** OpenMeteo API com dados meteorológicos globais
    """
    try:
        location = f"{cidade},{estado}"
        response = await client.get(f"/climate/forecast/{location}")
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Climate Agent não disponível: {str(e)}")

