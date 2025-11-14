from sqlalchemy.orm import Session
from typing import Optional
from app.models.models import Analise
from app.models.schemas import AnaliseCreate, AnaliseUpdate

def criar_analise(db: Session, analise: AnaliseCreate):
    db_analise = Analise(**analise.dict())
    db.add(db_analise)
    db.commit()
    db.refresh(db_analise)
    return db_analise

def obter_analise_por_id(db: Session, analise_id: int):
    return db.query(Analise).filter(Analise.id == analise_id).first()

def listar_analises_por_usuario(db: Session, usuario_id: int, skip: int = 0, limit: int = 100):
    return db.query(Analise).filter(Analise.usuario_id == usuario_id).offset(skip).limit(limit).all()

def listar_todas_analises(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Analise).offset(skip).limit(limit).all()

def atualizar_analise(db: Session, analise_id: int, analise_update: AnaliseUpdate):
    db_analise = db.query(Analise).filter(Analise.id == analise_id).first()
    if db_analise:
        update_data = analise_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_analise, field, value)
        db.commit()
        db.refresh(db_analise)
    return db_analise

def deletar_analise(db: Session, analise_id: int):
    db_analise = db.query(Analise).filter(Analise.id == analise_id).first()
    if db_analise:
        db.delete(db_analise)
        db.commit()
    return db_analise