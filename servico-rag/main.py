import os, io, uuid, requests
from typing import List
from fastapi import FastAPI, UploadFile, File, HTTPException
from pypdf import PdfReader
import chromadb
from chromadb.config import Settings

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")
EMBED_MODEL = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")
CHROMA_PATH = os.getenv("CHROMA_PATH", "/data/chroma")

app = FastAPI(title="RAG Service", version="1.0.0")

client = chromadb.PersistentClient(path=CHROMA_PATH, settings=Settings(allow_reset=True))
collection = client.get_or_create_collection(name="relatorios", metadata={"hnsw:space": "cosine"})

# --- Helpers -----------------------------------------------------------------

def embed_texts(texts: List[str]) -> List[List[float]]:
    vecs = []
    for t in texts:
        # Prefer the newer OpenAI-like Ollama endpoint /v1/embeddings; fall back to older /api/embeddings
        endpoints = [f"{OLLAMA_URL}/v1/embeddings", f"{OLLAMA_URL}/api/embeddings", f"{OLLAMA_URL}/embeddings"]
        last_exc = None
        for ep in endpoints:
            try:
                # The /v1 endpoint expects 'input' while older API used 'prompt'
                payload = {"model": EMBED_MODEL, "input": t}
                r = requests.post(ep, json=payload, timeout=30)
                # If server replies 404 for missing model, surface a helpful error
                if r.status_code == 404:
                    # try to parse a JSON error message
                    try:
                        err = r.json()
                        # standard Ollama error shape: {'error': {'message': '...'}}
                        msg = None
                        if isinstance(err, dict):
                            if 'error' in err and isinstance(err['error'], dict):
                                msg = err['error'].get('message')
                            elif 'message' in err:
                                msg = err.get('message')
                        if msg and 'not found' in msg:
                            raise HTTPException(status_code=502, detail=(
                                f"Embedding model '{EMBED_MODEL}' not found on Ollama (endpoint: {ep}).\n"
                                f"Pull the model into Ollama and try again. Example (on the host):\n"
                                f"  docker exec -it <ollama_container> ollama pull {EMBED_MODEL}\n"
                                f"Or run inside the Ollama container: ollama pull {EMBED_MODEL}\n"
                                f"Original error: {msg}"
                            ))
                    except HTTPException:
                        raise
                    except Exception:
                        # fall through to normal error handling below
                        pass
                if r.status_code >= 400:
                    # raise so our outer except handles formatting the message
                    r.raise_for_status()
                data = r.json()
                # Possible response shapes:
                # 1) {'embedding': [...]} (older)
                # 2) {'data': [{'embedding': [...]}], ...} (OpenAI-like)
                embedding = None
                if isinstance(data, dict) and "embedding" in data:
                    embedding = data["embedding"]
                elif isinstance(data, dict) and "data" in data and isinstance(data["data"], list) and len(data["data"]) > 0:
                    first = data["data"][0]
                    if isinstance(first, dict) and "embedding" in first:
                        embedding = first["embedding"]
                    elif isinstance(first, list):
                        # sometimes 'data' may be list of embeddings directly
                        embedding = first[0]
                # If still not found, try top-level 'embeddings' key
                if embedding is None and isinstance(data, dict) and "embeddings" in data:
                    embedding = data["embeddings"]

                if embedding is None:
                    raise HTTPException(status_code=502, detail=f"Invalid embedding response from {ep}: {data}")

                vecs.append(embedding)
                last_exc = None
                break
            except requests.exceptions.RequestException as e:
                last_exc = e
                # try next endpoint
                continue
        if last_exc is not None:
            # Surface a clearer error to the client instead of a 500 stack trace
            detail = f"Embedding request failed: {last_exc}"
            if hasattr(last_exc, 'response') and last_exc.response is not None:
                try:
                    body = last_exc.response.text
                except Exception:
                    body = '<unreadable response body>'
                detail += f"; response={last_exc.response.status_code}: {body}"
            raise HTTPException(status_code=502, detail=detail)
    return vecs

# Simples chunking por página/parágrafos

def chunk_page_text(text: str, max_chars: int = 700, overlap: int = 80) -> List[str]:
    text = " ".join(text.split())
    chunks = []
    i = 0
    while i < len(text):
        chunk = text[i:i+max_chars]
        chunks.append(chunk)
        i += max_chars - overlap
    return chunks

# --- Endpoints ---------------------------------------------------------------

@app.post("/rag/upload")
def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Envie um PDF")

    content = file.file.read()
    reader = PdfReader(io.BytesIO(content))

    doc_id = str(uuid.uuid4())
    texts, ids, metadatas = [], [], []

    for page_idx, page in enumerate(reader.pages):
        page_text = page.extract_text() or ""
        for j, chunk in enumerate(chunk_page_text(page_text)):
            cid = f"{doc_id}_{page_idx}_{j}"
            texts.append(chunk)
            ids.append(cid)
            metadatas.append({"doc_id": doc_id, "page": page_idx, "chunk": j, "source": file.filename})

    if not texts:
        raise HTTPException(status_code=400, detail="PDF sem texto extraível")

    embs = embed_texts(texts)
    collection.add(documents=texts, embeddings=embs, ids=ids, metadatas=metadatas)

    return {"ok": True, "doc_id": doc_id, "chunks": len(texts)}

@app.post("/rag/search")
def search(payload: dict):
    query = payload.get("query")
    k = int(payload.get("k", 4))
    if not query:
        raise HTTPException(status_code=400, detail="'query' obrigatório")

    qvec = embed_texts([query])[0]
    res = collection.query(query_embeddings=[qvec], n_results=k, include=["documents", "metadatas", "distances"])

    out = []
    for i in range(len(res["ids"][0])):
        out.append({
            "text": res["documents"][0][i],
            "metadata": res["metadatas"][0][i],
            "distance": res["distances"][0][i],
        })
    return {"results": out}

@app.get("/")
def root():
    return {"status": "ok", "collection": collection.name}