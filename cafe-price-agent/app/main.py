from fastapi import FastAPI
from app.routes.price import router as price_router

app = FastAPI(title="Cafe Price Agent")

app.include_router(price_router)

@app.get("/")
def read_root():
    """
    Endpoint raiz para health check e verificação do serviço.
    
    Returns:
        dict: Mensagem de status do serviço
    """
    return {"message": "Cafe Price Agent está rodando"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
