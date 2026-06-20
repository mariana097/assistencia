from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.models.base import Base


class Equipamento(Base):
    __tablename__ = "equipamentos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(120), nullable=False)
    quantidade = Column(Integer, default=0)
    valor_unitario = Column(Float, default=0.0)
    fornecedor = Column(String(120), nullable=True)
    observacoes = Column(String(500), nullable=True)

    estoque = relationship("Estoque", back_populates="equipamento", uselist=False, cascade="all, delete-orphan")
    ordens_servico = relationship("OrdemServico", secondary="ordem_equipamento", back_populates="equipamentos")
