from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.schemas import UsuarioResponse, UsuarioCreate
from app.crud import usuarios as crud_usuarios

# Alias para manter compatibilidade
Usuario = UsuarioResponse

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

@router.post("/", response_model=Usuario)
def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    db_user = crud_usuarios.obter_usuario_por_email(db, email=usuario.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email já registrado")
    return crud_usuarios.criar_usuario(db=db, usuario=usuario)

@router.get("/{usuario_id}", response_model=Usuario)
def ler_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_user = crud_usuarios.obter_usuario_por_id(db, usuario_id=usuario_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return db_user

@router.get("/", response_model=list[Usuario])
def listar_usuarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    usuarios = crud_usuarios.listar_usuarios(db, skip=skip, limit=limit)
    return usuarios