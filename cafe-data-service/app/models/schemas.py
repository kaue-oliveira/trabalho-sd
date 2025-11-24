from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional, List
from decimal import Decimal

# Schemas para autenticação
class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str


# Schemas para Usuario
class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr
    tipo_conta: str

class UsuarioCreate(UsuarioBase):
    senha: str

class UsuarioResponse(UsuarioBase):
    id: int
    criado_em: datetime

    class Config:
        from_attributes = True

# Schemas para Analise
class AnaliseBase(BaseModel):
    tipo_cafe: str
    data_colheita: date
    quantidade: Decimal
    cidade: str
    estado: str
    estado_cafe: str
    data_analise: date
    decisao: str
    explicacao_decisao: str

class AnaliseCreate(AnaliseBase):
    usuario_id: int

class AnaliseUpdate(BaseModel):
    tipo_cafe: Optional[str] = None
    quantidade: Optional[Decimal] = None
    estado_cafe: Optional[str] = None
    decisao: Optional[str] = None
    explicacao_decisao: Optional[str] = None

class AnaliseResponse(AnaliseBase):
    id: int
    usuario_id: int
    criado_em: datetime
    usuario_nome: Optional[str] = None

    class Config:
        from_attributes = True

# Response schemas para listagens
class UsuarioComAnalises(UsuarioResponse):
    analises: List[AnaliseResponse] = []

# Aliases para compatibilidade
Usuario = UsuarioResponse
Analise = AnaliseResponse


# Schemas para ArabicaPrice
class ArabicaPriceBase(BaseModel):
    price_date: date
    price: Decimal

class ArabicaPriceCreate(ArabicaPriceBase):
    pass

class ArabicaPriceUpdate(BaseModel):
    price_date: Optional[date] = None
    price: Optional[Decimal] = None

class ArabicaPriceResponse(ArabicaPriceBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Schemas para RobustaPrice
class RobustaPriceBase(BaseModel):
    price_date: date
    price: Decimal

class RobustaPriceCreate(RobustaPriceBase):
    pass

class RobustaPriceUpdate(BaseModel):
    price_date: Optional[date] = None
    price: Optional[Decimal] = None

class RobustaPriceResponse(RobustaPriceBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Aliases para compatibilidade
ArabicaPrice = ArabicaPriceResponse
RobustaPrice = RobustaPriceResponse