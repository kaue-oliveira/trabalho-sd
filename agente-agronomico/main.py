from fastapi import FastAPI, HTTPException
from models import Requisicao, Resposta
from utils import fetch_all_parallel, solicitar_decisao_ollama_async

app = FastAPI(title="Agente Agronômico")

@app.post("/recommend", response_model=Resposta)
async def recommend(req: Requisicao):
    # Construir localidade a partir de cidade e estado
    localidade = f"{req.cidade},{req.estado}"
    
    # Construir query RAG
    query_parts = [
        f"café {req.tipo_cafe}",
        f"região {req.cidade} {req.estado}",
        f"colheita {req.data_colheita}",
        f"qualidade {req.estado_cafe}",
        "preço mercado recomendação venda"
    ]
    query = " ".join(query_parts)
    
    # Buscar dados em paralelo
    clima, preco, rels = await fetch_all_parallel(
        {
            "cidade": req.cidade,
            "estado": req.estado,
            "data_colheita": req.data_colheita,
            "tipo_cafe": req.tipo_cafe
        },
        query
    )

    payload = {
        "tipo_cafe": req.tipo_cafe,
        "data_colheita": req.data_colheita,
        "quantidade": req.quantidade,
        "cidade": req.cidade,
        "estado": req.estado,
        "estado_cafe": req.estado_cafe,
        "localidade": localidade,
        "clima": clima,
        "preco": preco,
        "relatorios": rels
    }

    # Solicitar decisão ao modelo de IA
    try:
        out = await solicitar_decisao_ollama_async(payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar decisão: {str(e)}")

    if not out.get("decisao"):
        raise HTTPException(status_code=500, detail="Falha ao gerar decisão final.")

    # Extrair e logar as fontes (arquivos PDF) consultadas
    fontes = []
    if rels:  # Se há resultados RAG
        fontes = list(set([
            rel.get("metadata", {}).get("file", "Desconhecido") 
            for rel in rels if rel.get("metadata") and rel.get("metadata").get("file")
        ]))
    
    # Log das fontes consultadas (não retornadas na API)
    if fontes:
        print(f"[RAG] PDFs utilizados na análise: {', '.join(fontes)}")
    else:
        print("[RAG] Nenhum PDF específico foi utilizado na análise")

    return Resposta(
        decisao=out["decisao"],
        explicacao_decisao=out.get("explicacao", ""),
    )

@app.get("/")
def root():
    return {"status": "ok", "service": "agente_agronomico"}

@app.get("/health")
def health():
    return {"status": "healthy", "service": "agente_agronomico"}