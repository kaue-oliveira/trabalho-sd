import httpx
from typing import Tuple

class GeocodingService:
    def __init__(self):
        self.base_url = "https://geocoding-api.open-meteo.com/v1/search"
    
    async def get_coordinates(self, location_name: str) -> Tuple[float, float, float, str]:
        """Converte nome da localização em coordenadas"""
        async with httpx.AsyncClient() as client:
            params = {
                "name": location_name,
                "count": 1,
                "language": "pt",
                "format": "json"
            }
            
            response = await client.get(self.base_url, params=params)
            data = response.json()
            
            if not data.get("results"):
                raise ValueError(f"Localização '{location_name}' não encontrada")
            
            result = data["results"][0]
            return (
                result["latitude"],
                result["longitude"], 
                result.get("elevation", 0),
                result.get("timezone", "America/Sao_Paulo")
            )