from pydantic import BaseModel, Field
from typing import Optional, List

class Requisicao(BaseModel):
    tipo_cafe: str
    data_colheita: str = Field(..., description="YYYY-MM-DD")
    quantidade: float
    cidade: str
    estado: str
    estado_cafe: str

class Resposta(BaseModel):
    decisao: str
    explicacao_decisao: str