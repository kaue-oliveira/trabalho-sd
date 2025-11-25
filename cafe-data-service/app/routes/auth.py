from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud.usuarios import obter_usuario_por_email, verificar_senha
from app.models.schemas import LoginRequest, LoginResponse
from app.jwt_utils import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=LoginResponse)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    
    # Busca usuário por email
    usuario = obter_usuario_por_email(db, email=login_data.email)
    
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuários e/ou senha inválidos")
    
    if usuario.senha.startswith("$2b$") or usuario.senha.startswith("$2a$"):
        # senha com hash bcrypt
        if not verificar_senha(login_data.password, usuario.senha):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuários e/ou senha inválidos")
    else:
        if login_data.password != usuario.senha:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuários e/ou senha inválidos")

    
    access_token = create_access_token(
        data={
            "sub": usuario.email,
            "user_id": usuario.id,
            "tipo_conta": usuario.tipo_conta
        }
    )
    
    user_data = {
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email,
        "tipo_conta": usuario.tipo_conta,
        "criado_em": usuario.criado_em.isoformat() if usuario.criado_em else None
    }
    
    return LoginResponse(
        access_token=access_token,
        user=user_data
    )