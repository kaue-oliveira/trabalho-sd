"""
Módulo do Agente Agronômico - Núcleo de decisão do sistema

Este módulo contém funções para análise de dados climáticos, de preços e relatórios
de mercado, construção de prompts para o modelo de IA e tomada de decisão final.
"""

from typing import Dict, Any, List, Sequence
from datetime import datetime


def _safe_mean(values: Sequence[float], default: float = 0.0) -> float:
    """Calcula média de forma segura, evitando divisão por zero."""
    values = [v for v in values if v is not None]
    return sum(values) / len(values) if values else default


def analyze_climate_factors(
    clima: Dict[str, Any],
    tipo_cafe: str,
    estado_cafe: str = "",
    data_colheita: str = "",
) -> float:
    """
    Analisa fatores climáticos e retorna um score de favorabilidade para venda.
    """
    score = 0.5  # Score neutro
    
    if not clima or "daily_forecast" not in clima:
        raise ValueError("Dados climáticos inválidos: 'daily_forecast' não encontrado")
    
    forecast = clima["daily_forecast"]
    if not forecast:
        raise ValueError("Dados climáticos inválidos: 'daily_forecast' está vazio")
    
    # Analisa próximos 14 dias (período crítico para decisão)
    next_days = forecast[:14]
    if not next_days:
        raise ValueError("Dados climáticos inválidos: menos de 1 dia disponível")
    
    # Calcula médias/valores agregados dos próximos 14 dias
    avg_temp_max = _safe_mean([day.get("temperature_2m_max", 20.0) for day in next_days], 20.0)
    avg_temp_min = _safe_mean([day.get("temperature_2m_min", 15.0) for day in next_days], 15.0)
    total_precipitation = sum(day.get("precipitation_sum", 0.0) for day in next_days)
    total_precip_hours = sum(day.get("precipitation_hours", 0.0) for day in next_days)
    avg_windspeed = _safe_mean([day.get("windspeed_10m_max", 10.0) for day in next_days], 10.0)
    
    tipo_cafe = tipo_cafe.lower()
    
    # 1. Análise de temperatura
    if tipo_cafe == "arabica":
        if 18 <= avg_temp_max <= 22 and avg_temp_min >= 13:
            score += 0.25
        elif avg_temp_max > 32 or avg_temp_min < 13:
            score -= 0.30
        else:
            score -= 0.15

    elif tipo_cafe == "robusta":
        if 22 <= avg_temp_max <= 28 and avg_temp_min >= 15:
            score += 0.25
        elif avg_temp_max > 35 or avg_temp_min < 15:
            score -= 0.30
        else:
            score -= 0.15

    # 2. Análise de precipitação (logística)
    if total_precipitation < 10:
        score += 0.30
    elif total_precipitation < 30:
        score += 0.10
    elif total_precipitation > 80:
        score -= 0.35
    elif total_precipitation > 50:
        score -= 0.20
    
    # 3. Análise de horas de chuva
    if total_precip_hours > 48:
        score -= 0.15
    elif total_precip_hours == 0:
        score += 0.10
    
    # 4. Análise de vento
    if avg_windspeed > 20:
        score -= 0.10
    elif 10 <= avg_windspeed <= 18:
        score += 0.05
    
    # 5. Estado do café
    if estado_cafe:
        estado_lower = estado_cafe.lower()
        if "verde" in estado_lower:
            if total_precipitation > 30:
                score -= 0.20
            elif total_precipitation < 10:
                score += 0.15
        elif "torrado" in estado_lower or "moido" in estado_lower:
            if total_precipitation > 20:
                score -= 0.30
            elif total_precipitation < 5:
                score += 0.20
    
    # 6. Tempo desde a colheita
    if data_colheita:
        try:
            data_colheita_dt = datetime.strptime(data_colheita, "%Y-%m-%d")
            dias_desde_colheita = (datetime.now() - data_colheita_dt).days
            
            if dias_desde_colheita > 180:
                score += 0.15
            elif dias_desde_colheita > 120:
                score += 0.10
            elif dias_desde_colheita < 30:
                score -= 0.05
        except Exception:
            # Caso a data venha em formato inesperado, simplesmente ignora
            pass
    
    return max(0.0, min(1.0, score))


