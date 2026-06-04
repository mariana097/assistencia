from app.models.pagamento import Pagamento
from app.repositories.base_repository import BaseRepository


class PagamentoService:
    def __init__(self, session):
        self.repository = BaseRepository(session, Pagamento)

    def registrar_pagamento(self, conta_receber_id, valor_pago, forma_pagamento):
        pagamento = Pagamento(
            conta_receber_id=conta_receber_id,
            valor_pago=valor_pago,
            forma_pagamento=forma_pagamento,
        )
        return self.repository.add(pagamento)

    def listar(self):
        return self.repository.list()
