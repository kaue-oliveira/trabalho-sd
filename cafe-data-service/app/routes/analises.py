from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.schemas import AnaliseResponse, AnaliseCreate, AnaliseUpdate
from app.crud import analises as crud_analises

# Aliases para compatibilidade
Analise = AnaliseResponse

router = APIRouter(prefix="/analises", tags=["analises"])

@router.post("", response_model=Analise)
def criar_analise(analise: AnaliseCreate, db: Session = Depends(get_db)):
    return crud_analises.criar_analise(db=db, analise=analise)

@router.get("/{analise_id}", response_model=AnaliseResponse)
def ler_analise(analise_id: int, db: Session = Depends(get_db)):
    db_analise = crud_analises.obter_analise_por_id(db, analise_id=analise_id)
    if db_analise is None:
        raise HTTPException(status_code=404, detail="Análise não encontrada")
    return db_analise

@router.get("/usuario/{usuario_id}", response_model=List[AnaliseResponse])
def listar_analises_usuario(
    usuario_id: int, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    return crud_analises.listar_analises_por_usuario(db, usuario_id=usuario_id, skip=skip, limit=limit)

@router.get("", response_model=List[AnaliseResponse])
def listar_analises(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    return crud_analises.listar_todas_analises(db, skip=skip, limit=limit)

@router.put("/{analise_id}", response_model=Analise)
def atualizar_analise(
    analise_id: int, 
    analise_update: AnaliseUpdate, 
    db: Session = Depends(get_db)
):
    db_analise = crud_analises.atualizar_analise(db, analise_id=analise_id, analise_update=analise_update)
    if db_analise is None:
        raise HTTPException(status_code=404, detail="Análise não encontrada")
    return db_analise

@router.delete("/{analise_id}")
def deletar_analise(analise_id: int, db: Session = Depends(get_db)):
    db_analise = crud_analises.deletar_analise(db, analise_id=analise_id)
    if db_analise is None:
        raise HTTPException(status_code=404, detail="Análise não encontrada")
    return {"message": "Análise deletada com sucesso"}