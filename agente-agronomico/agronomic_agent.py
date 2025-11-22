"""
Módulo do Agente Agronômico - Núcleo de decisão do sistema

Este módulo contém funções para análise de dados climáticos, de preços e relatórios
de mercado, construção de prompts para o modelo de IA e tomada de decisão final.
"""

from typing import Dict, Any
from datetime import datetime


def analyze_climate_factors(clima: dict, tipo_cafe: str, estado_cafe: str = "", data_colheita: str = "") -> float:
    """
    Analisa fatores climáticos e retorna um score
    
    Args:
        clima: Dicionário com dados climáticos do Open-Meteo contendo:
               - daily_forecast: previsão dos próximos 14 dias
               - past_month_averages: médias históricas
        tipo_cafe: arabica ou robusta
        estado_cafe: verde, torrado ou moido
        data_colheita: Data da colheita (YYYY-MM-DD)
        
    Returns:
        Score indicando favorabilidade para venda
    """
    score = 0.5  # Score neutro
    
    if not clima or "daily_forecast" not in clima:
        return score
    
    forecast = clima.get("daily_forecast", [])
    if not forecast:
        return score
    
    # Analisa próximos 14 dias (período crítico para decisão)
    next_days = forecast[:14]
    
    # Calcula médias dos próximos 14 dias
    avg_temp_max = sum(day.get("temperature_2m_max", 20) for day in next_days) / len(next_days)
    avg_temp_min = sum(day.get("temperature_2m_min", 15) for day in next_days) / len(next_days)
    total_precipitation = sum(day.get("precipitation_sum", 0) for day in next_days)
    total_precip_hours = sum(day.get("precipitation_hours", 0) for day in next_days)
    avg_windspeed = sum(day.get("windspeed_10m_max", 10) for day in next_days) / len(next_days)
    
    # 1. Análise de temperatura (peso maior)
    # Temperatura ideal para armazenamento/transporte: 18-28°C
    tipo_cafe = tipo_cafe.lower()
    if tipo_cafe == "arabica":
        # Condições ótimas
        if 18 <= avg_temp_max <= 22 and avg_temp_min >= 13:
            score += 0.25  
        # Condições muito ruins
        elif avg_temp_max > 32 or avg_temp_min < 13:
            score -= 0.30  
        # Temperaturas fora do ideal, mas não críticas
        else:
            score -= 0.15  

    elif tipo_cafe == "robusta":
        # Condições ótimas
        if 22 <= avg_temp_max <= 28 and avg_temp_min >= 15:
            score += 0.25  
        # Condições muito ruins
        elif avg_temp_max > 35 or avg_temp_min < 15:
            score -= 0.30  
        # Temperaturas fora do ideal
        else:
            score -= 0.15  

    
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
    if total_precip_hours > 48:  # Mais de 48h de chuva em 14 dias
        score -= 0.15  # Período chuvoso prolongado
    elif total_precip_hours == 0:
        score += 0.10  # Período seco ideal
    
    # 4. Análise de vento (menor peso, mas relevante para secagem)
    if avg_windspeed > 20:  # Ventos muito fortes
        score -= 0.10  # Pode dificultar operações
    elif 10 <= avg_windspeed <= 18:
        score += 0.05  # Bom para secagem natural
    
    # 5. Análise do estado do café (impacta sensibilidade ao clima)
    if estado_cafe:
        estado_lower = estado_cafe.lower()
        if "verde" in estado_lower:
            # Café verde é mais sensível à umidade durante transporte
            if total_precipitation > 30:
                score -= 0.20  # Chuva prejudica muito café verde
            elif total_precipitation < 10:
                score += 0.15  # Clima seco ideal
        elif "torrado" in estado_lower or "moido" in estado_lower:
            # Café processado precisa proteção absoluta contra umidade
            if total_precipitation > 20:
                score -= 0.30  # Crítico: umidade degrada café torrado/moído rapidamente
            elif total_precipitation < 5:
                score += 0.20  # Excelente para transporte de processado
    
    # 6. Tempo desde a colheita (urgência aumenta com tempo)
    if data_colheita:
        try:
            
            data_colheita_dt = datetime.strptime(data_colheita, "%Y-%m-%d")
            dias_desde_colheita = (datetime.now() - data_colheita_dt).days
            
            if dias_desde_colheita > 180:  # Mais de 6 meses
                score += 0.15  # Urgência: vender logo
            elif dias_desde_colheita > 120:  # 4-6 meses
                score += 0.10
            elif dias_desde_colheita < 30:  # Menos de 1 mês
                score -= 0.05  # Pode aguardar melhor momento
        except:
            pass
    
    return max(0.0, min(1.0, score))


