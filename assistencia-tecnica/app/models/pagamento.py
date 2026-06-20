from datetime import date
from sqlalchemy import Column, Integer, Float, Date, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base


class Pagamento(Base):
    __tablename__ = "pagamentos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    valor_pago = Column(Float, nullable=False, default=0.0)
    data_pagamento = Column(Date, default=date.today)
    forma_pagamento = Column(String(50), nullable=True)
    numero_documento = Column(String(100), nullable=True)
    observacao = Column(String(500), nullable=True)
    conta_receber_id = Column(Integer, ForeignKey("contas_receber.id"), nullable=False)

    cliente = relationship("Cliente", back_populates="pagamentos")
    conta_receber = relationship("ContaReceber", back_populates="pagamento")
