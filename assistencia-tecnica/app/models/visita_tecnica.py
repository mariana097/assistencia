from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base


class VisitaTecnica(Base):
    __tablename__ = "visitas_tecnicas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    data_agendamento = Column(DateTime, default=datetime.utcnow)
    data_realizacao = Column(DateTime, nullable=True)
    resultado = Column(String(255), nullable=True)
    status = Column(String(50), default="agendada")
    ordem_servico_id = Column(Integer, ForeignKey("ordens_servico.id"), nullable=False)
    tecnico_id = Column(Integer, ForeignKey("funcionarios.id"), nullable=True)

    ordem_servico = relationship("OrdemServico", back_populates="visitas_tecnicas")
    tecnico = relationship("Funcionario", back_populates="visitas")
