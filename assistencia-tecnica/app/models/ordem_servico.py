from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.models.cliente import Cliente
from app.models.funcionario import Funcionario
from app.models.aparelho import Aparelho
from app.models.conta_receber import ContaReceber
from app.models.equipamento import Equipamento
from app.models.estoque import Estoque
from app.models.pagamento import Pagamento
from app.models.visita_tecnica import VisitaTecnica

ordem_equipamento = Table(
    "ordem_equipamento",
    Base.metadata,
    Column("ordem_id", Integer, ForeignKey("ordens_servico.id"), primary_key=True),
    Column("equipamento_id", Integer, ForeignKey("equipamentos.id"), primary_key=True),
)


class OrdemServico(Base):
    __tablename__ = "ordens_servico"

    id = Column(Integer, primary_key=True, autoincrement=True)
    data_abertura = Column(DateTime, default=datetime.utcnow)
    data_encerramento = Column(DateTime, nullable=True)
    descricao_problema = Column(String(255), nullable=True)
    status = Column(String(50), default="aberta")
    valor_base = Column(Float, default=0.0)
    valor_total = Column(Float, default=0.0)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    tecnico_id = Column(Integer, ForeignKey("funcionarios.id"), nullable=True)
    aparelho_id = Column(Integer, ForeignKey("aparelhos.id"), nullable=False)

    cliente = relationship("Cliente")
    tecnico = relationship("Funcionario", back_populates="ordens_servico")
    aparelho = relationship("Aparelho", back_populates="ordens_servico")
    visitas_tecnicas = relationship("VisitaTecnica", back_populates="ordem_servico", cascade="all, delete-orphan")
    conta_receber = relationship("ContaReceber", uselist=False, back_populates="ordem_servico", cascade="all, delete-orphan")
    equipamentos = relationship("Equipamento", secondary=ordem_equipamento, back_populates="ordens_servico")

    def __init__(self, *args, estrategia=None, **kwargs):
        super().__init__(*args, **kwargs)
        from app.strategies.calculo_padrao import CalculoPadrao

        self.estrategia = estrategia or CalculoPadrao()

    def calcular_valor_total(self, estrategia):
        self.valor_total = float(estrategia.calcular(self.valor_base or 0.0))
        return self.valor_total

    def calcular_valor(self):
        return self.calcular_valor_total(self.estrategia)
