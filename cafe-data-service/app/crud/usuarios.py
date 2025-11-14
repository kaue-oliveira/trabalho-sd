from sqlalchemy.orm import Session
from app.models.models import Usuario
from app.models.schemas import UsuarioCreate

def criar_usuario(db: Session, usuario: UsuarioCreate):
    db_usuario = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha=usuario.senha,  # ⚠️ Em produção, faça hash da senha!
        tipo_conta=usuario.tipo_conta
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def obter_usuario_por_id(db: Session, usuario_id: int):
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()

def obter_usuario_por_email(db: Session, email: str):
    return db.query(Usuario).filter(Usuario.email == email).first()

def listar_usuarios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Usuario).offset(skip).limit(limit).all()