import httpx
import os
import asyncio
import time
import json

client = httpx.AsyncClient(timeout=None)

GATEWAY_URL = os.getenv("GATEWAY_URL", "http://gateway:3000")

# --------- CLIMA / PREÇO EM PARALELO ---------

async def get_climate_async(payload: dict) -> dict:
    """Busca dados climáticos via Gateway"""
    if payload.get("clima"):
        return payload["clima"]
    if not GATEWAY_URL:
        return {}
    
    cidade = payload.get("cidade", "")
    estado = payload.get("estado", "")
    
    if not cidade or not estado:
        return {}
    
    try:
        r = await client.get(
            f"{GATEWAY_URL}/climate/forecast",
            params={"cidade": cidade, "estado": estado}
        )
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"[ERROR] Falha ao buscar clima: {e}")
        return {}

async def get_price_async(payload: dict) -> dict:
    """Busca dados de preço via Gateway"""
    if payload.get("preco"):
        return payload["preco"]
    if not GATEWAY_URL:
        return {}
    
    tipo_cafe = payload.get("tipo_cafe", "arabica")
    
    try:
        r = await client.get(f"{GATEWAY_URL}/price/{tipo_cafe}")
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"[ERROR] Falha ao buscar preço: {e}")
        return {}

# --------- RAG ---------

async def rag_search_async(query: str, k: int = 4):
    """Busca semântica em relatórios técnicos"""
    r = await client.post(f"{GATEWAY_URL}/rag/search", json={"query": query, "k": k})
    r.raise_for_status()
    return r.json().get("results", [])

# --------- OLLAMA ---------

def resumir_preco(preco):
    # extrai listas
    medias = [m["media"] for m in preco["medias_moveis_3_dias"]]
    
    # cálculos
    media_geral = sum(medias) / len(medias)
    minimo = min(medias)
    maximo = max(medias)
    
    preco_atual = preco["preco_atual"]
    variacao = ((preco_atual - minimo) / minimo) * 100

    preco_resumido = (
        f"Preço atual: {preco_atual:.2f}.\n"
        f"Média das últimas {len(medias)} médias móveis: {media_geral:.2f}.\n"
        f"Variação percentual dos últimos 90 dias: {variacao:.2f}%.\n"
    )

    return preco_resumido


def resumir_clima(clima):
    forecast = clima["daily_forecast"]

    # últimos 7 dias (ou tudo se quiser full range: forecast)
    ultimos_7 = forecast[-7:]

    dias_secos = sum(1 for d in ultimos_7 if d["precipitation_sum"] == 0)
    chuva_alta = any(d["precipitation_sum"] > 5 for d in forecast)
    
    # risco de mofo: chuva alta + muitas horas + mínimas elevadas
    risco_mofo = any(
        (d["precipitation_sum"] > 5 and 
         d["precipitation_hours"] >= 8 and 
         d["temperature_2m_min"] >= 18)
        for d in forecast
    )

    clima_resumido = (
        "Resumo climático:\n"
        f"- Dias secos na semana: {dias_secos}\n"
        f"- Precipitação alta prevista? {'Sim' if chuva_alta else 'Não'}\n"
        f"- Risco de mofo: {'Sim' if risco_mofo else 'Não'}\n"
    )

    return clima_resumido


async def solicitar_decisao_ollama_async(payload: dict):   
    clima = payload.get("clima", {})
    preco = payload.get("preco", {})
    relatorios = payload.get("relatorios", [])
    
    tipo_cafe = payload.get("tipo_cafe", "")
    cidade = payload.get("cidade", "")
    estado = payload.get("estado", "")
    data_colheita = payload.get("data_colheita", "")
    quantidade = payload.get("quantidade", 0)
    estado_cafe = payload.get("estado_cafe", "")

    preco_resumido = resumir_preco(preco)
    clima_resumido = resumir_clima(clima)
    prompt = f"""
Você é um especialista em cafeicultura e comercialização de café.

Sua análise deve seguir OBRIGATORIAMENTE esta ordem:

1. Interpretar os dados numéricos de preço.
2. Interpretar os dados numéricos do clima.
3. Considerar a condição do café armazenado.
4. Usar relatórios técnicos APENAS como complemento.
5. Tomar a decisão final com base MAJORITÁRIA nos dados recentes enviados (preço e clima).

Nunca use análises históricas irrelevantes dos PDFs se os dados numéricos atuais já forem suficientes.

---

### DADOS ESTRUTURADOS PARA ANÁLISE (PRINCIPAIS)
**PREÇO:**
{preco_resumido}

**CLIMA:**
{clima_resumido}

---

### INFORMAÇÕES COMPLEMENTARES (USO SECUNDÁRIO)
- Tipo de café: {tipo_cafe}
- Cidade: {cidade}, {estado}
- Data de colheita: {data_colheita}
- Quantidade: {quantidade}
- Estado do café: {estado_cafe}

---

### RELATÓRIOS TÉCNICOS (USO APENAS SE NECESSÁRIO)
{relatorios}

---

Agora siga estas regras lógicas obrigatórias:

- Se o preço atual está acima das médias → favorece VENDER.
- Se o clima é arriscado para armazenamento (chuva, umidade) → favorece VENDER.
- Se o preço está subindo fortemente → favorece AGUARDAR.
- Se os preços estão caindo → favorece VENDER.
- Se não houver tendência clara → dê peso MAIOR ao preço atual.
- Se PDFs contradirem os dados numéricos, IGNORE os PDFs.

---

Responda APENAS este JSON:

{{
  "decisao": "vender" ou "aguardar",
  "explicacao": "máximo 200 palavras, citando explicitamente preços e clima"
}}
"""



    try:
        start = time.perf_counter()
        
        # Log dos dados climáticos que estão sendo enviados ao Ollama
        print(f"[CLIMA] Dados climáticos enviados ao Ollama: {clima}")
        print(f"[PREÇO] Dados de preço enviados ao Ollama: {preco}")
        
        r = await client.post(
            f"{GATEWAY_URL}/ollama/generate",
            json={
                "model": "phi3:mini",
                "prompt": prompt,
                "stream": False,
                "format": "json"
            }
        )
        duration = time.perf_counter() - start
        r.raise_for_status()

        raw = r.json().get("response", "")
        decision_data = json.loads(raw)

        return {
            "decisao": decision_data.get("decisao", "aguardar").lower(),
            "explicacao": decision_data.get("explicacao", ""),
            "ollama_time_seconds": round(duration, 3)
        }

    except Exception as e:
        print(f"[ERROR] Erro ao consultar Ollama: {e}")
        return {
            "decisao": "aguardar",
            "explicacao": f"Erro ao consultar modelo: {e}",
            "ollama_time_seconds": None
        }

# --------- BUSCA EM PARALELO ---------
async def fetch_all_parallel(payload: dict, rag_query: str) -> tuple[dict, dict, list]:
    """
    Busca clima, preço e RAG em paralelo usando asyncio.gather
    Retorna: (clima, preco, relatorios)
    """
    async def safe_get_climate():
        try:
            return await get_climate_async(payload)
        except Exception:
            return {}
    
    async def safe_get_price():
        try:
            return await get_price_async(payload)
        except Exception:
            return {}
    
    async def safe_get_rag():
        try:
            return await rag_search_async(rag_query, k=4)
        except Exception:
            return []
    
    clima, preco, rels = await asyncio.gather(
        safe_get_climate(),
        safe_get_price(),
        safe_get_rag()
    )
    
    return clima, preco, rels
