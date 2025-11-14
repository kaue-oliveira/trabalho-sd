from sqlalchemy import Column, Integer, String, DateTime, Date, Numeric, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    senha = Column(String(255), nullable=False)
    tipo_conta = Column(String(20), nullable=False)  # PRODUTOR, COOPERATIVA
    criado_em = Column(DateTime(timezone=True), server_default=func.now())

    # Relacionamento com análises
    analises = relationship("Analise", back_populates="usuario")

class Analise(Base):
    __tablename__ = "analises"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    tipo_cafe = Column(String(100), nullable=False)
    data_colheita = Column(Date, nullable=False)
    quantidade = Column(Numeric(10, 2), nullable=False)
    cidade = Column(String(100), nullable=False)
    estado = Column(String(2), nullable=False)
    estado_cafe = Column(String(20), nullable=False)  # verde, torrado, moído
    data_analise = Column(Date, nullable=False)
    decisao = Column(String(20), nullable=False)  # VENDER, VENDER_PARCIALMENTE, AGUARDAR
    explicacao_decisao = Column(Text, nullable=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())

    # Relacionamento
    usuario = relationship("Usuario", back_populates="analises")