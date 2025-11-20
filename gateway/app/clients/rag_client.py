import httpx
from app.utils.config import RAG_SERVICE_URL

async def get_rag_service_client():
    async with httpx.AsyncClient(base_url=RAG_SERVICE_URL, timeout=None) as client:
        yield client