def analyze_price_trends(
    preco: Dict[str, Any],
    quantidade: float = 0,
    estado_cafe: str = "",
) -> float:
    """
    Analisa tendências de preço e retorna um score de favorabilidade para venda.
    """
    score = 0.5
    
    if not preco or "preco_atual" not in preco:
        raise ValueError("Dados de preço inválidos: 'preco_atual' não encontrado")
    
    preco_atual = preco.get("preco_atual", 0.0)
    medias_moveis = preco.get("medias_moveis_3_dias", [])
    desvio_padrao = preco.get("desvio_padrao")
    
    if preco_atual <= 0 or not medias_moveis:
        raise ValueError("Dados de preço inválidos: 'medias_moveis_3_dias' ou 'preco_atual' não encontrados")
    
    recent_averages: List[float] = [
        m.get("media", 0.0) for m in medias_moveis if m.get("media") is not None
    ]
    
    if len(recent_averages) < 3:
        raise ValueError("Dados de preço inválidos: 'medias_moveis_3_dias' insuficientes para análise")
    
    # Médias em diferentes janelas
    media_geral = _safe_mean(recent_averages, preco_atual)
    media_ultimos_30 = _safe_mean(recent_averages[-30:], media_geral)
    media_ultimos_15 = _safe_mean(recent_averages[-15:], media_geral)
    media_ultimos_7 = _safe_mean(recent_averages[-7:], media_geral)
    
    if media_geral == 0:
        # Evita divisão por zero; se isso acontecer algo está muito incoerente nos dados
        return max(0.0, min(1.0, score))
    
    # 1. Comparação do preço atual com médias
    variacao_vs_media_geral = (preco_atual - media_geral) / media_geral
    variacao_vs_media_30 = (preco_atual - media_ultimos_30) / media_ultimos_30 if media_ultimos_30 else 0
    variacao_vs_media_15 = (preco_atual - media_ultimos_15) / media_ultimos_15 if media_ultimos_15 else 0
    variacao_vs_media_7 = (preco_atual - media_ultimos_7) / media_ultimos_7 if media_ultimos_7 else 0
    
    if variacao_vs_media_geral > 0.05:
        score += 0.20
    elif variacao_vs_media_geral < -0.05:
        score -= 0.15
    
    if variacao_vs_media_30 > 0.03:
        score += 0.15
    elif variacao_vs_media_30 < -0.03:
        score -= 0.10
    
    # 2. Tendência de longo prazo (90 dias -> compara 30 iniciais com 30 finais)
    if len(recent_averages) >= 60:
        media_primeiro_mes = _safe_mean(recent_averages[:30])
        media_ultimo_mes = _safe_mean(recent_averages[-30:])
        
        if media_primeiro_mes:
            tendencia_longo_prazo = (media_ultimo_mes - media_primeiro_mes) / media_primeiro_mes
        else:
            tendencia_longo_prazo = 0
        
        if tendencia_longo_prazo > 0.15:
            score -= 0.20
        elif tendencia_longo_prazo < -0.15:
            score += 0.30
        elif -0.08 < tendencia_longo_prazo < 0.08:
            score += 0.05
    
    # Tendência de curto prazo (últimos 15 dias)
    if len(recent_averages) >= 15:
        base_curto = _safe_mean(recent_averages[-15:-8], media_ultimos_7)
        if base_curto:
            tendencia_curto_prazo = (media_ultimos_7 - base_curto) / base_curto
        else:
            tendencia_curto_prazo = 0
        
        if tendencia_curto_prazo > 0.10:
            score -= 0.15
        elif tendencia_curto_prazo < -0.10:
            score += 0.25
    
    # 3. Volatilidade (últimos 30 dias)
    if len(recent_averages) >= 30:
        janela_30 = recent_averages[-30:]
        volatilidade = max(janela_30) - min(janela_30)
        volatilidade_percentual = volatilidade / media_ultimos_30 if media_ultimos_30 else 0
        
        if volatilidade_percentual > 0.20:
            if variacao_vs_media_7 > 0:
                score += 0.15
            else:
                score -= 0.10
        elif volatilidade_percentual < 0.08 and variacao_vs_media_30 > 0.05:
            score += 0.10
    
    # 4. Momentum de curto prazo (últimos 7 dias)
    if len(recent_averages) >= 7:
        diff_recente = recent_averages[-1] - recent_averages[-4]
        diff_anterior = recent_averages[-4] - recent_averages[-7]
        
        if diff_recente > 0 and diff_anterior > 0 and diff_recente > diff_anterior * 1.2:
            score -= 0.10
        elif diff_recente < 0 and diff_anterior < 0 and abs(diff_recente) > abs(diff_anterior) * 1.2:
            score += 0.15
    
    # 5. Análise baseada no desvio padrão
    if desvio_padrao is not None and desvio_padrao > 0:
        z_score = (preco_atual - media_geral) / desvio_padrao
        
        if z_score > 1.5:
            score += 0.20
        elif z_score > 1.0:
            score += 0.15
        elif z_score < -1.5:
            score -= 0.20
        elif z_score < -1.0:
            score -= 0.15
        
        coeficiente_variacao = desvio_padrao / media_geral
        
        if coeficiente_variacao > 0.15 and z_score > 0.5:
            score += 0.10
        elif coeficiente_variacao < 0.05 and variacao_vs_media_30 > 0.02:
            score += 0.08
    
    # 6. Análise da quantidade
    if quantidade > 0:
        if quantidade >= 1000:
            if variacao_vs_media_30 > 0.03:
                score += 0.15
            elif variacao_vs_media_30 < -0.03:
                score -= 0.10
        elif quantidade >= 500:
            if variacao_vs_media_30 > 0:
                score += 0.08
        elif quantidade < 100 and len(recent_averages) >= 60:
            media_primeiro_mes = _safe_mean(recent_averages[:30])
            media_ultimo_mes = _safe_mean(recent_averages[-30:])
            if media_primeiro_mes:
                tendencia_geral = (media_ultimo_mes - media_primeiro_mes) / media_primeiro_mes
            else:
                tendencia_geral = 0
            if tendencia_geral > 0.05:
                score -= 0.10
    
    # 7. Estado do café
    if estado_cafe:
        estado_lower = estado_cafe.lower()
        if "torrado" in estado_lower or "moido" in estado_lower:
            score += 0.15
            if variacao_vs_media_7 > 0.05:
                score += 0.10
        elif "verde" in estado_lower and len(recent_averages) >= 30:
            media_15_dias_atras = _safe_mean(recent_averages[-30:-15])
            media_ultimos_15_dias = _safe_mean(recent_averages[-15:])
            if media_15_dias_atras:
                tendencia_recente = (media_ultimos_15_dias - media_15_dias_atras) / media_15_dias_atras
            else:
                tendencia_recente = 0
            if tendencia_recente > 0.08:
                score -= 0.08
    
    return max(0.0, min(1.0, score))


