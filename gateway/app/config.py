import os
from dotenv import load_dotenv

load_dotenv()

GATEWAY_HOST = os.getenv("GATEWAY_HOST", "0.0.0.0")
GATEWAY_PORT = int(os.getenv("GATEWAY_PORT", "3000"))

# URL dos serviços/agentes
DATA_SERVICE_URL = os.getenv("DATA_SERVICE_URL", "http://data-service:8000")
CLIMATE_AGENT_URL = os.getenv("CLIMATE_AGENT_URL", "http://cafe-climate-agent:8000")
AGRO_AGENT_URL = os.getenv("AGRO_AGENT_URL", "http://agro-agent:8000")
RAG_SERVICE_URL = os.getenv("RAG_SERVICE_URL", "http://rag-service:8000")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")

# Configurações JWT
SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_key_change_in_production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))   