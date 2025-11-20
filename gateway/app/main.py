from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from .utils.config import GATEWAY_HOST, GATEWAY_PORT

from .routes import (
    agro_routes, analysis_routes,  auth_routes,
    climate_routes, healthy_routes, ollama_routes,
    price_routes, rag_routes, user_routes
)


app = FastAPI(
    title="AgroAnalytics Gateway",
    description="API Gateway para o sistema AgroAnalytics",
    version="1.1.0"
)   


# Configurar resposta JSON com UTF-8
@app.middleware("http")
async def add_charset_to_content_type(request: Request, call_next):
    response = await call_next(request)
    if "application/json" in response.headers.get("content-type", ""):
        response.headers["content-type"] = "application/json; charset=utf-8"
    return response


# CORS para o React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Rotas
app.include_router(healthy_routes.router)
app.include_router(auth_routes.router)
app.include_router(user_routes.router)
app.include_router(analysis_routes.router)
app.include_router(climate_routes.router)
app.include_router(price_routes.router)
app.include_router(agro_routes.router)
app.include_router(rag_routes.router)
app.include_router(ollama_routes.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=GATEWAY_HOST,
        port=GATEWAY_PORT,
        reload=True
    )