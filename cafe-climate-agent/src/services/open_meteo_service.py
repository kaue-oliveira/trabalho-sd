import requests
from datetime import datetime
from models.climate_models import ClimateResponse, DailyForecast
from utils.geocoding import get_coordinates

class OpenMeteoService:
    def __init__(self):
        self.base_url = "https://api.open-meteo.com/v1/forecast"
    
    def get_forecast(self, location: str) -> ClimateResponse:
        # Primeiro obtém as coordenadas
        geo_data = get_coordinates(location)
        
        # Parâmetros para a API do Open-Meteo
        params = {
            "latitude": geo_data["latitude"],
            "longitude": geo_data["longitude"],
            "timezone": geo_data["timezone"],
            "daily": [
                "temperature_2m_max",
                "temperature_2m_min", 
                "precipitation_sum",
                "precipitation_hours",
                "windspeed_10m_max",
                "winddirection_10m_dominant",
                "weathercode"
            ],
            "forecast_days": 14  # Próximas 2 semanas
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            return self._parse_response(data, geo_data, location)
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erro ao consultar API meteorológica: {str(e)}")
    
    def _parse_response(self, data: dict, geo_data: dict, location: str) -> ClimateResponse:
        daily_data = data["daily"]
        
        forecasts = []
        for i in range(len(daily_data["time"])):
            forecast = DailyForecast(
                date=daily_data["time"][i],
                temperature_2m_max=daily_data["temperature_2m_max"][i],
                temperature_2m_min=daily_data["temperature_2m_min"][i],
                precipitation_sum=daily_data["precipitation_sum"][i],
                precipitation_hours=daily_data.get("precipitation_hours", [None])[i],
                windspeed_10m_max=daily_data["windspeed_10m_max"][i],
                winddirection_10m_dominant=daily_data.get("winddirection_10m_dominant", [None])[i],
                weathercode=daily_data["weathercode"][i]
            )
            forecasts.append(forecast)
        
        return ClimateResponse(
            location=location,
            latitude=geo_data["latitude"],
            longitude=geo_data["longitude"],
            timezone=geo_data["timezone"],
            elevation=geo_data["elevation"],
            daily_forecast=forecasts,
            generated_time=datetime.utcnow().isoformat()
        )