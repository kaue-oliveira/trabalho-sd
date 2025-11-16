from datetime import datetime, timedelta

def calcular_medias_moveis(dados_90_dias):
    """
    Calcula médias móveis de preços em períodos de 3 dias.
    
    Args:
        dados_90_dias (list): Lista de dicionários com 'data' e 'preco'
                             (90 dias mais recentes)
                             
    Returns:
        list: Lista de dicionários com períodos e médias
              (máximo 30 períodos)
              
    Processo:
        1. Ordena dados por data crescente
        2. Agrupa em blocos de 3 dias
        3. Calcula média aritmética de cada bloco
        4. Formata período e retorna resultados
    """
    # Ordena dados por data (mais antiga primeiro) para cálculo sequencial
    # Necessário pois entrada vem ordenada por data decrescente
    dados_ordenados = sorted(dados_90_dias, key=lambda x: x['data'])
    
    medias = []  # Lista para armazenar resultados
    # Itera em passos de 3 para formar blocos de 3 dias
    for i in range(0, len(dados_ordenados) - 2, 3):
        periodo = dados_ordenados[i:i+3]  # Fatia bloco de 3 elementos
        # Verifica se bloco tem exatamente 3 elementos
        if len(periodo) == 3:
            # Calcula média aritmética dos preços do período
            media_preco = sum([p['preco'] for p in periodo]) / 3
            # Formata datas para string (DD/MM/AAAA)
            data_inicio = periodo[0]['data'].strftime('%d/%m/%Y')
            data_fim = periodo[2]['data'].strftime('%d/%m/%Y')
            
            # Adiciona dicionário com informações do período
            medias.append({
                "periodo": f"{data_inicio} a {data_fim}",  # String descritiva
                "media": round(media_preco, 2)  # Média com 2 casas decimais
            })
    
    return medias[:30]  # Retorna no máximo 30 médias (90 dias / 3)