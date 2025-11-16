from fastapi import FastAPI, Request
import requests
import json
import os
import logging
import time

# Configurar logging com UTF-8
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Ollama Decision Service")

OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://ollama:11434/api/generate")
MODEL = os.getenv("MODEL", "mistral")

@app.on_event("startup")
async def warmup_model():
    """
    Pré-carrega o modelo Ollama no startup para evitar timeout na primeira requisição
    """
    logger.info(f"Iniciando pré-carregamento do modelo {MODEL}...")
    try:
        warmup_prompt = "Teste de inicialização"
        response = requests.post(
            OLLAMA_API_URL,
            json={
                "model": MODEL,
                "prompt": warmup_prompt,
                "stream": False
            },
            timeout=90
        )
        if response.status_code == 200:
            logger.info(f"✅ Modelo {MODEL} pré-carregado com sucesso!")
        else:
            logger.warning(f"⚠️  Falha ao pré-carregar modelo: {response.status_code}")
    except Exception as e:
        logger.error(f"❌ Erro ao pré-carregar modelo: {e}")

@app.get("/")
def root():
    return {"service": "ollama_service", "status": "ok", "model": MODEL}

@app.get("/health")
def health():
    return {"status": "healthy", "model": MODEL}

@app.post("/generate")
async def generate_recommendation(request: Request):
    """
    Gera decisão de venda baseada em clima, preço e relatórios técnicos
    Modelo já está pré-carregado, então a resposta é mais rápida
    """
    data = await request.json()
    clima = data.get("clima", {})
    preco = data.get("preco", {})
    relatorios = data.get("relatorios", [])
    localidade = data.get("localidade", "")
    data_colheita = data.get("data_colheita", "")

    # Montar contexto dos relatórios
    contexto_relatorios = "\n".join([
        f"- {r.get('text', '')[:200]}..." 
        for r in relatorios[:3]
    ])

    # Montar prompt com encoding UTF-8 explícito
    clima_str = json.dumps(clima, indent=2, ensure_ascii=False)
    preco_str = json.dumps(preco, indent=2, ensure_ascii=False)
    
    prompt = f"""Você é um assistente especialista em café. Analise os dados abaixo e recomende se o produtor deve VENDER, AGUARDAR ou VENDER_PARCIALMENTE o café.

Localidade: {localidade}
Data de Colheita: {data_colheita}

Clima: {clima_str}

Preço: {preco_str}

Contexto de relatórios técnicos:
{contexto_relatorios}

Forneça sua resposta APENAS em JSON válido com os campos:
{{"decision": "vender|aguardar|vender_parcialmente", "explanation": "explicação detalhada em até 200 palavras com acentuação correta em português"}}
"""

    try:
        logger.info(f"🤖 Gerando decisão para {localidade}...")
        
        # Chamar Ollama com streaming desabilitado
        # Timeout de 90s é suficiente para phi3:mini (responde em ~10-20s)
        start = time.perf_counter()
        response = requests.post(
            OLLAMA_API_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "format": "json"
            },
            timeout=90,
            headers={"Content-Type": "application/json; charset=utf-8"}
        )
        duration = time.perf_counter() - start
        response.raise_for_status()
        
        # Garantir encoding UTF-8 na resposta
        response.encoding = 'utf-8'
        response_data = response.json()
        response_text = response_data.get("response", "{}")
        
        logger.info(f"✅ Decisão gerada com sucesso (tempo={duration:.3f}s)")
        
        # Tentar parsear a resposta JSON do modelo
        try:
            decision_data = json.loads(response_text)
            return {
                "decision": decision_data.get("decision", "aguardar").lower(),
                "explanation": decision_data.get("explanation", "Decisão gerada pelo modelo de IA"),
                "ollama_time_seconds": round(duration, 3)
            }
        except json.JSONDecodeError:
            logger.warning(f"Resposta do modelo não é JSON válido")
            # Se não conseguir parsear, retornar resposta como texto
            return {
                "decision": "aguardar",
                "explanation": response_text[:500] if response_text else "Não foi possível gerar recomendação.",
                "ollama_time_seconds": round(duration, 3)
            }
            
    except requests.exceptions.Timeout:
        logger.error("Timeout ao gerar decisão")
        return {
            "decision": "aguardar",
            "explanation": "Timeout ao gerar decisão. Por favor, tente novamente.",
            "ollama_time_seconds": None
        }
    except Exception as e:
        logger.error(f"Erro ao gerar decisão: {e}")
        return {
            "decision": "aguardar",
            "explanation": f"Erro ao gerar decisão: {str(e)}",
            "ollama_time_seconds": None
        }