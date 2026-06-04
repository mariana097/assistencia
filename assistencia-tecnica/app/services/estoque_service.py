from app.models.estoque import Estoque
from app.repositories.base_repository import BaseRepository


class EstoqueService:
    def __init__(self, session):
        self.repository = BaseRepository(session, Estoque)

    def atualizar_estoque(self, equipamento_id, quantidade_disponivel, quantidade_minima):
        estoque = Estoque(
            equipamento_id=equipamento_id,
            quantidade_disponivel=quantidade_disponivel,
            quantidade_minima=quantidade_minima,
        )
        return self.repository.add(estoque)

    def listar(self):
        return self.repository.list()
