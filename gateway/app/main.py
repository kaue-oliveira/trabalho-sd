from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import httpx
import time
from jose import jwt
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel

from .config import (
    GATEWAY_HOST, GATEWAY_PORT, CLIMATE_AGENT_URL, DATA_SERVICE_URL,
    SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
)

app = FastAPI(
    title="AgroAnalytics Gateway",
    description="API Gateway para o sistema AgroAnalytics",
    version="1.0.0"
)   

# Configurar resposta JSON com UTF-8
@app.middleware("http")
async def add_charset_to_content_type(request: Request, call_next):
    response = await call_next(request)
    if "application/json" in response.headers.get("content-type", ""):
        response.headers["content-type"] = "application/json; charset=utf-8"
    return response

# CORS para o React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()


# =====================================================
# **FUNÇÕES DE AUTENTICAÇÃO**
# =====================================================
def create_access_token(data: dict):
    # Cria token JWT
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # Verifica token JWT
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado"
        )


# =====================================================
# **CLIENTS HTTP**
# =====================================================
async def get_climate_agent_client():
    async with httpx.AsyncClient(base_url=CLIMATE_AGENT_URL, timeout=30.0) as client:
        yield client

async def get_data_service_client():
    async with httpx.AsyncClient(base_url=DATA_SERVICE_URL, timeout=30.0) as client:
        yield client


# =====================================================
# **ENDPOINTS DE HEALTH CHECK**
# =====================================================
@app.get("/")
async def root():
    return {"message": "CafeQuality Gateway está rodando!", "service": "gateway"}

