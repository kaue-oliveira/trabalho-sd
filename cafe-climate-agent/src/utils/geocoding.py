import requests
import unicodedata
from typing import Dict, Optional

def normalize_name(name: str) -> str:
    """Remove acentos e padroniza o nome da cidade"""
    name = name.lower().strip()
    return "".join(
        c for c in unicodedata.normalize("NFD", name)
        if unicodedata.category(c) != "Mn"
    )

def get_coordinates(location_name: str) -> Dict[str, float | str]:
    """
    Converte qualquer nome de cidade em coordenadas via API Open-Meteo.
    Aceita entradas no formato livre, ex: 'Lavras', 'Lavras-MG', 'Lisboa, Portugal'.
    
    Args:
        location_name: Nome da localidade a ser geocodificada
        
    Returns:
        Dict com latitude, longitude, timezone, elevation e nome
        
    Raises:
        ValueError: Quando a localização não é encontrada
        Exception: Quando há erro na requisição à API
    """
    # Normaliza o nome
    normalized_name = normalize_name(location_name)

    # Configuração da API
    url = "https://geocoding-api.open-meteo.com/v1/search"
    
    # Estratégias de busca em ordem de prioridade
    search_strategies = [
        normalized_name,  # Tentativa original
    ]
    
    # Adiciona fallbacks se o nome original contiver separadores
    if '-' in normalized_name or ',' in normalized_name:
        city_only = normalized_name.split('-')[0].split(',')[0].strip()
        search_strategies.extend([
            city_only,
            f"{city_only}, Brazil",  # Fallback para Brasil
        ])

    for search_term in search_strategies:
        try:
            params = {
                "name": search_term,
                "count": 1,
                "language": "pt",
                "format": "json"
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data.get("results"):
                result = data["results"][0]
                return {
                    "latitude": result["latitude"],
                    "longitude": result["longitude"],
                    "timezone": result.get("timezone", "America/Sao_Paulo"),
                    "elevation": result.get("elevation", 0),
                    "name": result["name"],
                    "country": result.get("country", "N/A")
                }
                
        except requests.exceptions.RequestException as e:
            # Se for a última tentativa, levanta a exceção
            if search_term == search_strategies[-1]:
                raise Exception(f"Erro ao buscar coordenadas: {e}")
            # Caso contrário, continua para a próxima estratégia
            continue

    raise ValueError(f"Localização '{location_name}' não encontrada após {len(search_strategies)} tentativas.")

# Exemplo de uso:
if __name__ == "__main__":
    try:
        coords = get_coordinates("São Paulo-SP")
        print(f"Coordenadas: {coords}")
    except (ValueError, Exception) as e:
        print(f"Erro: {e}")