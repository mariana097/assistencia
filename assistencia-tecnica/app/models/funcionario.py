from datetime import date
from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.orm import relationship
from app.models.base import Base


class Funcionario(Base):
    __tablename__ = "funcionarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(120), nullable=False)
    cpf = Column(String(14), nullable=False, unique=True)
    salario = Column(Float, nullable=False)
    data_admissao = Column(Date, default=date.today)
    horario_expediente = Column(String(50), nullable=True)
    status = Column(String(50), default="ativo")
    especialidade = Column(String(120), nullable=True)
    nivel_acesso = Column(String(50), nullable=True)
    tipo = Column(String(50), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "funcionario",
        "polymorphic_on": tipo,
    }

    ordens_servico = relationship("OrdemServico", back_populates="tecnico")
    visitas = relationship("VisitaTecnica", back_populates="tecnico")


class Tecnico(Funcionario):
    __mapper_args__ = {"polymorphic_identity": "tecnico"}


class Administrador(Funcionario):
    __mapper_args__ = {"polymorphic_identity": "administrador"}
