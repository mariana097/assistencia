from datetime import date
from sqlalchemy import Column, Integer, Float, Date, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base


class ContaReceber(Base):
    __tablename__ = "contas_receber"

    id = Column(Integer, primary_key=True, autoincrement=True)
    valor = Column(Float, nullable=False, default=0.0)
    vencimento = Column(Date, default=date.today)
    status = Column(String(50), default="aberta")
    ordem_servico_id = Column(Integer, ForeignKey("ordens_servico.id"), nullable=False)

    ordem_servico = relationship("OrdemServico", back_populates="conta_receber")
    pagamento = relationship("Pagamento", back_populates="conta_receber", uselist=False, cascade="all, delete-orphan")
