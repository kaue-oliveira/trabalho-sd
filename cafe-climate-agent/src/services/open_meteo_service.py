import requests
from datetime import datetime, timedelta
from models.climate_models import ClimateResponse, DailyForecast
from utils.geocoding import get_coordinates

class OpenMeteoService:
    def __init__(self):
        self.forecast_url = "https://api.open-meteo.com/v1/forecast"
        self.archive_url = "https://archive-api.open-meteo.com/v1/archive"

    def get_forecast(self, location: str) -> ClimateResponse:
        geo_data = get_coordinates(location)
        latitude, longitude = geo_data["latitude"], geo_data["longitude"]

        # ====== 1. PREVISÃO FUTURA (14 DIAS) ======
        forecast_params = {
            "latitude": latitude,
            "longitude": longitude,
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
            "forecast_days": 14
        }

        try:
            forecast_response = requests.get(self.forecast_url, params=forecast_params)
            forecast_response.raise_for_status()
            forecast_data = forecast_response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erro ao consultar previsão: {str(e)}")

        forecasts = self._parse_forecast(forecast_data)

        # ====== 2. HISTÓRICO (1, 2 e 3 MESES ATRÁS) ======
        now = datetime.utcnow()
        averages = {}

        for months_back in [1, 2, 3]:
            # Calcula período do mês correspondente
            ref_date = now.replace(day=1) - timedelta(days=(months_back * 30))
            start_date = ref_date.replace(day=1)
            end_date = (start_date + timedelta(days=30))

            archive_params = {
                "latitude": latitude,
                "longitude": longitude,
                "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": end_date.strftime("%Y-%m-%d"),
                "timezone": geo_data["timezone"],
                "daily": [
                    "temperature_2m_max",
                    "temperature_2m_min",
                    "precipitation_sum",
                    "windspeed_10m_max"
                ]
            }

            try:
                archive_response = requests.get(self.archive_url, params=archive_params)
                archive_response.raise_for_status()
                archive_data = archive_response.json()
            except requests.exceptions.RequestException as e:
                raise Exception(f"Erro ao consultar histórico: {str(e)}")

            averages[f"{months_back}_mes_atras"] = self._compute_monthly_average(archive_data)

        # ====== 3. RETORNO FINAL ======
        return ClimateResponse(
            location=location,
            latitude=latitude,
            longitude=longitude,
            timezone=geo_data["timezone"],
            elevation=geo_data["elevation"],
            daily_forecast=forecasts,
            past_month_averages=averages,
            generated_time=datetime.utcnow().isoformat()
        )

    def _parse_forecast(self, data: dict):
        daily_data = data["daily"]
        forecasts = []
        for i in range(len(daily_data["time"])):
            forecasts.append(DailyForecast(
                date=daily_data["time"][i],
                temperature_2m_max=daily_data["temperature_2m_max"][i],
                temperature_2m_min=daily_data["temperature_2m_min"][i],
                precipitation_sum=daily_data["precipitation_sum"][i],
                precipitation_hours=daily_data.get("precipitation_hours", [None])[i],
                windspeed_10m_max=daily_data["windspeed_10m_max"][i],
                winddirection_10m_dominant=daily_data.get("winddirection_10m_dominant", [None])[i],
                weathercode=daily_data["weathercode"][i]
            ))
        return forecasts

    def _compute_monthly_average(self, data: dict):
        """Calcula médias simples de temperatura, chuva e vento."""
        daily = data.get("daily", {})
        n = len(daily.get("time", []))
        if n == 0:
            return None

        def avg(values):
            valid = [v for v in values if v is not None]
            return sum(valid) / len(valid) if valid else None

        return {
            "temperature_max_avg": avg(daily.get("temperature_2m_max", [])),
            "temperature_min_avg": avg(daily.get("temperature_2m_min", [])),
            "precipitation_avg": avg(daily.get("precipitation_sum", [])),
            "windspeed_max_avg": avg(daily.get("windspeed_10m_max", []))
        }