def analyze_market_reports(
    relatorios: List[Dict[str, Any]],
    estado_cafe: str = "",
    tipo_cafe: str = "",
) -> float:
    """
    Analisa relatórios de mercado via RAG e retorna um score.
    """
    score = 0.5
    
    if not relatorios:
        return score
    
    positive_keywords = ["vender", "alta", "crescimento", "valorização", "positivo", "boa", "favorável"]
    negative_keywords = ["aguardar", "queda", "baixa", "desvalorização", "negativo", "risco", "desfavorável"]
    
    all_text = " ".join(
        f"{rel.get('content', '')} {rel.get('metadata', {})}"
        for rel in relatorios
    ).lower()
    
    positive_count = sum(1 for keyword in positive_keywords if keyword in all_text)
    negative_count = sum(1 for keyword in negative_keywords if keyword in all_text)
    
    if positive_count > negative_count:
        score += 0.3
    elif negative_count > positive_count:
        score -= 0.3
    
    if estado_cafe:
        estado_lower = estado_cafe.lower()
        if "torrado" in estado_lower or "moido" in estado_lower:
            if positive_count > negative_count:
                score += 0.10
        if "verde" in all_text or "cru" in all_text:
            if "verde" in estado_lower and positive_count > negative_count:
                score += 0.10
    
    return max(0.0, min(1.0, score))


