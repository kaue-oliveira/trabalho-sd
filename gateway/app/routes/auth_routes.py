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

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict


# =====================================================
# ROTAS DE AUTH
# =====================================================
router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
async def login(login_data: LoginRequest, data_client: httpx.AsyncClient = Depends(get_data_service_client)):
    """
    Autentica usuário via Data Service e gera JWT
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
    return {"message": "Logout realizado com sucesso"}


@router.get("/me")
async def get_current_user(payload: dict = Depends(verify_token), data_client: httpx.AsyncClient = Depends(get_data_service_client)):
    """
    Retorna dados do usuário atual via Data Service.
    """
    user_id = int(payload.get("sub"))
    try:
        resp = await data_client.get(f"/usuarios/{user_id}")
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Data Service não disponível: {str(e)}")


@router.post("/forgot-password")
async def forgot_password(payload: dict, data_client: httpx.AsyncClient = Depends(get_data_service_client)):
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
    try:
        resp = await data_client.post("/auth/reset-password", json=payload)
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Data Service não disponível: {str(e)}")
