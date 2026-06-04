from app.models.ordem_servico import OrdemServico
from app.repositories.base_repository import BaseRepository


class OrdemServicoRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session, OrdemServico)
