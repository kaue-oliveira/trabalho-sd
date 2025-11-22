from fastapi import APIRouter, Depends, HTTPException
import httpx
from app.clients.data_client import get_data_service_client
from app.utils.jwt_utils import create_access_token, verify_token
from pydantic import BaseModel


# =====================================================
# SCHEMAS DO AUTH
# =====================================================
class LoginRequest(BaseModel):
    email: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "ana.cafeicultora@email.com",
                "password": "CafeAna123"
            }
        }


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict

    class Config:
        schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "user": {
                    "id": 1,
                    "nome": "Ana Costa",
                    "email": "ana.cafeicultora@email.com",
                    "tipo_conta": "PRODUTOR"
                }
            }
        }

class ForgotPasswordRequest(BaseModel):
    email: str

    class Config:
        schema_extra = {
            "example": {
                "email": "ana.cafeicultora@email.com"
            }
        }


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

    class Config:
        schema_extra = {
            "example": {
                "token": "reset_token_123",
                "new_password": "NovaSenha456"
            }
        }


# =====================================================
# ROTAS DE AUTH
# =====================================================
router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
async def login(login_data: LoginRequest, data_client: httpx.AsyncClient = Depends(get_data_service_client)):
    """
    Autentica usuário no sistema e retorna token JWT.

    - **email**: E-mail do usuário cadastrado
    - **password**: Senha do usuário
    
    Retorna access_token para uso em requisições autenticadas
    e dados do usuário autenticado.
    """
    try:
        resp = await data_client.post("/auth/login", json=login_data.dict())
        resp.raise_for_status()
        response_data = resp.json()
        user_data = response_data["user"]

        token_data = {"sub": str(user_data["id"]), "email": user_data["email"]}
        access_token = create_access_token(token_data)

        return LoginResponse(access_token=access_token, user=user_data)

    except httpx.HTTPStatusError as e:
        detail = e.response.json().get("detail") if e.response.content else e.response.text
        raise HTTPException(status_code=e.response.status_code, detail=detail or "Erro de autenticação")
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Data Service não disponível: {str(e)}")

@router.post("/logout")
async def logout():
    """
    Realiza logout do usuário.
    
    Nota: Em sistemas JWT stateless, o logout é realizado no cliente
    através da remoção do token.
    """
    return {"message": "Logout realizado com sucesso"}

@router.post("/forgot-password")
async def forgot_password(payload: dict, data_client: httpx.AsyncClient = Depends(get_data_service_client)):
    """
    Solicita recuperação de senha para o e-mail informado.

    - **email**: E-mail da conta para recuperação
    
    Envia instruções por e-mail para redefinição de senha.
    """
    try:
        resp = await data_client.post("/auth/forgot-password", json=payload)
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Data Service não disponível: {str(e)}")


@router.post("/reset-password")
async def reset_password(payload: dict, data_client: httpx.AsyncClient = Depends(get_data_service_client)):
    """
    Redefine a senha do usuário usando token de recuperação.

    - **token**: Token recebido por e-mail
    - **new_password**: Nova senha para a conta
    
    Redefine a senha e invalida o token de recuperação.
    """
    try:
        resp = await data_client.post("/auth/reset-password", json=payload)
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Data Service não disponível: {str(e)}")
