from datetime import datetime, timedelta
import statistics

def calcular_desvio_padrao_10_dias(dados_90_dias):
    """
    Calcula desvio padrão de preços em períodos de 10 dias.
    
    Args:
        dados_90_dias (list): Lista de dicionários com 'data' e 'preco'
                             (90 dias mais recentes)
                             
    Returns:
        list: Lista de dicionários com períodos e desvios padrão
              (máximo 9 períodos)
              
    Processo:
        1. Ordena dados por data crescente
        2. Agrupa em blocos de 10 dias
        3. Calcula desvio padrão de cada bloco
        4. Formata período e retorna resultados
    """
    dados_ordenados = sorted(dados_90_dias, key=lambda x: x['data'])
    
    desvios = []
    for i in range(0, len(dados_ordenados), 10):
        periodo = dados_ordenados[i:i+10]
        if len(periodo) >= 2:  # Precisa de pelo menos 2 elementos para desvio padrão
            precos = [p['preco'] for p in periodo]
            desvio = statistics.stdev(precos)
            
            data_inicio = periodo[0]['data'].strftime('%d/%m/%Y')
            data_fim = periodo[-1]['data'].strftime('%d/%m/%Y')
            
            desvios.append({
                "periodo": f"{data_inicio} a {data_fim}",
                "desvio_padrao": round(desvio, 2)
            })
    
    return desvios[:9]


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
    dados_ordenados = sorted(dados_90_dias, key=lambda x: x['data'])
    
    medias = [] 
    for i in range(0, len(dados_ordenados) - 2, 3):
        periodo = dados_ordenados[i:i+3]
        if len(periodo) == 3:
            media_preco = sum([p['preco'] for p in periodo]) / 3
            
            data_inicio = periodo[0]['data'].strftime('%d/%m/%Y')
            data_fim = periodo[2]['data'].strftime('%d/%m/%Y')
            
            medias.append({
                "periodo": f"{data_inicio} a {data_fim}",
                "media": round(media_preco, 2) 
            })
    
    return medias[:30]


