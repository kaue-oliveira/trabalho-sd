from pydantic import BaseModel, Field
from typing import Optional, List

class Requisicao(BaseModel):
    # Metadados funcionais
    localidade: Optional[str] = None
    data_colheita: Optional[str] = Field(None, description="YYYY-MM-DD")
    tipo_grao: Optional[str] = Field(None, description="verde|torrado|moido")

    # Dados opcionais já resolvidos (bypassa gateway)
    clima: Optional[dict] = None
    preco: Optional[dict] = None


    # Consulta para RAG (opcional)
    pergunta_relatorios: Optional[str] = None


class Resposta(BaseModel):
    decision: str
    explanation: str
    contexto_relatorios: List[dict] = []