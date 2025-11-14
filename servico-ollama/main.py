from fastapi import FastAPI, Request
import requests
import json

app = FastAPI(title="Ollama Text Service", version="1.0.0")

OLLAMA_API_URL = "http://ollama:11434/api/generate"
MODEL = "mistral"  # ou outro modelo disponível localmente

@app.post("/generate")
async def generate_recommendation(request: Request):
    data = await request.json()
    clima = data.get("clima")
    preco = data.get("preco")
    analise = data.get("analise")

    prompt = f"""
    Você é um especialista em cafeicultura.
    Com base nestes dados:
    - Clima: {clima}
    - Preço: {preco}
    - Análise agronômica: {analise}

    Gere uma recomendação em linguagem natural, curta e explicativa,
    dizendo o que o produtor deve fazer (vender, esperar, armazenar, etc.)
    """

    response = requests.post(OLLAMA_API_URL, json={
        "model": MODEL,
        "prompt": prompt
    }, stream=True)

    result_text = ""
    for line in response.iter_lines():
        if line:
            data = json.loads(line.decode("utf-8"))
            if "response" in data:
                result_text += data["response"]

    return {"recomendacao": result_text.strip() or "Não foi possível gerar recomendação."}