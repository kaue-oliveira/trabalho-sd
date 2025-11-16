import os
import glob
import requests
from pypdf import PdfReader
import chromadb
import re

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")
EMBED_MODEL = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")
CHROMA_PATH = os.getenv("CHROMA_PATH", "/data/chroma")

# inicializa o ChromaDB
client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_or_create_collection("relatorios")

def embed_text(text: str):
    r = requests.post(
        f"{OLLAMA_URL}/api/embeddings",
        json={"model": EMBED_MODEL, "prompt": text}
    )
    return r.json()["embedding"]

def load_pdfs_from_folder(folder="./pdfs"):
    pdf_paths = glob.glob(os.path.join(folder, "*.pdf"))
    print(f"[RAG] Encontrados {len(pdf_paths)} PDFs para indexar.")

    for pdf_path in pdf_paths:
        file_name = os.path.basename(pdf_path)
        print(f"[RAG] Processando PDF: {file_name}")

        try:
            reader = PdfReader(pdf_path)
            texts = []
            ids = []
            metadatas = []

            for page_index, page in enumerate(reader.pages):
                text = page.extract_text() or ""
                chunk_id = f"{file_name}_p{page_index}"

                texts.append(text)
                ids.append(chunk_id)
                metadatas.append({
                    "file": file_name,
                    "page": page_index
                })

            # gera embeddings
            embeddings = [embed_text(t) for t in texts]

            # salva na coleção
            collection.add(
                ids=ids,
                documents=texts,
                embeddings=embeddings,
                metadatas=metadatas
            )

            print(f"[RAG] PDF '{file_name}' indexado com sucesso.")

        except Exception as e:
            print(f"[RAG] Erro processando {file_name}: {e}")

def clean_text(text: str) -> str:
    # Remove múltiplas quebras de linha
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    
    # Remove espaços duplicados
    text = re.sub(r" {2,}", " ", text)

    # Remove números isolados quebrados (ruído comum em PDFs)
    text = re.sub(r"\b\d+\s+\n", "", text)

    # Remove códigos de página soltos
    text = re.sub(r"^\s*\d+\s*$", "", text, flags=re.MULTILINE)

    # Remove texto "quebrado" que está no meio de palavras
    text = text.replace(" \n", " ").replace("\n ", " ")

    # Normaliza novas linhas
    text = text.replace("\n", " ").strip()

    return text

def search(query: str, k: int = 5):
    vec = embed_text(query)

    res = collection.query(
        query_embeddings=[vec],
        n_results=k,
        include=["documents", "metadatas", "distances"]
    )

    results = []
    for i in range(len(res["ids"][0])):
        raw_text = res["documents"][0][i]
        cleaned_text = clean_text(raw_text)

        results.append({
            "text": cleaned_text,
            "metadata": res["metadatas"][0][i],
            "distance": res["distances"][0][i]
        })

    return results
