from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud.usuarios import obter_usuario_por_email, verificar_senha
from app.models.schemas import LoginRequest, LoginResponse

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=LoginResponse)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    
    # Busca usuário por email
    usuario = obter_usuario_por_email(db, email=login_data.email)
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuários e/ou senha inválidos"
        )
    
    if not verificar_senha(login_data.password, usuario.senha):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuários e/ou senha inválidos"
        )
    
    user_data = {
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email,
        "tipo_conta": usuario.tipo_conta,
        "criado_em": usuario.criado_em.isoformat() if usuario.criado_em else None
    }
    
    return LoginResponse(
        access_token="placeholder",  # Será substituído pelo Gateway
        user=user_data
    )