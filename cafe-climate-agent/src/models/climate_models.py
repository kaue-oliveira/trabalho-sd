from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict
from datetime import date
import unicodedata
import re

class DailyForecast(BaseModel):
    date: date
    temperature_2m_max: float
    temperature_2m_min: float
    precipitation_sum: float
    precipitation_hours: Optional[float] = None
    windspeed_10m_max: float
    winddirection_10m_dominant: Optional[float] = None
    weathercode: int


class ClimateResponse(BaseModel):
    location: str
    latitude: float
    longitude: float
    timezone: str
    elevation: Optional[float] = None
    daily_forecast: List[DailyForecast]
    past_month_averages: Optional[Dict[str, Dict[str, float]]] = None
    generated_time: str


class LocationRequest(BaseModel):
    location: str = Field(..., min_length=1, max_length=100)

    @validator("location")
    def sanitize_location(cls, value: str):
        value = value.strip()
        value = unicodedata.normalize("NFKC", value)

        # Permite apenas letras, números, espaços, hífen, apóstrofo e vírgula
        if not re.match(r"^[\w\s\-\',\.À-ÖØ-öø-ÿ]+$", value, flags=re.UNICODE):
            raise ValueError(
                "Local inválido. Use apenas letras, números, espaços, hífen e vírgula."
            )

        return value
