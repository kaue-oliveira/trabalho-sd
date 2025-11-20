import httpx
from app.utils.config import PRICE_AGENT_URL

async def get_price_agent_client():
    async with httpx.AsyncClient(base_url=PRICE_AGENT_URL, timeout=30.0) as client:
        yield client
