class ClienteController:
    def __init__(self, cliente_service):
        self.service = cliente_service

    def cadastrar_cliente(self, **dados):
        return self.service.cadastrar(**dados)

    def listar_clientes(self):
        return self.service.listar()
