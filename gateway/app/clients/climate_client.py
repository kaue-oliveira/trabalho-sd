import httpx
from app.utils.config import CLIMATE_AGENT_URL

async def get_climate_agent_client():
    async with httpx.AsyncClient(base_url=CLIMATE_AGENT_URL, timeout=30.0) as client:
        yield client