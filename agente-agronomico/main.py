from fastapi import FastAPI, HTTPException
import os, json, requests
from models import Requisicao, Resposta


OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")
DECISION_MODEL = os.getenv("DECISION_MODEL", "phi")
RAG_URL = os.getenv("RAG_URL", "http://rag_service:8002")
GATEWAY_URL = os.getenv("GATEWAY_URL")  # opcional


class ExternalFetchError(Exception):
    pass


def _fetch_gateway_json(url: str, params: dict | None = None):
    try:
        r = requests.get(url, params=params, timeout=20)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        raise ExternalFetchError(str(e))


def get_climate_via_gateway(payload: dict) -> dict:
    if payload.get("clima"):
        return payload["clima"]
    if not GATEWAY_URL:
        return {}
    params = {"localidade": payload.get("localidade"), "data_colheita": payload.get("data_colheita")}
    return _fetch_gateway_json(f"{GATEWAY_URL}/climate", params)


def get_price_via_gateway(payload: dict) -> dict:
    if payload.get("preco"):
        return payload["preco"]
    if not GATEWAY_URL:
        return {}
    params = {"produto": "cafe"}
    return _fetch_gateway_json(f"{GATEWAY_URL}/price", params)


def rag_search(query: str, k: int = 4) -> list[dict]:
    try:
        r = requests.post(f"{RAG_URL}/rag/search", json={"query": query, "k": k}, timeout=30)
        r.raise_for_status()
        data = r.json()
        return data.get("results", [])
    except Exception:
        return []


def ollama_decide(clima: dict, preco: dict, relatorios: list[dict]) -> dict:
    prompt = f"""
    Você é um especialista agronômico em cafeicultura.
    Com base nos DADOS abaixo, decida **vender** ou **aguardar** e produza **apenas** um JSON válido com os campos:
    - decision: "vender" ou "aguardar"
    - explanation: texto conciso e detalhado justificando com base nos dados

    [DADOS DE CLIMA]\n{json.dumps(clima, ensure_ascii=False)}
    [DADOS DE PREÇO]\n{json.dumps(preco, ensure_ascii=False)}
    [TRECHOS DE RELATÓRIOS]\n{json.dumps(relatorios, ensure_ascii=False)}

    Restrições:
    - Responda **somente** o JSON final, sem comentários adicionais.
    - Use português do Brasil.
    - Seja específico citando janelas de tempo e tendências (subida/queda/volatilidade).
    """.strip()

    endpoints = [f"{OLLAMA_URL}/api/generate", f"{OLLAMA_URL}/v1/generate"]
    acc = ""
    last_err = None
    for ep in endpoints:
        if ep.endswith('/api/generate'):
            body = {"model": DECISION_MODEL, "prompt": prompt, "stream": True, "options": {"temperature": 0.2, "num_predict": 300}}
        else:
            body = {"model": DECISION_MODEL, "input": prompt, "stream": True, "options": {"temperature": 0.2, "num_predict": 300}}
        try:
            with requests.post(ep, json=body, stream=True, timeout=120) as resp:
                resp.raise_for_status()
                acc = ""
                for line in resp.iter_lines():
                    if not line:
                        continue
                    chunk = line.decode("utf-8")
                    try:
                        obj = json.loads(chunk)
                        piece = obj.get("response") or ""
                        if not piece and isinstance(obj.get("choices"), list) and obj["choices"]:
                            c0 = obj["choices"][0]
                            if isinstance(c0, dict):
                                delta = c0.get("delta") or {}
                                piece = delta.get("content") or ""
                            else:
                                piece = ""
                        acc += piece
                        if obj.get("done") or (isinstance(obj.get("choices"), list) and obj["choices"] and obj["choices"][0].get("finish_reason")):
                            break
                    except json.JSONDecodeError:
                        acc += chunk
                break
        except Exception as e:
            last_err = e
            continue

    if not acc:
        return {"decision": "aguardar", "explanation": f"Falha ao consultar o modelo: {last_err}"}

    txt = acc.strip()
    start = txt.find("{")
    end = txt.rfind("}")
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(txt[start:end+1])
        except Exception:
            pass

    decision = "vender" if "vender" in txt.lower() else "aguardar"
    return {"decision": decision, "explanation": txt}


app = FastAPI(title="Agente Agronômico", version="1.0.0")

@app.post("/recommend", response_model=Resposta)
def recommend(req: Requisicao):
    # 1) Obter clima/preço (ou usar os enviados)
    clima = get_climate_via_gateway(req.model_dump())
    preco = get_price_via_gateway(req.model_dump())


    # 2) Buscar contexto nos relatórios via RAG
    q = req.pergunta_relatorios or (
    f"Decisão de venda de café para {req.localidade or 'localidade desconhecida'}, "
    f"colheita em {req.data_colheita or 'data não informada'}, considerando {req.tipo_grao or 'tipo não informado'}, "
    f"clima: {clima}, preço: {preco}."
    )
    rels = rag_search(q, k=4)

    # 3) Decidir via LLM local (Ollama)
    out = ollama_decide(clima=clima, preco=preco, relatorios=rels)
    if not out or not out.get("decision"):
        raise HTTPException(status_code=500, detail="Falha ao gerar decisão")

    return Resposta(decision=out["decision"], explanation=out.get("explanation", ""), contexto_relatorios=rels)


@app.get("/")
def root():
    return {"status": "ok", "service": "agente_agronomico"}