def analyze_price_trends(preco: dict, quantidade: float = 0, estado_cafe: str = "") -> float:
    """
    Analisa tendências de preço e retorna um score
    
    Args:
        preco: Dicionário com dados do agente de preços contendo:
               - preco_atual: preço atual
               - medias_moveis_3_dias: histórico de médias móveis
               - dias_analisados: período de análise
        quantidade: Quantidade de sacas (1-5000)
        estado_cafe: verde, torrado ou moido
        
    Returns:
        Score indicando favorabilidade para venda
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
    
    # 5. Análise da quantidade (volumes diferentes têm estratégias diferentes)
    if quantidade > 0:
        if quantidade >= 1000:  # Grande volume (1000-5000 sacas)
            # Grande volume: aproveitar preço bom, difícil vender tudo em queda
            if variacao_vs_media_5 > 0.03:
                score += 0.15  # Preço bom + volume alto = vender
            elif variacao_vs_media_5 < -0.03:
                score -= 0.10  # Preço ruim + volume alto = difícil escoar
        elif quantidade >= 500:  # Volume médio (500-999 sacas)
            if variacao_vs_media_5 > 0:
                score += 0.08  # Preço acima da média = bom momento
        elif quantidade < 100:  # Volume pequeno (1-99 sacas)
            # Pequeno volume = flexibilidade, pode aguardar melhor preço
            if tendencia > 0.05:  # Se preços subindo
                score -= 0.10  # Aguardar mais
    
    # 6. Estado do café afeta valor e urgência
    if estado_cafe:
        estado_lower = estado_cafe.lower()
        if "torrado" in estado_lower or "moido" in estado_lower:
            # Café processado: maior valor agregado mas prazo de validade menor
            score += 0.15  # Urgência para vender antes de perder qualidade
            if variacao_vs_media_3 > 0.05:  # Se preço está 5% acima
                score += 0.10  # Momento excelente
        elif "verde" in estado_lower:
            # Café verde: mais estável, pode aguardar melhor momento
            if tendencia > 0.08:  # Tendência forte de alta
                score -= 0.08  # Pode esperar valorizar mais
    
    return max(0.0, min(1.0, score))


def analyze_market_reports(relatorios: list, estado_cafe: str = "", tipo_cafe: str = "") -> float:
    """
    Analisa relatórios de mercado via RAG e retorna um score
    
    Args:
        relatorios: Lista de relatórios do RAG
        estado_cafe: verde, torrado ou moido
        tipo_cafe: arabica ou robusta
        
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
    
    # Análise específica por estado do café
    if estado_cafe:
        estado_lower = estado_cafe.lower()
        if "torrado" in estado_lower or "moido" in estado_lower:
                # Relatórios sobre café processado são relevantes
                if positive_count > negative_count:
                    score += 0.10
        if "verde" in all_text or "cru" in all_text:
            if "verde" in estado_lower:
                # Relatórios sobre café verde/cru
                if positive_count > negative_count:
                    score += 0.10
    
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
        - **Score Final: {decision_score:.3f}** → Limiar: 0.5 para VENDER

        ---

        ### DADOS QUE FUNDAMENTARAM A DECISÃO

        **DADOS CLIMÁTICOS (próximos 14 dias):**
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
        1. Como as condições climáticas dos próximos 14 dias influenciam
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