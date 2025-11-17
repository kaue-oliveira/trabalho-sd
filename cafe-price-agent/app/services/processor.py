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
    # Abertura do arquivo CSV com encoding UTF-8 para caracteres especiais
    with open(nome_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)  # Leitor que mapeia cada linha para dicionário
        dados = []  # Lista para armazenar dados processados
        
        # Itera sobre cada linha do CSV
        for linha in reader:
            # Converte string de data no formato DD/MM/AAAA para objeto datetime
            data = datetime.strptime(linha['Data'], '%d/%m/%Y')
            # Converte string de preço para float (ex: "1250,50" → 1250.50)
            preco = float(linha['Preco_R$'])
            # Adiciona dicionário com dados convertidos à lista
            dados.append({'data': data, 'preco': preco})
    
    # Ordena lista por data em ordem decrescente (mais recente primeiro)
    # key=lambda x: x['data'] - função que extrai campo data para ordenação
    # reverse=True - ordenação decrescente
    dados.sort(key=lambda x: x['data'], reverse=True)
    
    return dados  # Retorna lista ordenada de dicionários