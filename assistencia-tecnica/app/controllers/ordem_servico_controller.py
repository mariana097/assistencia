class OrdemServicoController:
    def __init__(self, ordem_service):
        self.service = ordem_service

    def criar_ordem(self, **dados):
        return self.service.criar_ordem(**dados)

    def listar_ordens(self):
        return self.service.listar()

    def obter_ordem(self, ordem_id):
        return self.service.get_ordem(ordem_id)

    def calcular_valor_ordem(self, ordem, estrategia):
        return self.service.atualizar_valor(ordem, estrategia)
