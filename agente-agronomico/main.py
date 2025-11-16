from fastapi import FastAPI, HTTPException
from models import Requisicao, Resposta
from utils import fetch_all_parallel, solicitar_decisao_ollama_async

app = FastAPI(title="Agente Agronômico")

@app.post("/recommend", response_model=Resposta)
async def recommend(req: Requisicao):
    # Construir query RAG antes de paralelizar
    query_parts = []
    if req.localidade:
        query_parts.append(f"região {req.localidade}")
    if req.tipo_grao:
        query_parts.append(f"café {req.tipo_grao}")
    if req.data_colheita:
        query_parts.append(f"colheita {req.data_colheita}")
    
    query_parts.append("preço mercado recomendação venda")
    query = " ".join(query_parts)
    
    # 🚀 PARALELIZAÇÃO: Buscar clima, preço e RAG simultaneamente
    clima, preco, rels = await fetch_all_parallel(
        req.model_dump(),
        query
    )

    # Montar payload para Ollama
    payload = {
        "localidade": req.localidade,
        "data_colheita": req.data_colheita,
        "clima": clima,
        "preco": preco,
        "relatorios": rels
    }

    # Solicitar decisão ao modelo de IA
    try:
        out = await solicitar_decisao_ollama_async(payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar decisão: {str(e)}")

    if not out.get("decision"):
        raise HTTPException(status_code=500, detail="Falha ao gerar decisão final.")

    # Extrair apenas as fontes (arquivos PDF) consultadas, sem duplicatas
    fontes = list(set([
        rel.get("metadata", {}).get("source", "Desconhecido")
        for rel in rels
    ]))

    return Resposta(
        decision=out["decision"],
        explanation=out.get("explanation", ""),
        fontes_consultadas=fontes,
    )

@app.get("/")
def root():
    return {"status": "ok", "service": "agente_agronomico"}