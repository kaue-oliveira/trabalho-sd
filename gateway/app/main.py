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
    GATEWAY_HOST, GATEWAY_PORT, CLIMATE_AGENT_URL,
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
# **DADOS MOCKADOS - AGUARDANDO DATASERVICE**
# =====================================================
MOCK_USUARIOS = [
    {
        "id": 1,
        "nome": "João Silva",
        "email": "joao.produtor@email.com",
        "tipo_conta": "PRODUTOR"
    },
    {
        "id": 2, 
        "nome": "Cooperativa Café Mineiro", 
        "email": "coop.mineira@email.com",
        "tipo_conta": "COOPERATIVA"
    }
]

# Senhas mockadas
MOCK_PASSWORDS = {
    1: "senha123",
    2: "senha123"
}

MOCK_ANALISES = [
    { "id": 1, "usuario_id": 1, "tipo_cafe": "Arábica", "data_colheita": "2025-10-15", "quantidade": 1500.50, "cidade": "Varginha", "estado": "MG", "estado_cafe": "verde", "data_analise": "2025-11-01", "decisao": "VENDER", "explicacao_decisao": "Preço do Arábica em alta de 8% no mercado futuro. Previsão de chuva intensa na região pode comprometer qualidade do grão armazenado. Relatórios indicam baixa oferta nos próximos 30 dias." },
    { "id": 2, "usuario_id": 1, "tipo_cafe": "Arábica", "data_colheita": "2025-09-20", "quantidade": 800.75, "cidade": "Varginha", "estado": "MG", "estado_cafe": "verde", "data_analise": "2025-10-10", "decisao": "VENDER_PARCIALMENTE", "explicacao_decisao": "Preço atual favorável com tendência de alta moderada. Previsão de geada no Paraná pode valorizar estoques. Vender 50% agora e aguardar potencial valorização." },
    { "id": 3, "usuario_id": 1, "tipo_cafe": "Robusta", "data_colheita": "2025-08-10", "quantidade": 1200.00, "cidade": "Varginha", "estado": "MG", "estado_cafe": "verde", "data_analise": "2025-09-05", "decisao": "AGUARDAR", "explicacao_decisao": "Mercado de Robusta saturado por exportações vietnamitas. Previsão de estiagem pode reduzir oferta nacional em 60 dias. Condições climáticas estáveis para armazenamento." },
    { "id": 4, "usuario_id": 2, "tipo_cafe": "Robusta", "data_colheita": "2024-11-10", "quantidade": 3000.00, "cidade": "Linhares", "estado": "ES", "estado_cafe": "verde", "data_analise": "2024-12-05", "decisao": "AGUARDAR", "explicacao_decisao": "Excesso de oferta no mercado internacional. Previsão de chuva no Espírito Santo pode melhorar qualidade. Esperar abertura de novos contratos de exportação." }
]

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
# **CLIENT HTTP PARA CLIMATE AGENT**
# =====================================================
async def get_climate_agent_client():
    async with httpx.AsyncClient(base_url=CLIMATE_AGENT_URL, timeout=30.0) as client:
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
async def full_health_check(client: httpx.AsyncClient = Depends(get_climate_agent_client)):
    """Health check completo incluindo Climate Agent"""
    try:
        climate_response = await client.get("/health")
        climate_status = "healthy" if climate_response.status_code == 200 else "unhealthy"
    except Exception:
        climate_status = "unreachable"

    return {
        "gateway": "healthy",
        "climate_agent": climate_status,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

# =====================================================
# **ENDPOINTS DE AUTENTICAÇÃO**
# =====================================================
class LoginRequest(BaseModel):
    email: str
    password: str

@app.post("/auth/login")
async def login(login_data: LoginRequest):
    """
    Login - usando dados mockados temporariamente
    """
    email = login_data.email
    password = login_data.password

    # Buscar usuário nos mocks
    usuario = next((u for u in MOCK_USUARIOS if u["email"] == email), None)
    
    # Verificar senha mockada
    if usuario and MOCK_PASSWORDS.get(usuario["id"]) == password:
        access_token = create_access_token(data={"sub": str(usuario["id"]), "email": email})
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": usuario
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou/e senha incorretos"
        )

@app.post("/auth/logout")
async def logout(payload: dict = Depends(verify_token)):
    return {"message": "Logout realizado com sucesso"}

@app.get("/auth/me")
async def get_current_user(payload: dict = Depends(verify_token)):
    user_id = int(payload.get("sub"))
    usuario = next((u for u in MOCK_USUARIOS if u["id"] == user_id), None)
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    return usuario

# VOU VER COMO FAÇO ISSO DAQUI DPS
@app.post("/auth/forgot-password")
async def forgot_password(payload: dict):
    """
    Simula envio de email de redefinição de senha (mock).
    """
    email = payload.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Email é obrigatório")

    usuario = next((u for u in MOCK_USUARIOS if u["email"] == email), None)
    if not usuario:
        return {"message": "Se o email existir, instruções foram enviadas."}

    # Simular envio (em produção: criar token e enviar email)
    return {"message": "Instruções de redefinição enviadas para o email informado."}

