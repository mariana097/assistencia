from datetime import date, datetime

from app.models.pagamento import Pagamento
from app.repositories.base_repository import BaseRepository


class PagamentoService:
    def __init__(self, session):
        self.repository = BaseRepository(session, Pagamento)

    def registrar_pagamento(
        self,
        cliente_id,
        conta_receber_id,
        valor_pago,
        forma_pagamento,
        data_pagamento=None,
        numero_documento=None,
        observacao=None,
    ):
        if isinstance(data_pagamento, str):
            data_pagamento = datetime.fromisoformat(data_pagamento).date()
        elif data_pagamento is None:
            data_pagamento = date.today()

        pagamento = Pagamento(
            cliente_id=cliente_id,
            conta_receber_id=conta_receber_id,
            valor_pago=valor_pago,
            forma_pagamento=forma_pagamento,
            data_pagamento=data_pagamento,
            numero_documento=numero_documento,
            observacao=observacao,
        )
        return self.repository.add(pagamento)

    def listar(self):
        return self.repository.list()
