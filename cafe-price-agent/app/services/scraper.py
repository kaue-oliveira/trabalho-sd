import requests
import pandas as pd
from datetime import datetime, timedelta
import csv

def baixar_cepea(tipo_cafe):
    """
    Realiza scraping do site CEPEA para baixar dados históricos de preços.
    
    Args:
        tipo_cafe (str): 'arabica' ou 'robusta'
        dias (int): Número de dias para buscar (padrão: 120)
        
    Returns:
        str: Nome do arquivo XLS baixado
        
    Processo:
        1. Configura sessão HTTP com headers
        2. Calcula datas inicial e final
        3. Define tabela ID baseada no tipo de café
        4. Faz requisição AJAX para obter URL do arquivo
        5. Baixa e salva arquivo XLS
    """
    url_base = "https://www.cepea.org.br"
    DIAS = 120

    sessao = requests.Session()

    sessao.headers.update({"User-Agent": "Mozilla/5.0"})

    sessao.get(f"{url_base}/br/consultas-ao-banco-de-dados-do-site.aspx")

    data_final = datetime.now()

    data_inicial = data_final - timedelta(days=int((DIAS / 5) * 7))

    tabela_id = "23" if tipo_cafe == "arabica" else "24"
    
    params = {
        "tabela_id": tabela_id,
        "data_inicial": data_inicial.strftime("%d/%m/%Y"),
        "data_final": data_final.strftime("%d/%m/%Y"),
        "periodicidade": "1" 
    }

    resposta = sessao.get(
        f"{url_base}/br/consultas-ao-banco-de-dados-do-site.aspx",
        params=params,
        headers={"X-Requested-With": "XMLHttpRequest"}
    )

    url_arquivo = resposta.json()["arquivo"]

    conteudo = sessao.get(url_arquivo).content

    nome_xls = f"cepea_temp_{tipo_cafe}.xls"

    with open(nome_xls, "wb") as f:
        f.write(conteudo)

    return nome_xls

def ler_xls_para_csv(nome_xls, nome_csv="cepea_dados.csv"):
    """
    Converte arquivo XLS do CEPEA para CSV formatado.
    
    Args:
        nome_xls (str): Caminho do arquivo XLS de entrada
        nome_csv (str): Caminho do arquivo CSV de saída
        
    Returns:
        str: Nome do arquivo CSV gerado
        
    Processo:
        1. Lê XLS usando pandas com engine calamine
        2. Identifica células de data no formato DD/MM/AAAA
        3. Busca preços nas colunas adjacentes
        4. Remove duplicatas e salva CSV formatado
    """

    df = pd.read_excel(nome_xls, engine="calamine")
    dados = []

    for i in range(len(df)):
        for j in range(len(df.columns)):
            valor = str(df.iloc[i, j]).strip()

            if (len(valor) == 10 and valor[2] == "/" and valor[5] == "/" 
                and valor.replace("/", "").isdigit()):
                data = valor 

                for k in range(j + 1, min(j + 4, len(df.columns))):
                    preco_str = str(df.iloc[i, k]).replace(" ", "") 

                    if "," in preco_str:
                        try:
             
                            preco = float(preco_str.replace(".", "").replace(",", "."))
                            dados.append((data, preco))
                            break 
                        except:
                            continue

    dados = list(dict.fromkeys(dados))

    with open(nome_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Data", "Preco_R$"])
        for linha in dados:
            writer.writerow(linha)

    return nome_csv 