# VOU VER COMO FAÇO ISSO DAQUI DPS
@app.post("/auth/change-password")
async def change_password(payload: dict, token_payload: dict = Depends(verify_token)):

    new_password = payload.get("new_password")
    if not new_password:
        raise HTTPException(status_code=400, detail="Nova senha é obrigatória")

    user_id = int(token_payload.get("sub"))
    if user_id not in [u["id"] for u in MOCK_USUARIOS]:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    MOCK_PASSWORDS[user_id] = new_password
    return {"message": "Senha atualizada com sucesso."}

# =====================================================
# **ENDPOINTS DE USUARIOS (REGISTRO/UPDATE/DELETE)**
# =====================================================
@app.post("/usuarios")
async def criar_usuario(user_data: dict):
    """
    Registro de usuário (mock)
    """
    nome = user_data.get("nome")
    email = user_data.get("email")
    senha = user_data.get("senha")
    tipo_conta = user_data.get("tipo_conta", "PRODUTOR")

    if not nome or not email or not senha:
        raise HTTPException(status_code=400, detail="nome, email e senha são obrigatórios")

    # Verificar se email já existe
    if any(u for u in MOCK_USUARIOS if u["email"].lower() == email.lower()):
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    new_id = max([u["id"] for u in MOCK_USUARIOS] + [0]) + 1
    novo_usuario = {
        "id": new_id,
        "nome": nome,
        "email": email,
        "tipo_conta": tipo_conta.upper()
    }
    MOCK_USUARIOS.append(novo_usuario)
    MOCK_PASSWORDS[new_id] = senha
    return novo_usuario

@app.put("/usuarios/me")
async def atualizar_usuario(user_data: dict, token_payload: dict = Depends(verify_token)):
    """
    Atualiza dados do usuário autenticado (mock).
    """
    user_id = int(token_payload.get("sub"))
    usuario = next((u for u in MOCK_USUARIOS if u["id"] == user_id), None)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    novo_nome = user_data.get("nome")
    novo_email = user_data.get("email")
    novo_tipo = user_data.get("tipo_conta")
    nova_senha = user_data.get("senha")

    # Verificar conflito de email
    if novo_email and any(u for u in MOCK_USUARIOS if u["email"].lower() == novo_email.lower() and u["id"] != user_id):
        raise HTTPException(status_code=400, detail="Email já em uso")

    if novo_nome:
        usuario["nome"] = novo_nome
    if novo_email:
        usuario["email"] = novo_email
    if novo_tipo:
        usuario["tipo_conta"] = novo_tipo.upper()
    if nova_senha:
        MOCK_PASSWORDS[user_id] = nova_senha

    return usuario

@app.delete("/usuarios/me")
async def deletar_usuario(token_payload: dict = Depends(verify_token)):
    """
    Deleta usuário e análises associadas (mock).
    """
    user_id = int(token_payload.get("sub"))
    usuario = next((u for u in MOCK_USUARIOS if u["id"] == user_id), None)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")


    MOCK_USUARIOS[:] = [u for u in MOCK_USUARIOS if u["id"] != user_id]

    MOCK_PASSWORDS.pop(user_id, None)

    global MOCK_ANALISES
    MOCK_ANALISES = [a for a in MOCK_ANALISES if a["usuario_id"] != user_id]

    return {"message": "Usuário e dados associados removidos com sucesso."}

# =====================================================
# **ENDPOINTS DE ANÁLISES (MOCKADOS)**
# =====================================================
@app.get("/analises")
async def listar_analises(payload: dict = Depends(verify_token)):
    """
    Lista análises do usuário - dados mockados
    """
    user_id = int(payload.get("sub"))
    
    # Filtrar análises do usuário logado
    user_analises = [a for a in MOCK_ANALISES if a["usuario_id"] == user_id]
    return user_analises

@app.post("/analises")
async def criar_analise(
    analise_data: dict,
    payload: dict = Depends(verify_token)
):
    """
    Cria nova análise - mockado
    """
    user_id = int(payload.get("sub"))
    
    nova_analise = {
        "id": len(MOCK_ANALISES) + 1,
        "usuario_id": user_id,
        **analise_data,
        "data_analise": datetime.now(timezone.utc).date().isoformat(),
        "criado_em": datetime.now(timezone.utc).isoformat()
    }
    
    # Adicionar à lista mockada (em produção, salvar no banco)
    MOCK_ANALISES.append(nova_analise)
    
    return nova_analise

