"""
Módulo do Agente Agronômico - Núcleo de decisão do sistema

Este módulo contém funções para análise de dados climáticos, de preços e relatórios
de mercado, construção de prompts para o modelo de IA e tomada de decisão final.
"""

from typing import Dict, Any


def analyze_climate_factors(clima: dict) -> float:
    """
    Analisa fatores climáticos e retorna um score (0.0 = aguardar, 1.0 = vender)
    
    Args:
        clima: Dicionário com dados climáticos do Open-Meteo contendo:
               - daily_forecast: previsão dos próximos 14 dias
               - past_month_averages: médias históricas
        
    Returns:
        Score entre 0.0 e 1.0 indicando favorabilidade para venda
    """
    score = 0.5  # Score neutro
    
    if not clima or "daily_forecast" not in clima:
        return score
    
    forecast = clima.get("daily_forecast", [])
    if not forecast:
        return score
    
    # Analisa próximos 7 dias (período crítico para decisão)
    next_7_days = forecast[:7]
    
    # Calcula médias dos próximos 7 dias
    avg_temp_max = sum(day.get("temperature_2m_max", 20) for day in next_7_days) / len(next_7_days)
    avg_temp_min = sum(day.get("temperature_2m_min", 15) for day in next_7_days) / len(next_7_days)
    total_precipitation = sum(day.get("precipitation_sum", 0) for day in next_7_days)
    total_precip_hours = sum(day.get("precipitation_hours", 0) for day in next_7_days)
    avg_windspeed = sum(day.get("windspeed_10m_max", 10) for day in next_7_days) / len(next_7_days)
    
    # 1. Análise de temperatura (peso maior)
    # Temperatura ideal para armazenamento/transporte: 18-28°C
    if 18 <= avg_temp_max <= 28 and avg_temp_min >= 12:
        score += 0.25  # Condições ótimas
    elif avg_temp_max > 32 or avg_temp_min < 10:
        score -= 0.30  # Condições ruins (risco de deterioração)
    elif avg_temp_max > 30:
        score -= 0.15  # Calor excessivo
    
    # 2. Análise de precipitação (muito importante para logística)
    # Chuva dificulta transporte e pode afetar qualidade
    if total_precipitation < 10:  # Pouca chuva
        score += 0.30  # Excelente para venda (logística facilitada)
    elif total_precipitation < 30:
        score += 0.10  # Aceitável
    elif total_precipitation > 80:  # Muita chuva
        score -= 0.35  # Aguardar (logística comprometida)
    elif total_precipitation > 50:
        score -= 0.20
    
    # 3. Análise de horas de chuva (complementar)
    if total_precip_hours > 48:  # Mais de 48h de chuva em 7 dias
        score -= 0.15  # Período chuvoso prolongado
    elif total_precip_hours == 0:
        score += 0.10  # Período seco ideal
    
    # 4. Análise de vento (menor peso, mas relevante para secagem)
    if avg_windspeed > 20:  # Ventos muito fortes
        score -= 0.10  # Pode dificultar operações
    elif 10 <= avg_windspeed <= 18:
        score += 0.05  # Bom para secagem natural
    
    return max(0.0, min(1.0, score))


