import httpx
from app.utils.config import AGRO_AGENT_URL

async def get_agro_agent_client():
    async with httpx.AsyncClient(base_url=AGRO_AGENT_URL, timeout=600.0) as client:
        yield client