from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.database import get_db
from app.models.schemas import (
    ArabicaPriceResponse, ArabicaPriceCreate, ArabicaPriceUpdate,
    RobustaPriceResponse, RobustaPriceCreate, RobustaPriceUpdate
)
from app.crud import precos as crud_precos

# Aliases para compatibilidade
ArabicaPrice = ArabicaPriceResponse
RobustaPrice = RobustaPriceResponse

router = APIRouter(prefix="/precos", tags=["precos"])

# Rotas para Arabica
@router.post("/arabica/", response_model=ArabicaPrice)
def criar_arabica_price(arabica_price: ArabicaPriceCreate, db: Session = Depends(get_db)):
    # Verificar se já existe preço para esta data
    existing_price = crud_precos.obter_arabica_price_por_data(db, price_date=arabica_price.price_date)
    if existing_price:
        raise HTTPException(status_code=400, detail="Já existe um preço registrado para esta data")
    return crud_precos.criar_arabica_price(db=db, arabica_price=arabica_price)

@router.get("/arabica/{price_id}", response_model=ArabicaPrice)
def ler_arabica_price(price_id: int, db: Session = Depends(get_db)):
    db_price = crud_precos.obter_arabica_price_por_id(db, arabica_price_id=price_id)
    if db_price is None:
        raise HTTPException(status_code=404, detail="Preço do Arábica não encontrado")
    return db_price

@router.get("/arabica/", response_model=List[ArabicaPrice])
def listar_arabica_prices(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    return crud_precos.listar_arabica_prices(db, skip=skip, limit=limit)

@router.get("/arabica/data/{price_date}", response_model=ArabicaPrice)
def ler_arabica_price_por_data(price_date: date, db: Session = Depends(get_db)):
    db_price = crud_precos.obter_arabica_price_por_data(db, price_date=price_date)
    if db_price is None:
        raise HTTPException(status_code=404, detail="Preço do Arábica para esta data não encontrado")
    return db_price

@router.get("/arabica/ultimo/", response_model=ArabicaPrice)
def obter_ultimo_preco_arabica(db: Session = Depends(get_db)):
    db_price = crud_precos.obter_ultimo_preco_arabica(db)
    if db_price is None:
        raise HTTPException(status_code=404, detail="Nenhum preço do Arábica encontrado")
    return db_price

# @router.put("/arabica/{price_id}", response_model=ArabicaPrice)
# def atualizar_arabica_price(
#     price_id: int, 
#     arabica_price_update: ArabicaPriceUpdate, 
#     db: Session = Depends(get_db)
# ):
#     db_price = crud_precos.atualizar_arabica_price(db, arabica_price_id=price_id, arabica_price_update=arabica_price_update)
#     if db_price is None:
#         raise HTTPException(status_code=404, detail="Preço do Arábica não encontrado")
#     return db_price

@router.delete("/arabica/{price_id}")
def deletar_arabica_price(price_id: int, db: Session = Depends(get_db)):
    db_price = crud_precos.deletar_arabica_price(db, arabica_price_id=price_id)
    if db_price is None:
        raise HTTPException(status_code=404, detail="Preço do Arábica não encontrado")
    return {"message": "Preço do Arábica deletado com sucesso"}

# Rotas para Robusta
@router.post("/robusta/", response_model=RobustaPrice)
def criar_robusta_price(robusta_price: RobustaPriceCreate, db: Session = Depends(get_db)):
    existing_price = crud_precos.obter_robusta_price_por_data(db, price_date=robusta_price.price_date)
    if existing_price:
        raise HTTPException(status_code=400, detail="Já existe um preço registrado para esta data")
    return crud_precos.criar_robusta_price(db=db, robusta_price=robusta_price)

@router.get("/robusta/{price_id}", response_model=RobustaPrice)
def ler_robusta_price(price_id: int, db: Session = Depends(get_db)):
    db_price = crud_precos.obter_robusta_price_por_id(db, robusta_price_id=price_id)
    if db_price is None:
        raise HTTPException(status_code=404, detail="Preço do Robusta não encontrado")
    return db_price

@router.get("/robusta/", response_model=List[RobustaPrice])
def listar_robusta_prices(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    return crud_precos.listar_robusta_prices(db, skip=skip, limit=limit)

@router.get("/robusta/data/{price_date}", response_model=RobustaPrice)
def ler_robusta_price_por_data(price_date: date, db: Session = Depends(get_db)):
    db_price = crud_precos.obter_robusta_price_por_data(db, price_date=price_date)
    if db_price is None:
        raise HTTPException(status_code=404, detail="Preço do Robusta para esta data não encontrado")
    return db_price

@router.get("/robusta/ultimo/", response_model=RobustaPrice)
def obter_ultimo_preco_robusta(db: Session = Depends(get_db)):
    db_price = crud_precos.obter_ultimo_preco_robusta(db)
    if db_price is None:
        raise HTTPException(status_code=404, detail="Nenhum preço do Robusta encontrado")
    return db_price

# @router.put("/robusta/{price_id}", response_model=RobustaPrice)
# def atualizar_robusta_price(
#     price_id: int, 
#     robusta_price_update: RobustaPriceUpdate, 
#     db: Session = Depends(get_db)
# ):
#     db_price = crud_precos.atualizar_robusta_price(db, robusta_price_id=price_id, robusta_price_update=robusta_price_update)
#     if db_price is None:
#         raise HTTPException(status_code=404, detail="Preço do Robusta não encontrado")
#     return db_price

@router.delete("/robusta/{price_id}")
def deletar_robusta_price(price_id: int, db: Session = Depends(get_db)):
    db_price = crud_precos.deletar_robusta_price(db, robusta_price_id=price_id)
    if db_price is None:
        raise HTTPException(status_code=404, detail="Preço do Robusta não encontrado")
    return {"message": "Preço do Robusta deletado com sucesso"}

# DELETE do preço mais antigo
@router.delete("/arabica/antigo/")
def deletar_preco_mais_antigo_arabica(db: Session = Depends(get_db)):
    preco_deletado = crud_precos.deletar_preco_mais_antigo_arabica(db)
    if preco_deletado is None:
        raise HTTPException(status_code=404, detail="Nenhum preço do Arábica encontrado para deletar")
    return {"message": f"Preço mais antigo do Arábica (data: {preco_deletado.price_date}) deletado com sucesso"}

@router.delete("/robusta/antigo/")
def deletar_preco_mais_antigo_robusta(db: Session = Depends(get_db)):
    preco_deletado = crud_precos.deletar_preco_mais_antigo_robusta(db)
    if preco_deletado is None:
        raise HTTPException(status_code=404, detail="Nenhum preço do Robusta encontrado para deletar")
    return {"message": f"Preço mais antigo do Robusta (data: {preco_deletado.price_date}) deletado com sucesso"}