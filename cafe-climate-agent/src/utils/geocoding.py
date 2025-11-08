import requests

def get_coordinates(location_name: str):
    """
    Converte nome da localização em coordenadas usando API do Open-Meteo
    """
    # Tratamento especial para cidades brasileiras
    brazilian_cities = {
        "barueri-sp": {"lat": -23.511, "lon": -46.876},
        "são paulo-sp": {"lat": -23.5489, "lon": -46.6388},
        "lavras-mg": {"lat": -21.248, "lon": -44.999},
        "varginha-mg": {"lat": -21.551, "lon": -45.430},
        "três pontas-mg": {"lat": -21.366, "lon": -45.512},
        "guaxupé-mg": {"lat": -21.305, "lon": -46.712},
        "boquira-ba": {"lat": -12.823, "lon": -42.731},
        "machado-mg": {"lat": -21.677, "lon": -45.921}
    }
    
    # Normaliza o nome para comparação
    normalized_name = location_name.lower().strip()
    
    # Verifica se é uma cidade conhecida
    if normalized_name in brazilian_cities:
        city_data = brazilian_cities[normalized_name]
        return {
            "latitude": city_data["lat"],
            "longitude": city_data["lon"],
            "timezone": "America/Sao_Paulo",
            "elevation": 0,
            "name": location_name
        }
    
    # Se não for uma cidade conhecida, tenta a API
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": location_name,
        "count": 1,
        "language": "pt",
        "format": "json"
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if not data.get("results"):
            # Fallback: tenta buscar apenas o nome da cidade (sem estado)
            city_only = location_name.split('-')[0].split(',')[0].strip()
            params["name"] = city_only + ", Brazil"
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if not data.get("results"):
                raise ValueError(f"Localização '{location_name}' não encontrada")
        
        result = data["results"][0]
        return {
            "latitude": result["latitude"],
            "longitude": result["longitude"],
            "timezone": result["timezone"],
            "elevation": result.get("elevation", 0),
            "name": result["name"]
        }
    except requests.exceptions.RequestException as e:
        raise Exception(f"Erro ao buscar coordenadas: {str(e)}")