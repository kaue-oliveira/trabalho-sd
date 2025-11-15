from fastapi import FastAPI
from app.routes.price import router as price_router

app = FastAPI(
    title="Agente de Preço do Café",
    version="1.0.0",
    description="Serviço que faz scraping dos preços, comunica com gateway e calcula médias móveis."
)

app.include_router(price_router)

@app.get("/")
async def root():
    return {"service": "price_agent", "status": "running"}