def analyze_price_trends(preco: dict) -> float:
    """
    Analisa tendências de preço e retorna um score (0.0 = aguardar, 1.0 = vender)
    
    Args:
        preco: Dicionário com dados do agente de preços contendo:
               - preco_atual: preço atual
               - medias_moveis_3_dias: histórico de médias móveis
               - dias_analisados: período de análise
        
    Returns:
        Score entre 0.0 e 1.0 indicando favorabilidade para venda
    """
    score = 0.5
    
    if not preco or "preco_atual" not in preco:
        return score
    
    preco_atual = preco.get("preco_atual", 0)
    medias_moveis = preco.get("medias_moveis_3_dias", [])
    
    if not medias_moveis or preco_atual == 0:
        return score
    
    # Pega as últimas médias móveis para análise de tendências
    # Últimas 10 médias = ~30 dias de análise
    recent_averages = [m.get("media", 0) for m in medias_moveis[-10:] if m.get("media")]
    
    if len(recent_averages) < 3:
        return score
    
    # 1. Comparação do preço atual com médias recentes (peso alto)
    media_ultimos_10_periodos = sum(recent_averages) / len(recent_averages)
    media_ultimos_5_periodos = sum(recent_averages[-5:]) / len(recent_averages[-5:])
    media_ultimos_3_periodos = sum(recent_averages[-3:]) / len(recent_averages[-3:])
    
    # Se preço atual está acima das médias = bom momento para vender
    variacao_vs_media_10 = (preco_atual - media_ultimos_10_periodos) / media_ultimos_10_periodos
    variacao_vs_media_5 = (preco_atual - media_ultimos_5_periodos) / media_ultimos_5_periodos
    variacao_vs_media_3 = (preco_atual - media_ultimos_3_periodos) / media_ultimos_3_periodos
    
    # Preço atual acima das médias = VENDER
    if variacao_vs_media_10 > 0.05:  # 5% acima da média de 30 dias
        score += 0.20
    elif variacao_vs_media_10 < -0.05:  # 5% abaixo
        score -= 0.15
    
    if variacao_vs_media_5 > 0.03:  # 3% acima da média de 15 dias
        score += 0.15
    elif variacao_vs_media_5 < -0.03:
        score -= 0.10
    
    # 2. Análise de tendência (preços subindo ou caindo?)
    # Compara primeiros 3 períodos com últimos 3 períodos
    if len(recent_averages) >= 6:
        media_inicio = sum(recent_averages[:3]) / 3
        media_fim = sum(recent_averages[-3:]) / 3
        tendencia = (media_fim - media_inicio) / media_inicio
        
        if tendencia > 0.10:  # Tendência de alta > 10%
            # Preços subindo = pode valer aguardar mais um pouco
            score -= 0.15
        elif tendencia < -0.10:  # Tendência de queda > 10%
            # Preços caindo = VENDER antes que caia mais
            score += 0.25
        elif -0.05 < tendencia < 0.05:  # Estável
            # Mercado estável = analisar outros fatores
            score += 0.05
    
    # 3. Volatilidade recente (últimos 5 períodos)
    if len(recent_averages) >= 5:
        volatilidade = max(recent_averages[-5:]) - min(recent_averages[-5:])
        volatilidade_percentual = volatilidade / media_ultimos_5_periodos
        
        if volatilidade_percentual > 0.15:  # Alta volatilidade (>15%)
            # Mercado instável = se preço está bom, VENDER
            if variacao_vs_media_3 > 0:
                score += 0.15
            else:
                score -= 0.10
    
    # 4. Momentum de curto prazo (últimos 3 períodos)
    if len(recent_averages) >= 3:
        # Verifica se está acelerando pra cima ou pra baixo
        diff_1 = recent_averages[-1] - recent_averages[-2]
        diff_2 = recent_averages[-2] - recent_averages[-3]
        
        if diff_1 > 0 and diff_2 > 0 and diff_1 > diff_2:  # Acelerando pra cima
            score -= 0.10  # Pode subir mais, aguardar
        elif diff_1 < 0 and diff_2 < 0 and abs(diff_1) > abs(diff_2):  # Acelerando pra baixo
            score += 0.15  # Vender antes que caia mais
    
    return max(0.0, min(1.0, score))


def analyze_market_reports(relatorios: list) -> float:
    """
    Analisa relatórios de mercado via RAG e retorna um score
    
    Args:
        relatorios: Lista de relatórios do RAG
        
    Returns:
        Score entre 0.0 e 1.0 indicando favorabilidade para venda
    """
    score = 0.5
    
    if not relatorios:
        return score
    
    # Análise das recomendações
    positive_keywords = ["vender", "alta", "crescimento", "valorização", "positivo", "boa", "favorável"]
    negative_keywords = ["aguardar", "queda", "baixa", "desvalorização", "negativo", "risco", "desfavorável"]
    
    # Combina todo o texto dos relatórios
    all_text = " ".join([
        rel.get("content", "") + " " + str(rel.get("metadata", {}))
        for rel in relatorios
    ]).lower()
    
    positive_count = sum(1 for keyword in positive_keywords if keyword in all_text)
    negative_count = sum(1 for keyword in negative_keywords if keyword in all_text)
    
    if positive_count > negative_count:
        score += 0.3
    elif negative_count > positive_count:
        score -= 0.3
    
    return max(0.0, min(1.0, score))


