from fastapi import APIRouter, Depends, HTTPException
import httpx
from app.clients.data_client import get_data_service_client
from app.utils.jwt_utils import verify_token
from pydantic import BaseModel
from typing import List, Optional


# =====================================================
# SCHEMAS DE USUÁRIO
# =====================================================
class UserCreateRequest(BaseModel):
    nome: str
    email: str
    senha: str
    tipo_conta: Optional[str] = "PRODUTOR"

    class Config:
        schema_extra = {
            "example": {
                "nome": "Ana Costa",
                "email": "ana.cafeicultora@email.com",
                "senha": "CafeAna123",
                "tipo_conta": "PRODUTOR"
            }
        }


class UserUpdateRequest(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    senha: Optional[str] = None
    tipo_conta: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "nome": "Ana Costa Atualizada",
                "email": "ana.nova@email.com",
                "senha": "CafeAna123",
                "tipo_conta": "PRODUTOR"
            }
        }


class UserResponse(BaseModel):
    id: int
    nome: str
    email: str
    tipo_conta: str

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "nome": "Ana Costa",
                "email": "ana.cafeicultora@email.com",
                "tipo_conta": "PRODUTOR"
            }
        }


# =====================================================
# ROTAS DE USUÁRIOS
# =====================================================
router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@router.get("")

async def listar_usuarios(data_client: httpx.AsyncClient = Depends(get_data_service_client)):
    """
    Lista todos os usuários do sistema.
    
    Requer autenticação JWT.
    Retorna uma lista com todos os usuários cadastrados.
    """
    try:
        resp = await data_client.get("/usuarios")
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Data Service não disponível: {str(e)}")


@router.get("/me")
async def get_current_user(payload: dict = Depends(verify_token), data_client: httpx.AsyncClient = Depends(get_data_service_client)):
    """
    Retorna dados do usuário atualmente autenticado.
    
    Utiliza o token JWT para identificar o usuário e buscar
    seus dados completos no Data Service.
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
    

@router.post("")
async def criar_usuario(user_data: dict, data_client: httpx.AsyncClient = Depends(get_data_service_client)):
    """
    Cria um novo usuário no sistema.

    - **nome**: Nome completo do usuário
    - **email**: E-mail único do usuário
    - **senha**: Senha de acesso (mínimo 8 caracteres)
    - **tipo_conta**: Tipo de conta (PRODUTOR, ADMIN) - opcional, padrão: PRODUTOR
    
    Retorna os dados do usuário criado.
    """
    try:
        resp = await data_client.post("/usuarios", json=user_data)
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Data Service não disponível: {str(e)}")


@router.put("/me")
async def atualizar_usuario(user_data: dict, token_payload: dict = Depends(verify_token), data_client: httpx.AsyncClient = Depends(get_data_service_client)):
    """
    Atualiza os dados do usuário autenticado.

    - **nome**: Novo nome (opcional)
    - **email**: Novo e-mail (opcional)
    - **tipo_conta**: Novo tipo de conta (opcional)
    
    Retorna os dados atualizados do usuário.
    O usuário só pode atualizar seus próprios dados.
    """
    user_id = token_payload.get("user_id")
    try:
        resp = await data_client.put(f"/usuarios/{user_id}", json=user_data)
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Data Service não disponível: {str(e)}")


@router.delete("/me")
async def deletar_usuario(token_payload: dict = Depends(verify_token), data_client: httpx.AsyncClient = Depends(get_data_service_client)):
    """
    Remove permanentemente a conta do usuário autenticado.
    
    Esta ação é irreversível e remove todos os dados do usuário.
    O usuário só pode deletar sua própria conta.
    """
    user_id = token_payload.get("user_id")
    try:
        resp = await data_client.delete(f"/usuarios/{user_id}")
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Data Service não disponível: {str(e)}")
