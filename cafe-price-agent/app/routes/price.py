from fastapi import APIRouter, HTTPException
import os
from app.services.scraper import baixar_cepea, ler_xls_para_csv
from app.services.processor import processar_dados
from app.utils.calc import calcular_medias_moveis

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
    if tipo_cafe not in ["arabica", "robusta"]:
        raise HTTPException(status_code=400, detail="Tipo de café deve ser 'arabica' ou 'robusta'")
    
    nome_xls = None
    nome_csv = f"cepea_dados_{tipo_cafe}.csv"
    
    try:
        
        nome_xls = baixar_cepea(tipo_cafe)
        ler_xls_para_csv(nome_xls, nome_csv)

        dados_processados = processar_dados(nome_csv)

        if not dados_processados:
            raise HTTPException(status_code=404, detail="Nenhum dado encontrado para o período")

        dados_90_dias = dados_processados[:90]

        medias = calcular_medias_moveis(dados_90_dias)

        resposta = {
            "tipo_cafe": tipo_cafe,
            "dias_analisados": len(dados_90_dias),
            "data_mais_recente": dados_90_dias[0]['data'].strftime('%d/%m/%Y'),
            "preco_atual": dados_90_dias[0]['preco'],
            "medias_moveis_3_dias": medias
        }
        
        return resposta 
        
    except Exception as e:

        raise HTTPException(status_code=500, detail=f"Erro no processamento: {str(e)}")
    
    finally:

        try:

            if nome_xls and os.path.exists(nome_xls):
                os.remove(nome_xls)

            if nome_csv and os.path.exists(nome_csv):
                os.remove(nome_csv)
        except Exception as e:
            print(f"Aviso: Erro na limpeza dos arquivos: {e}")