def calculate_decision_score(climate_score: float, price_score: float, market_score: float) -> float:
    """
    Calcula score final da decisão baseado nos pesos
    
    Pesos:
    - climate: 0.35 (35%)
    - price_trend: 0.40 (40%)
    - market_reports: 0.25 (25%)
    
    Args:
        climate_score: Score climático
        price_score: Score de preços
        market_score: Score de mercado
        
    Returns:
        Score final entre 0.0 e 1.0
    """
    decision_weights = {
        "climate": 0.35,
        "price_trend": 0.40,
        "market_reports": 0.25
    }
    
    total_score = (
        climate_score * decision_weights["climate"] +
        price_score * decision_weights["price_trend"] +
        market_score * decision_weights["market_reports"]
    )
    return round(total_score, 3)


def build_ai_prompt(payload: dict, clima: dict, preco: dict, relatorios: list, 
                   climate_score: float, price_score: float, market_score: float,
                   decision_score: float, decision: str) -> str:
    """
    Constrói prompt para explicação da decisão tomada pelo agente
    
    Este prompt inclui:
    1. Decisão tomada pelo agente
    2. Dados estruturados (preço e clima)
    3. Scores calculados pelo agente
    4. Relatórios técnicos como contexto
    
    Args:
        payload: Dados da requisição original
        clima: Dados climáticos
        preco: Dados de preços
        relatorios: Relatórios do RAG
        climate_score: Score climático calculado
        price_score: Score de preços calculado
        market_score: Score de mercado calculado
        decision_score: Score final da decisão
        decision: Decisão final ("vender" ou "aguardar")
        
    Returns:
        String com o prompt formatado
    """
    tipo_cafe = payload.get("tipo_cafe", "")
    cidade = payload.get("cidade", "")
    estado = payload.get("estado", "")
    data_colheita = payload.get("data_colheita", "")
    quantidade = payload.get("quantidade", 0)
    estado_cafe = payload.get("estado_cafe", "")
    
    prompt = f"""
        Você é um especialista em cafeicultura e comercialização de café.

        **IMPORTANTE**: A decisão já foi tomada pelo sistema de análise quantitativa. 
        Seu papel é APENAS explicar e justificar esta decisão de forma clara e técnica.

        ---

        ### DECISÃO FINAL DO AGENTE AGRONÔMICO: {decision.upper()}

        Esta decisão foi calculada através de análise quantitativa com os seguintes resultados:

        **ANÁLISE QUANTITATIVA:**
        - Score Climático: {climate_score:.3f} (peso 35%)
        - Score de Preços: {price_score:.3f} (peso 40%)  
        - Score de Mercado: {market_score:.3f} (peso 25%)
        - **Score Final: {decision_score:.3f}** → Limiar: 0.6 para VENDER

        ---

        ### DADOS QUE FUNDAMENTARAM A DECISÃO

        **DADOS CLIMÁTICOS (próximos 7 dias):**
        {clima}

        **DADOS DE PREÇOS:**
        {preco}

        **INFORMAÇÕES DO CAFÉ:**
        - Tipo: {tipo_cafe}
        - Localização: {cidade}, {estado}
        - Data de colheita: {data_colheita}
        - Quantidade: {quantidade} sacas
        - Estado: {estado_cafe}

        **RELATÓRIOS TÉCNICOS (contexto adicional):**
        {relatorios}

        ---

        Sua tarefa é explicar por que a decisão de **{decision.upper()}** é apropriada baseada nos dados acima.

        Considere na explicação:
        1. Como as condições climáticas dos próximos 7 dias influenciam
        2. O que as tendências de preço indicam
        3. O estado atual do café e logística
        4. Insights relevantes dos relatórios técnicos

        Responda APENAS este JSON:

        {{
        "decisao": "{decision}",
        "explicacao": "Explicação detalhada em até 150 palavras justificando por que {decision.upper()} é a decisão correta. Cite números específicos dos dados climáticos e de preços."
        }}
        """
    return prompt.strip()