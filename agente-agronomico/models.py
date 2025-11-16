from pydantic import BaseModel, Field
from typing import Optional, List

class Requisicao(BaseModel):
    localidade: Optional[str] = None
    data_colheita: Optional[str] = Field(None, description="YYYY-MM-DD")
    tipo_grao: Optional[str] = None
    clima: Optional[dict] = None
    preco: Optional[dict] = None

class Resposta(BaseModel):
    decision: str
    explanation: str