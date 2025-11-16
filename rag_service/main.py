from fastapi import FastAPI
from rag_loader import load_pdfs_from_folder, search

app = FastAPI(title="RAG Service")

@app.get("/")
def root():
    return {"service": "RAG Service", "status": "healthy"}

@app.on_event("startup")
def startup_event():
    try:
        print("[RAG] Carregando PDFs automaticamente...")
        load_pdfs_from_folder("./pdfs")
    except Exception as e:
        print(f"[RAG] Erro ao carregar PDFs: {e}")

@app.post("/rag/search")
def rag_search(body: dict):
    query = body.get("query")
    k = body.get("k", 4)
    return {"results": search(query, k)}

@app.post("/rag/reload")
def reload_pdfs():
    try:
        load_pdfs_from_folder("./pdfs")
        return {"status": "success", "message": "PDFs recarregados com sucesso"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/rag/status")
def get_status():
    """Verifica quantos documentos estão indexados"""
    from rag_loader import collection
    try:
        count = collection.count()
        return {"status": "ok", "indexed_documents": count}
    except Exception as e:
        return {"status": "error", "message": str(e)}