def calculate_decision_score(
    climate_score: float,
    price_score: float,
    market_score: float,
) -> float:
    """
    Calcula score final da decisão baseado nos pesos definidos.
    """
    decision_weights = {
        "climate": 0.35,
        "price_trend": 0.40,
        "market_reports": 0.25,
    }
    
    total_score = (
        climate_score * decision_weights["climate"]
        + price_score * decision_weights["price_trend"]
        + market_score * decision_weights["market_reports"]
    )
    return round(total_score, 3)


def build_ai_prompt(
    payload: Dict[str, Any],
    clima: Dict[str, Any],
    preco: Dict[str, Any],
    relatorios: List[Dict[str, Any]],
    climate_score: float,
    price_score: float,
    market_score: float,
    decision_score: float,
    decision: str,
) -> str:
    """
    Constrói prompt para explicação da decisão tomada pelo agente.
    Foco principal em dados climáticos e de preço, relatórios como contexto auxiliar.
    """
    tipo_cafe = payload.get("tipo_cafe", "")
    cidade = payload.get("cidade", "")
    estado = payload.get("estado", "")
    data_colheita = payload.get("data_colheita", "")
    quantidade = payload.get("quantidade", 0)
    estado_cafe = payload.get("estado_cafe", "")
    
    # Extrair dados climáticos relevantes
    forecast = clima.get("daily_forecast", [])
    next_days = forecast[:14] if forecast else []
    
    # Calcular métricas climáticas detalhadas
    if next_days:
        temps_max = [day.get("temperature_2m_max", 0) for day in next_days]
        temps_min = [day.get("temperature_2m_min", 0) for day in next_days]
        precips = [day.get("precipitation_sum", 0) for day in next_days]
        winds = [day.get("windspeed_10m_max", 0) for day in next_days]
        precip_hours = [day.get("precipitation_hours", 0) for day in next_days]
        
        # Métricas gerais dos 14 dias
        avg_temp_max = sum(temps_max) / len(temps_max) if temps_max else 0
        avg_temp_min = sum(temps_min) / len(temps_min) if temps_min else 0
        total_precip = sum(precips)
        avg_wind = sum(winds) / len(winds) if winds else 0
        precip_days = sum(1 for p in precips if p > 0)
        total_precip_hours = sum(precip_hours)
        
        # Dados dos últimos 7 dias (mais relevantes)
        last_7_days = next_days[:7]
        temps_max_7 = [day.get("temperature_2m_max", 0) for day in last_7_days]
        temps_min_7 = [day.get("temperature_2m_min", 0) for day in last_7_days]
        precips_7 = [day.get("precipitation_sum", 0) for day in last_7_days]
        
        avg_temp_max_7 = sum(temps_max_7) / len(temps_max_7) if temps_max_7 else 0
        avg_temp_min_7 = sum(temps_min_7) / len(temps_min_7) if temps_min_7 else 0
        total_precip_7 = sum(precips_7)
        precip_days_7 = sum(1 for p in precips_7 if p > 0)
        
        # Variação térmica
        variacao_termica = avg_temp_max - avg_temp_min
        variacao_termica_7 = avg_temp_max_7 - avg_temp_min_7
        
        # Dias críticos (chuva intensa ou calor extremo)
        dias_chuva_intensa = sum(1 for p in precips if p > 10)
        dias_calor_extremo = sum(1 for t in temps_max if t > 30)
    else:
        avg_temp_max = avg_temp_min = total_precip = avg_wind = precip_days = 0
        avg_temp_max_7 = avg_temp_min_7 = total_precip_7 = precip_days_7 = 0
        variacao_termica = variacao_termica_7 = 0
        dias_chuva_intensa = dias_calor_extremo = 0
        total_precip_hours = 0
    
    # Extrair dados de preço relevantes
    preco_atual = preco.get("preco_atual", 0)
    medias_moveis = preco.get("medias_moveis_3_dias", [])
    desvios_padrao = preco.get("desvio_padrao_10_dias", [])
    
    # Calcular métricas de preço detalhadas
    if medias_moveis:
        # Valores das médias móveis
        valores_medias = [m.get("media", 0) for m in medias_moveis]
        
        # Tendência de curto prazo (últimas 3 médias)
        if len(valores_medias) >= 3:
            media_recente = valores_medias[-1]
            media_anterior = valores_medias[-2]
            media_antiga = valores_medias[-3]
            
            tendencia_curta = "alta" if media_recente > media_anterior else "baixa" if media_recente < media_anterior else "estável"
            variacao_curta = ((media_recente - media_anterior) / media_anterior * 100) if media_anterior else 0
            
            # Tendência de médio prazo (últimas 5 médias)
            if len(valores_medias) >= 5:
                media_5_periodos = sum(valores_medias[-5:]) / 5
                media_10_periodos = sum(valores_medias[-10:]) / 10 if len(valores_medias) >= 10 else media_5_periodos
                tendencia_media = "alta" if media_5_periodos > media_10_periodos else "baixa" if media_5_periodos < media_10_periodos else "estável"
            else:
                tendencia_media = "indeterminada"
                media_5_periodos = media_recente
        else:
            tendencia_curta = tendencia_media = "indeterminada"
            variacao_curta = 0
            media_5_periodos = preco_atual
        
        # Volatilidade (desvio padrão)
        if desvios_padrao:
            ultimo_desvio = desvios_padrao[-1].get("desvio_padrao", 0) if desvios_padrao else 0
            avg_desvio = sum(d.get("desvio_padrao", 0) for d in desvios_padrao) / len(desvios_padrao) if desvios_padrao else 0
        else:
            ultimo_desvio = avg_desvio = 0
        
        # Comparação com média histórica
        media_geral = sum(valores_medias) / len(valores_medias) if valores_medias else preco_atual
        variacao_vs_media = ((preco_atual - media_geral) / media_geral * 100) if media_geral else 0
    else:
        tendencia_curta = tendencia_media = "indeterminada"
        variacao_curta = variacao_vs_media = 0
        media_5_periodos = preco_atual
        ultimo_desvio = avg_desvio = 0
        media_geral = preco_atual
    
    # Extrair insights relevantes dos relatórios (apenas se muito relevantes)
    insights_relatorios = []
    if relatorios:
        for rel in relatorios[:2]:  # Limitar a 2 relatórios mais relevantes
            content = rel.get("content", "")
            # Buscar menções específicas ao tipo de café ou região
            if tipo_cafe.lower() in content.lower() or estado.lower() in content.lower():
                insights_relatorios.append(content[:150] + "...")  # Limitar tamanho
    
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

        ### DADOS CLIMÁTICOS DETALHADOS (Próximos 14 dias - {cidade}, {estado})

        **VISÃO GERAL (14 dias):**
        - Temperatura máxima média: {avg_temp_max:.1f}°C
        - Temperatura mínima média: {avg_temp_min:.1f}°C  
        - Variação térmica diária: {variacao_termica:.1f}°C
        - Precipitação total: {total_precip:.1f}mm
        - Dias com chuva: {precip_days} dias
        - Horas de precipitação: {total_precip_hours:.1f}h
        - Velocidade média do vento: {avg_wind:.1f}km/h
        - Dias com chuva intensa (>10mm): {dias_chuva_intensa}
        - Dias com calor extremo (>30°C): {dias_calor_extremo}

        **PRÓXIMOS 7 DIAS (Período Crítico):**
        - Temp. máxima: {avg_temp_max_7:.1f}°C | Temp. mínima: {avg_temp_min_7:.1f}°C
        - Precipitação: {total_precip_7:.1f}mm em {precip_days_7} dias
        - Variação térmica: {variacao_termica_7:.1f}°C

        ### ANÁLISE DE PREÇOS DETALHADA ({tipo_cafe.title()})

        **PREÇOS ATUAIS:**
        - Preço atual: R$ {preco_atual:.2f}
        - Média geral (90 dias): R$ {media_geral:.2f}
        - Variação vs média: {variacao_vs_media:+.1f}%

        **TENDÊNCIAS:**
        - Curto prazo (últimos períodos): {tendencia_curta} ({variacao_curta:+.1f}%)
        - Médio prazo: {tendencia_media}
        - Média últimos 5 períodos: R$ {media_5_periodos:.2f}

        **VOLATILIDADE:**
        - Desvio padrão recente: R$ {ultimo_desvio:.2f}
        - Desvio padrão médio: R$ {avg_desvio:.2f}
        - Períodos analisados: {len(medias_moveis)} médias móveis

        **INFORMAÇÕES DO CAFÉ:**
        - Tipo: {tipo_cafe}
        - Estado: {estado_cafe}
        - Quantidade: {quantidade} sacas
        - Data de colheita: {data_colheita}

        **CONTEXTO ADICIONAL (Relatórios):**
        {'- ' + ' | '.join(insights_relatorios) if insights_relatorios else 'Nenhum insight relevante dos relatórios para esta decisão específica.'}

        ---

        Sua tarefa é explicar por que a decisão de **{decision.upper()}** é apropriada BASEANDO-SE PRINCIPALMENTE NOS DADOS CLIMÁTICOS E DE PREÇO.

        **FOCO PRINCIPAL (80% da explicação):**
        1. **Análise Climática Detalhada**: 
           - Como as condições dos próximos 7-14 dias afetam qualidade, secagem, logística
           - Impacto das temperaturas, chuva e vento no café {estado_cafe}
           - Risco de dias críticos (chuva intensa/calor extremo)

        2. **Análise de Preços Avançada**:
           - Significado da tendência {tendencia_curta} e variação de {variacao_curta:+.1f}%
           - Posicionamento do preço atual vs histórico (R$ {preco_atual:.2f} vs R$ {media_geral:.2f})
           - Impacto da volatilidade (desvio R$ {ultimo_desvio:.2f})

        **CONTEXTO SECUNDÁRIO (20% da explicação):**
        3. **Considerações Complementares**: Apenas se muito relevante, mencione brevemente insights dos relatórios

        Seja ESPECÍFICO com números: 
        - Cite temperaturas exatas ({avg_temp_max_7:.1f}°C/{avg_temp_min_7:.1f}°C)
        - Precipitação concreta ({total_precip_7:.1f}mm)
        - Preços precisos (R$ {preco_atual:.2f})
        - Variações percentuais ({variacao_vs_media:+.1f}%)

        Responda APENAS este JSON:

        {{
        "decisao": "{decision}",
        "explicacao": "Explicação técnica em 150-180 palavras focando 80% em clima e preço. Use números específicos: temp {avg_temp_max_7:.1f}°C, precip {total_precip_7:.1f}mm, preço R$ {preco_atual:.2f}, variação {variacao_vs_media:+.1f}%, tendência {tendencia_curta}."
        }}
        """
    return prompt.strip()
