import csv
from datetime import datetime

def processar_dados(nome_csv):
    """
    Processa dados de um arquivo CSV contendo informações de preços de café.
    
    Args:
        nome_csv (str): Caminho para o arquivo CSV com dados de preços
        
    Returns:
        list: Lista de dicionários ordenada por data (mais recente primeiro)
              Cada dicionário contém 'data' (datetime) e 'preco' (float)
              
    Processo:
        1. Abre e lê arquivo CSV usando DictReader
        2. Converte string de data para objeto datetime
        3. Converte string de preço para float
        4. Ordena dados por data em ordem decrescente
    """
    with open(nome_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f) 
        dados = []

        for linha in reader:
            data = datetime.strptime(linha['Data'], '%d/%m/%Y')

            preco = float(linha['Preco_R$'])

            dados.append({'data': data, 'preco': preco})

    dados.sort(key=lambda x: x['data'], reverse=True)
    
    return dados
