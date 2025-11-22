import httpx
from app.utils.config import OLLAMA_URL

async def get_ollama_client():
    async with httpx.AsyncClient(base_url=OLLAMA_URL, timeout=None) as client:
        yield client