from app.repositories.aparelho_repository import AparelhoRepository


class AparelhoService:
    def __init__(self, session):
        self.repository = AparelhoRepository(session)

    def cadastrar(self, tipo, marca, modelo, numero_serie, observacoes, cliente_id):
        from app.models.aparelho import Aparelho

        aparelho = Aparelho(
            tipo=tipo,
            marca=marca,
            modelo=modelo,
            numero_serie=numero_serie,
            observacoes=observacoes,
            cliente_id=cliente_id,
        )
        return self.repository.add(aparelho)

    def listar(self):
        return self.repository.list()
