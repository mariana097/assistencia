from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base


class Aparelho(Base):
    __tablename__ = "aparelhos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo = Column(String(120), nullable=False)
    marca = Column(String(120), nullable=True)
    modelo = Column(String(120), nullable=True)
    numero_serie = Column(String(120), nullable=True)
    cor = Column(String(50), nullable=True)
    observacoes = Column(String(255), nullable=True)
    status = Column(String(50), default="pendente")
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)

    cliente = relationship("Cliente", back_populates="aparelhos")
    ordens_servico = relationship("OrdemServico", back_populates="aparelho", cascade="all, delete-orphan")
