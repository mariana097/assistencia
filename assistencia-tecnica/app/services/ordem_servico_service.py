from app.repositories.ordem_servico_repository import OrdemServicoRepository


class OrdemServicoService:
    def __init__(self, session):
        self.repository = OrdemServicoRepository(session)

    def criar_ordem(self, cliente_id, aparelho_id, valor_base, descricao_problema, tecnico_id=None):
        from app.models.ordem_servico import OrdemServico

        ordem = OrdemServico(
            cliente_id=cliente_id,
            aparelho_id=aparelho_id,
            valor_base=valor_base,
            descricao_problema=descricao_problema,
            tecnico_id=tecnico_id,
            valor_total=valor_base,
        )
        return self.repository.add(ordem)

    def get_ordem(self, ordem_id):
        return self.repository.get(ordem_id)

    def atualizar_valor(self, ordem, estrategia):
        ordem.calcular_valor_total(estrategia)
        self.repository.session.commit()
        return ordem

    def listar(self):
        return self.repository.list()
