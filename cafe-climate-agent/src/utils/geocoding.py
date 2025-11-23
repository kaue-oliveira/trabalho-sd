import requests
import unicodedata
from typing import Dict, Optional

def normalize_name(name: str) -> str:
    name = name.lower().strip()
    return "".join(
        c for c in unicodedata.normalize("NFD", name)
        if unicodedata.category(c) != "Mn"
    )

def get_coordinates(location_name: str) -> Dict[str, float | str]:
    """
    Converte nome de cidade em coordenadas, retornando *somente cidades do Brasil*.
    Agora utiliza o parâmetro 'country=BR' da própria API Open-Meteo.
    """
    normalized_name = normalize_name(location_name)

    url = "https://geocoding-api.open-meteo.com/v1/search"

    search_strategies = [normalized_name]

    if "-" in normalized_name or "," in normalized_name:
        city_only = normalized_name.split("-")[0].split(",")[0].strip()
        search_strategies.extend([
            city_only,
            f"{city_only}, Brazil"
        ])

    for search_term in search_strategies:
        try:
            params = {
                "name": search_term,
                "count": 10,
                "language": "pt-br",
                "format": "json",
                "country": "BR"        # ← FORÇA APENAS BRASIL
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            results = data.get("results", [])
            if not results:
                continue

            # Fallback: filtra novamente, por segurança
            results_br = [
                r for r in results
                if r.get("country", "").lower() == "brazil"
            ]

            if results_br:
                r = results_br[0]
            else:
                continue

            return {
                "latitude": r["latitude"],
                "longitude": r["longitude"],
                "timezone": r.get("timezone", "America/Sao_Paulo"),
                "elevation": r.get("elevation", 0),
                "name": r["name"],
                "country": r.get("country", "Brazil")
            }

        except requests.exceptions.RequestException as e:
            if search_term == search_strategies[-1]:
                raise Exception(f"Erro ao buscar coordenadas: {e}")
            continue

    raise ValueError(
        f"A localização '{location_name}' não foi encontrada no Brasil."
    )
