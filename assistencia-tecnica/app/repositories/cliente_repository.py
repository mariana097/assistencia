from app.models.cliente import Cliente
from app.repositories.base_repository import BaseRepository


class ClienteRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session, Cliente)