# =====================================================
# **ENDPOINTS MOCKADOS PARA AGENTE AGRÔNOMO**
# =====================================================
@app.get("/climate")
async def get_climate_data(
    localidade: str = None,
    data_colheita: str = None
):
    """
    Endpoint mockado para dados climáticos com estrutura real
    """
    # Extrair cidade e estado da localidade
    location_parts = (localidade or "Minas Gerais, Brasil").split(",")
    cidade = location_parts[0].strip() if len(location_parts) > 0 else "Desconhecida"
    estado = location_parts[1].strip() if len(location_parts) > 1 else "Brasil"
    
    # Gerar previsão para os próximos 7 dias
    daily_forecast = []
    base_date = datetime.now(timezone.utc).date()
    
    for i in range(7):
        forecast_date = base_date + timedelta(days=i)
        daily_forecast.append({
            "date": forecast_date.isoformat(),
            "temperature_2m_max": 28.5 - (i * 0.5),  # Simular variação
            "temperature_2m_min": 18.2 + (i * 0.3),
            "precipitation_sum": 5.0 if i % 2 == 0 else 0.0,  # Chuva em dias alternados
            "precipitation_hours": 2.0 if i % 2 == 0 else 0.0,
            "windspeed_10m_max": 15.2 + (i * 0.8),
            "winddirection_10m_dominant": 120,
            "weathercode": 61 if i % 2 == 0 else 0  # 61=chuva leve, 0=céu limpo
        })
    
    return {
        "location": f"{cidade}-{estado}",
        "latitude": -23.511,
        "longitude": -46.876,
        "timezone": "America/Sao_Paulo",
        "elevation": 719.0,
        "daily_forecast": daily_forecast,
        "generated_time": datetime.now(timezone.utc).isoformat()
    }

@app.get("/price")
async def get_price_data(
    tipo_grao: str = None,
    localidade: str = None
):
    """
    Endpoint mockado para dados históricos de preço do café
    Média de 5 anos, 1 ano, 3 meses, 1 mês e última semana (diário)
    """
    tipo = (tipo_grao or "arabica").lower()
    
    # Preços base por tipo
    precos_base = {
        "arabica": 1250.50,
        "robusta": 980.75,
        "conilon": 950.00
    }
    
    preco_base = precos_base.get(tipo, 1100.00)
    
    # Gerar dados históricos com variação
    def gerar_historico_diario(dias, preco_inicial):
        historico = []
        preco_atual = preco_inicial
        base_date = datetime.now(timezone.utc).date()
        
        for i in range(dias, 0, -1):
            data = base_date - timedelta(days=i)
            # Adicionar variação aleatória simulada
            variacao = (i % 10 - 5) * 2  # Variação de -10 a +10
            preco_atual = preco_inicial + variacao
            historico.append({
                "data": data.isoformat(),
                "preco_saca_60kg": round(preco_atual, 2)
            })
        
        return historico
    
    return {
        "tipo_grao": tipo,
        "moeda": "BRL",
        "preco_atual": preco_base,
        "data_consulta": datetime.now(timezone.utc).isoformat(),
        "historico": {
            "media_5_anos": {
                "preco_medio": round(preco_base * 0.85, 2),
                "variacao_percentual": -15.0,
                "periodo": "2020-2025"
            },
            "media_1_ano": {
                "preco_medio": round(preco_base * 0.92, 2),
                "variacao_percentual": -8.0,
                "periodo": "2024-2025"
            },
            "media_3_meses": {
                "preco_medio": round(preco_base * 0.96, 2),
                "variacao_percentual": -4.0,
                "periodo": "ago/2024-nov/2024"
            },
            "media_1_mes": {
                "preco_medio": round(preco_base * 0.98, 2),
                "variacao_percentual": -2.0,
                "periodo": "out/2024"
            },
            "ultima_semana_diario": gerar_historico_diario(7, preco_base)
        },
        "tendencia": "alta",
        "volatilidade": "moderada"
    }

# =====================================================
# **ENDPOINTS PROXY PARA CLIMATE AGENT**
# =====================================================
@app.get("/climate/forecast")
async def get_climate_forecast(
    cidade: str,
    estado: str,
    payload: dict = Depends(verify_token),
    client: httpx.AsyncClient = Depends(get_climate_agent_client)
):
    try:
        location = f"{cidade},{estado}"
        response = await client.get(f"/climate/forecast/{location}")
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except Exception as e:
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
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "http://rag_service:8002/rag/search",
                json=request
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"RAG Service não disponível: {str(e)}")

# =====================================================
# **ENDPOINTS PROXY PARA OLLAMA SERVICE**
# =====================================================
@app.post("/ollama/generate")
async def proxy_ollama_generate(request: Request):
    """
    Proxy para o serviço Ollama
    Timeout de 120s é suficiente para phi3:mini (responde em 10-30s)
    """
    body = await request.json()
    try:
        start = time.perf_counter()
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                "http://ollama_service:8004/generate",
                json=body
            )
            duration = time.perf_counter() - start
            resp_json = response.json()
            # adicionar informações de timing no corpo para diagnóstico
            if isinstance(resp_json, dict):
                resp_json.setdefault("timings", {})
                resp_json["timings"]["gateway_proxy_seconds"] = round(duration, 3)
                if "ollama_time_seconds" in resp_json:
                    resp_json["timings"]["ollama_time_seconds"] = resp_json.get("ollama_time_seconds")
            return JSONResponse(content=resp_json, headers={"X-Proxy-Duration": f"{duration:.3f}"})
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Ollama service timeout")
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