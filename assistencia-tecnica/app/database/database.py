import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config.settings import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def init_db():
    from app.models.base import Base
    from app.models.cliente import Cliente
    from app.models.aparelho import Aparelho
    from app.models.funcionario import Funcionario, Tecnico, Administrador
    from app.models.ordem_servico import OrdemServico
    from app.models.visita_tecnica import VisitaTecnica
    from app.models.equipamento import Equipamento
    from app.models.estoque import Estoque
    from app.models.conta_receber import ContaReceber
    from app.models.pagamento import Pagamento

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
