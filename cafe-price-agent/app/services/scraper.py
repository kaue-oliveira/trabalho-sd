import requests
from bs4 import BeautifulSoup
from datetime import datetime

BASE_URL = "https://www.noticiasagricolas.com.br/cotacoes/cafe"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

def scrape_price(tipo_cafe: str):
    """
    Retorna o preço mais atualizado do café (arábica ou robusta) no formato:
    {
        "data": "YYYY-MM-DD",
        "preco": 1234.56
    }
    """
    try:
        response = requests.get(BASE_URL, headers=HEADERS, timeout=10)
        response.raise_for_status()
        html = BeautifulSoup(response.content, "html.parser")

        blocos = html.find_all("div", class_="cotacao")
        tabela_encontrada = None

        for bloco in blocos:
            titulo = bloco.find("h2")
            if not titulo:
                continue

            titulo_normalizado = titulo.get_text(strip=True).lower()

            if tipo_cafe == "arabica" and ("arábica" in titulo_normalizado or "arabica" in titulo_normalizado):
                tabela_encontrada = bloco.find("table")
                break

            if tipo_cafe == "robusta" and ("robusta" in titulo_normalizado):
                tabela_encontrada = bloco.find("table")
                break

        if tabela_encontrada is None:
            return None

        corpo = tabela_encontrada.find("tbody")
        if not corpo:
            return None
            
        linha = corpo.find("tr")
        if not linha:
            return None
            
        colunas = linha.find_all("td")
        if len(colunas) < 2:
            return None

        data_br = colunas[0].get_text(strip=True)
        preco_br = colunas[1].get_text(strip=True)

        # Data BR → ISO
        data_iso = datetime.strptime(data_br, "%d/%m/%Y").date().isoformat()

        # "2.204,71" → 2204.71
        preco_float = float(preco_br.replace(".", "").replace(",", "."))

        return {"data": data_iso, "preco": preco_float}
        
    except Exception as e:
        print(f" Erro no scraping: {e}")
        return None