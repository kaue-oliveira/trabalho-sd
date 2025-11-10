from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import date

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
    location: str