@app.get("/health")
async def health_check():
    """Health check do Gateway"""
    return {
        "status": "healthy",
        "service": "gateway",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.get("/health/full")
async def full_health_check(
    client: httpx.AsyncClient = Depends(get_climate_agent_client),
    data_client: httpx.AsyncClient = Depends(get_data_service_client)
):
    """Health check completo incluindo serviços"""
    try:
        climate_response = await client.get("/health")
        climate_status = "healthy" if climate_response.status_code == 200 else "unhealthy"
    except Exception:
        climate_status = "unreachable"

    try:
        data_response = await data_client.get("/health")
        data_status = "healthy" if data_response.status_code == 200 else "unhealthy"
    except Exception:
        data_status = "unreachable"

    return {
        "gateway": "healthy",
        "climate_agent": climate_status,
        "data_service": data_status,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


# =====================================================
# **ENDPOINTS DE AUTENTICAÇÃO **
# =====================================================
class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict


@app.post("/auth/login", response_model=LoginResponse)
async def login(login_data: LoginRequest, data_client: httpx.AsyncClient = Depends(get_data_service_client)):
    """
    Autentica usuário via Data Service e gera JWT no Gateway
    """
    try:
        resp = await data_client.post("/auth/login", json=login_data.dict())
        resp.raise_for_status()
        response_data = resp.json()
        user_data = response_data["user"]

        token_data = {"sub": str(user_data["id"]), "email": user_data["email"]}
        access_token = create_access_token(token_data)

        return LoginResponse(access_token=access_token, user=user_data)

    except httpx.HTTPStatusError as e:
        detail = e.response.json().get("detail") if e.response.content else e.response.text
        raise HTTPException(
            status_code=e.response.status_code,
            detail=detail or "Erro de autenticação"
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Data Service não disponível: {str(e)}"
        )

@app.post("/auth/logout")
async def logout():
    return {"message": "Logout realizado com sucesso"}


@app.get("/auth/me")
async def get_current_user(payload: dict = Depends(verify_token), data_client: httpx.AsyncClient = Depends(get_data_service_client)):
    """
    Retorna dados do usuário atual via Data Service.
    """
    user_id = int(payload.get("sub"))
    try:
        resp = await data_client.get(f"/usuarios/{user_id}")
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Data Service não disponível: {str(e)}")


@app.post("/auth/forgot-password")
async def forgot_password(payload: dict, data_client: httpx.AsyncClient = Depends(get_data_service_client)):
    try:
        resp = await data_client.post("/auth/forgot-password", json=payload)
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Data Service não disponível: {str(e)}")


@app.post("/auth/reset-password")
async def change_password(payload: dict, data_client: httpx.AsyncClient = Depends(get_data_service_client)):
    try:
        resp = await data_client.post("/auth/reset-password", json=payload)
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Data Service não disponível: {str(e)}")


# =====================================================
# **ENDPOINTS DE USUARIOS (REGISTRO/UPDATE/DELETE)**
# =====================================================
@app.get("/usuarios")
async def listar_usuarios(data_client: httpx.AsyncClient = Depends(get_data_service_client)):
    try:
        resp = await data_client.get("/usuarios")
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Data Service não disponível: {str(e)}")
    
    
@app.post("/usuarios")
async def criar_usuario(user_data: dict, data_client: httpx.AsyncClient = Depends(get_data_service_client)):
    try:
        resp = await data_client.post("/usuarios", json=user_data)
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Data Service não disponível: {str(e)}")


@app.put("/usuarios/me")
async def atualizar_usuario(user_data: dict, token_payload: dict = Depends(verify_token), data_client: httpx.AsyncClient = Depends(get_data_service_client)):
    user_id = int(token_payload.get("sub"))
    try:
        resp = await data_client.put(f"/usuarios/{user_id}", json=user_data)
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Data Service não disponível: {str(e)}")


@app.delete("/usuarios/me")
async def deletar_usuario(token_payload: dict = Depends(verify_token), data_client: httpx.AsyncClient = Depends(get_data_service_client)):
    user_id = int(token_payload.get("sub"))
    try:
        resp = await data_client.delete(f"/usuarios/{user_id}")
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Data Service não disponível: {str(e)}")


# =====================================================
# **ENDPOINTS DE ANÁLISES**
# =====================================================
@app.get("/analises")
async def listar_analises(payload: dict = Depends(verify_token), data_client: httpx.AsyncClient = Depends(get_data_service_client)):
    user_id = int(payload.get("sub"))
    try:
        resp = await data_client.get(f"/analises/usuario/{user_id}")
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Data Service não disponível: {str(e)}")


@app.post("/analises")
async def criar_analise(analise_data: dict, payload: dict = Depends(verify_token), data_client: httpx.AsyncClient = Depends(get_data_service_client)):
    user_id = int(payload.get("sub"))
    analise_payload = { **analise_data, "usuario_id": user_id }
    try:
        resp = await data_client.post("/analises", json=analise_payload)
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Data Service não disponível: {str(e)}")


# =====================================================
# **ENDPOINTS PROXY PARA CLIMATE AGENT**
# =====================================================
@app.get("/climate/forecast")
async def get_climate_forecast(cidade: str, estado: str, payload: dict = Depends(verify_token), client: httpx.AsyncClient = Depends(get_climate_agent_client)):
    try:
        location = f"{cidade},{estado}"
        response = await client.get(f"/climate/forecast/{location}")
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Climate Agent não disponível: {str(e)}")

# =====================================================
# **ENDPOINTS PROXY PARA RAG SERVICE**
# =====================================================
@app.post("/rag/search")
async def rag_search_proxy(request: dict):
    """
    Proxy para o RAG service - busca semântica em documentos
    Sem autenticação pois é usado internamente pelos agentes
    """
    try:
        async with httpx.AsyncClient(timeout=None) as client:
            response = await client.post(
                "http://rag_service:8010/rag/search",
                json=request
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"RAG Service não disponível: {str(e)}")

# =====================================================
# **ENDPOINTS PROXY PARA OLLAMA**
# =====================================================
@app.post("/ollama/generate")
async def proxy_ollama_generate(request: Request):
    """
    Proxy para Ollama direto - sem service intermediário
    Arquitetura distribuída mantida via gateway
    """
    body = await request.json()
    try:
        start = time.perf_counter()
        async with httpx.AsyncClient(timeout=None) as client:
            response = await client.post(
                "http://ollama:11434/api/generate",
                json=body
            )
            duration = time.perf_counter() - start
            resp_json = response.json()
            # adicionar informações de timing no corpo para diagnóstico
            if isinstance(resp_json, dict):
                resp_json.setdefault("timings", {})
                resp_json["timings"]["gateway_proxy_seconds"] = round(duration, 3)
            return JSONResponse(content=resp_json, headers={"X-Proxy-Duration": f"{duration:.3f}"})
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Ollama timeout")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ollama/api/embeddings")
async def proxy_ollama_embeddings(request: Request):

    body = await request.json()
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "http://ollama:11434/api/embeddings",
                json=body
            )
            resp_json = response.json()
            return JSONResponse(content=resp_json)
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Ollama embeddings timeout")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=GATEWAY_HOST,
        port=GATEWAY_PORT,
        reload=True
    )