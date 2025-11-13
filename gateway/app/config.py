import os
from dotenv import load_dotenv

load_dotenv()

GATEWAY_HOST = os.getenv("GATEWAY_HOST", "0.0.0.0")
GATEWAY_PORT = int(os.getenv("GATEWAY_PORT", "3000"))

# URL do Climate Agent
CLIMATE_AGENT_URL = os.getenv("CLIMATE_AGENT_URL", "http://localhost:8000")

# Configurações JWT
SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_key_change_in_production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))