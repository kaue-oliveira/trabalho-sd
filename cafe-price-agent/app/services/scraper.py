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
    # Cria sessão HTTP para manter cookies e headers
    sessao = requests.Session()
    # Define User-Agent para simular navegador
    sessao.headers.update({"User-Agent": "Mozilla/5.0"})

    # Requisição inicial para obter cookies de sessão
    sessao.get(f"{url_base}/br/consultas-ao-banco-de-dados-do-site.aspx")

    # Cálculo do período temporal
    data_final = datetime.now()  # Data final é sempre atual
    # Data inicial: ajusta para garantir dias úteis (considera fins de semana)
    data_inicial = data_final - timedelta(days=int((DIAS / 5) * 7))

    # Mapeamento dinâmico do tipo de café para ID da tabela no CEPEA
    tabela_id = "23" if tipo_cafe == "arabica" else "24"
    
    # Parâmetros da requisição AJAX
    params = {
        "tabela_id": tabela_id,  # ID da tabela no banco do CEPEA
        "data_inicial": data_inicial.strftime("%d/%m/%Y"),  # Formato DD/MM/AAAA
        "data_final": data_final.strftime("%d/%m/%Y"),
        "periodicidade": "1"  # Periodicidade diária
    }

    # Requisição AJAX para obter URL do arquivo
    resposta = sessao.get(
        f"{url_base}/br/consultas-ao-banco-de-dados-do-site.aspx",
        params=params,
        headers={"X-Requested-With": "XMLHttpRequest"}  # Header para identificar AJAX
    )

    # Extrai URL do arquivo XLS da resposta JSON
    url_arquivo = resposta.json()["arquivo"]

    # Download do conteúdo do arquivo XLS
    conteudo = sessao.get(url_arquivo).content
    # Gera nome único do arquivo incluindo tipo de café
    nome_xls = f"cepea_temp_{tipo_cafe}.xls"

    # Salva arquivo XLS localmente
    with open(nome_xls, "wb") as f:
        f.write(conteudo)

    return nome_xls  # Retorna nome do arquivo salvo

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
    # Leitura do arquivo XLS usando engine calamine (compatível com .xls antigo)
    df = pd.read_excel(nome_xls, engine="calamine")
    dados = []  # Lista para armazenar tuplas (data, preço)

    # Iteração por todas as células da planilha
    for i in range(len(df)):  # Itera linhas
        for j in range(len(df.columns)):  # Itera colunas
            valor = str(df.iloc[i, j]).strip()  # Obtém e limpa valor da célula

            # Identifica padrão de data (DD/MM/AAAA)
            if (len(valor) == 10 and valor[2] == "/" and valor[5] == "/" 
                and valor.replace("/", "").isdigit()):
                data = valor  # Armazena data encontrada

                # Busca preço nas 3 colunas seguintes
                for k in range(j + 1, min(j + 4, len(df.columns))):
                    preco_str = str(df.iloc[i, k]).replace(" ", "")  # Remove espaços

                    # Verifica se string contém vírgula (formato brasileiro)
                    if "," in preco_str:
                        try:
                            # Converte formato brasileiro para float
                            # Ex: "1.250,50" → 1250.50
                            preco = float(preco_str.replace(".", "").replace(",", "."))
                            dados.append((data, preco))  # Adiciona tupla à lista
                            break  # Para busca após encontrar primeiro preço válido
                        except:
                            continue  # Continua se conversão falhar

    # Remove duplicatas mantendo ordem (usando dict)
    dados = list(dict.fromkeys(dados))

    # Escrita do arquivo CSV formatado
    with open(nome_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Data", "Preco_R$"])  # Cabeçalho
        for linha in dados:
            writer.writerow(linha)  # Escreve cada linha de dados

    return nome_csv  # Retorna nome do arquivo gerado
