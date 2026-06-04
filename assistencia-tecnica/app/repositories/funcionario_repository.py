from app.models.funcionario import Funcionario
from app.repositories.base_repository import BaseRepository


class FuncionarioRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session, Funcionario)
