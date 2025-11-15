from typing import List, Dict

def gerar_medias_3em3(historico: List[Dict]) -> List[float]:
    """
    Gera médias móveis de 3 em 3 dias sobre os 90 dias do histórico.
    
    Parâmetro:
        historico: lista de dicionários no formato:
            [{"data": "YYYY-MM-DD", "preco": 1234.56}, ...]
            
    Retorno:
        lista contendo 30 médias (float)
    """
    if not historico:
        return []
    
    # Extrair apenas os preços (usar somente os 90 primeiros)
    precos = [item["preco"] for item in historico[:90] if item.get("preco") is not None]
    
    if len(precos) < 3:
        return []
    
    # Garantir que temos pelo menos 90 preços (preencher com o último se necessário)
    while len(precos) < 90:
        precos.append(precos[-1] if precos else 0)
    
    # Calcular médias de 3 em 3 dias
    medias = []
    for i in range(0, 90, 3):
        grupo = precos[i:i+3]
        if len(grupo) == 3:
            media = sum(grupo) / 3
            medias.append(round(media, 2))
    
    return medias[:30]  # Garantir no máximo 30 médias