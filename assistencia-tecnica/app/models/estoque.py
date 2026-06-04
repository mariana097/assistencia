from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base


class Estoque(Base):
    __tablename__ = "estoques"

    id = Column(Integer, primary_key=True, autoincrement=True)
    quantidade_disponivel = Column(Integer, default=0)
    quantidade_minima = Column(Integer, default=0)
    equipamento_id = Column(Integer, ForeignKey("equipamentos.id"), nullable=False, unique=True)

    equipamento = relationship("Equipamento", back_populates="estoque")

    def precisa_repor(self):
        return self.quantidade_disponivel <= self.quantidade_minima
