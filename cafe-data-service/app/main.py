from fastapi import FastAPI
from app.routes import usuarios, analises, precos
from app.database import engine, Base

# Criar tabelas no banco (em produção usar Alembic para migrations)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Cafe Data Service",
    description="Serviço de dados para o sistema CafeQuality",
    version="1.0.0"
)

# Incluir rotas
app.include_router(usuarios.router)
app.include_router(analises.router)
app.include_router(precos.router)
@app.get("/")
def root():
    return {"message": "Cafe Data Service - API REST"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Cafe Data Service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)