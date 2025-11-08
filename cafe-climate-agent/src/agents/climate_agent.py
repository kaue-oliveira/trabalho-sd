from fastapi import FastAPI, HTTPException
from services.open_meteo_service import OpenMeteoService
from models.climate_models import ClimateResponse, LocationRequest

app = FastAPI(
    title="Agente Climático - Cafeicultura",
    description="Agente para consulta de dados climáticos para cafeicultura",
    version="1.0.0"
)

service = OpenMeteoService()

@app.get("/")
async def root():
    return {"message": "Agente Climático para Cafeicultura - Online"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/climate/forecast", response_model=ClimateResponse)
async def get_climate_forecast(request: LocationRequest):
    """
    Retorna a previsão climática para 14 dias de uma localização
    """
    try:
        forecast = service.get_forecast(request.location)
        return forecast
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/climate/forecast/{location}")
async def get_climate_forecast_by_path(location: str):
    """
    Retorna a previsão climática para 14 dias via path parameter
    """
    try:
        forecast = service.get_forecast(location)
        return forecast
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)