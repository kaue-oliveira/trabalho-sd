from fastapi import FastAPI
from app.routes.price import router as price_router

# Cria aplicação FastAPI principal com metadados
app = FastAPI(title="Cafe Price Agent")

# Registra roteador de preços na aplicação principal
# Todas as rotas em price.py ficam sob o path base da aplicação
app.include_router(price_router)

@app.get("/")
def read_root():
    """
    Endpoint raiz para health check e verificação do serviço.
    
    Returns:
        dict: Mensagem de status do serviço
    """
    return {"message": "Cafe Price Agent está rodando"}