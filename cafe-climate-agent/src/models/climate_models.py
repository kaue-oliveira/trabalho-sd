from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class DailyForecast(BaseModel):
    date: date
    temperature_2m_max: float
    temperature_2m_min: float
    precipitation_sum: float
    precipitation_hours: Optional[float]
    windspeed_10m_max: float
    winddirection_10m_dominant: Optional[float]
    weathercode: int

class ClimateResponse(BaseModel):
    location: str
    latitude: float
    longitude: float
    timezone: str
    elevation: float
    daily_forecast: List[DailyForecast]
    generated_time: str

class LocationRequest(BaseModel):
    location: str