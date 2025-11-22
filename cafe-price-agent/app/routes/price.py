from fastapi import APIRouter, HTTPException
import os
from app.services.scraper import baixar_cepea, ler_xls_para_csv
from app.services.processor import processar_dados
from app.utils.calc import calcular_medias_moveis

# Cria roteador FastAPI para agrupar endpoints relacionados a preços
router = APIRouter()

@router.get("/preco/{tipo_cafe}")
async def obter_preco_cafe(tipo_cafe: str):
    """
    Endpoint REST para obter preços atualizados e médias móveis do café.
    
    Args:
        tipo_cafe (str): Tipo de café ('arabica' ou 'robusta')
        
    Returns:
        dict: Dicionário contendo:
            - tipo_cafe: Tipo consultado
            - data_mais_recente: Data do último preço disponível
            - preco_atual: Preço mais recente
            - medias_moveis_3_dias: Lista de médias móveis calculadas
            
    Raises:
        HTTPException: 400 para tipo inválido, 404 para dados não encontrados,
                      500 para erros internos
    """
    # Validação do parâmetro de entrada
    if tipo_cafe not in ["arabica", "robusta"]:
        raise HTTPException(status_code=400, detail="Tipo de café deve ser 'arabica' ou 'robusta'")
    
    nome_xls = None  # Variável para controle do arquivo XLS temporário
    nome_csv = f"cepea_dados_{tipo_cafe}.csv"  # Nome único do CSV por tipo
    
    try:
        # FASE 1: Download e conversão de dados
        # Baixa planilha XLS do site CEPEA (120 dias para garantir 90 úteis)
        nome_xls = baixar_cepea(tipo_cafe)
        # Converte XLS para CSV formatado
        ler_xls_para_csv(nome_xls, nome_csv)
        
        # FASE 2: Processamento dos dados
        # Processa CSV e converte para estrutura interna
        dados_processados = processar_dados(nome_csv)
        
        # Verifica se existem dados processados
        if not dados_processados:
            raise HTTPException(status_code=404, detail="Nenhum dado encontrado para o período")
        
        # FASE 3: Filtro temporal
        # Seleciona apenas os 90 registros mais recentes (já ordenados)
        dados_90_dias = dados_processados[:90]
        
        # FASE 4: Cálculo estatístico
        # Calcula médias móveis de 3 em 3 dias
        medias = calcular_medias_moveis(dados_90_dias)
        
        # FASE 5: Formatação da resposta
        resposta = {
            "tipo_cafe": tipo_cafe,
            "dias_analisados": len(dados_90_dias),  # Quantidade real de dias processados
            "data_mais_recente": dados_90_dias[0]['data'].strftime('%d/%m/%Y'),  # Formata data
            "preco_atual": dados_90_dias[0]['preco'],  # Preço do dia mais recente
            "medias_moveis_3_dias": medias  # Lista de médias calculadas
        }
        
        return resposta  # Retorna resposta formatada como JSON
        
    except Exception as e:
        # Tratamento genérico de exceções - captura qualquer erro não tratado
        raise HTTPException(status_code=500, detail=f"Erro no processamento: {str(e)}")
    
    finally:
        # FASE 6: Limpeza de recursos
        # Garante que arquivos temporários sejam removidos mesmo em caso de erro
        try:
            # Remove arquivo XLS se existir
            if nome_xls and os.path.exists(nome_xls):
                os.remove(nome_xls)
            # Remove arquivo CSV se existir
            if nome_csv and os.path.exists(nome_csv):
                os.remove(nome_csv)
        except Exception as e:
            # Log silencioso - erro na limpeza não afeta resposta principal
            print(f"Aviso: Erro na limpeza dos arquivos: {e}")
