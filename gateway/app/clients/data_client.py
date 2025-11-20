import httpx
from app.utils.config import DATA_SERVICE_URL

async def get_data_service_client():
    async with httpx.AsyncClient(base_url=DATA_SERVICE_URL, timeout=30.0) as client:
        yield client