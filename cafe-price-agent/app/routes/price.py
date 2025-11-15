from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.services.scraper import scrape_price
from app.services.dataservice import salvar_preco, buscar_historico
from app.utils.calc import gerar_medias_3em3
import json

router = APIRouter(prefix="/price", tags=["Price Agent"])

@router.post("/update/{tipo_cafe}")
async def update_price_and_stats(tipo_cafe: str, background_tasks: BackgroundTasks):
    """
    1) faz scraping para pegar o preço mais atual;
    2) salva o preço no DataService (via gateway);
    3) busca 90 dias de histórico do DataService;
    4) calcula as 30 médias (3 em 3 dias);
    5) retorna o JSON no formato pedido.
    """
    print(f" INICIANDO REQUISIÇÃO PARA: {tipo_cafe}")
    
    tipo = tipo_cafe.lower()
    if tipo not in ("arabica", "robusta"):
        raise HTTPException(400, "Tipo deve ser 'arabica' ou 'robusta'")

    # 1) Scraping
    print("1. Fazendo scraping...")
    preco_info = scrape_price(tipo)
    if not preco_info:
        raise HTTPException(404, "Preço não encontrado via scraping")
    print(f"Scraping OK: {preco_info}")

    # 2) Salvar no DataService
    print("2. Salvando preço no DataService...")
    try:
        await salvar_preco(tipo, preco_info)
        print("Preço salvo com sucesso")
    except HTTPException as e:
        print(f"Erro ao salvar preço: {e.detail}")
        # Se for erro de duplicata, continuamos (é esperado)
        if "Já existe um preço registrado para esta data" not in str(e.detail):
            raise

    # 3) Buscar histórico
    print("3. Buscando histórico...")
    try:
        historico = await buscar_historico(tipo)
        print(f" Histórico obtido: {len(historico)} registros")
    except HTTPException as e:
        print(f" Erro ao buscar histórico: {e.detail}")
        raise HTTPException(e.status_code, f"Erro ao buscar histórico: {e.detail}")

    # 4) Processar histórico
    print(" 4. Processando histórico...")
    historico_norm = []
    for item in historico:
        if isinstance(item, dict):
            d = item.get("data") or item.get("price_date")
            p = item.get("preco") or item.get("price")
        else:
            continue
            
        if d and p is not None:
            historico_norm.append({"data": d, "preco": float(p)})
    
    # Ordenar por data decrescente
    historico_norm.sort(key=lambda x: x["data"], reverse=True)
    print(f" Histórico normalizado: {len(historico_norm)} registros")

    # 5) Calcular médias
    print(" 5. Calculando médias...")
    medias_3em3 = gerar_medias_3em3(historico_norm)
    print(f"   Médias calculadas: {len(medias_3em3)} valores")

    # 6) Montar resposta
    print(" 6. Montando resposta final...")
    resposta = {
        "tipo": tipo,
        "data": preco_info["data"],
        "preco": preco_info["preco"],
        "medias_3em3dias": medias_3em3
    }

    # PRINT DO JSON NO TERMINAL 
    print("\n" + "="*60)
    print("🎯 JSON RETORNADO PELO AGENTE:")
    print("="*60)
    print(json.dumps(resposta, indent=2, ensure_ascii=False))
    print("="*60)
    print(f"✅ Tipo: {resposta['tipo']}")
    print(f"✅ Data: {resposta['data']}")
    print(f"✅ Preço: R$ {resposta['preco']:,.2f}")
    print(f"✅ Médias 3em3: {len(resposta['medias_3em3dias'])} valores")
    print("="*60)

    return resposta