from app.repositories.cliente_repository import ClienteRepository


class ClienteService:
    def __init__(self, session):
        self.repository = ClienteRepository(session)

    def cadastrar(self, nome, cpf, telefone=None, email=None, endereco=None):
        from app.models.cliente import Cliente

        cliente = Cliente(
            nome=nome,
            cpf=cpf,
            telefone=telefone,
            email=email,
            endereco=endereco,
        )
        return self.repository.add(cliente)

    def listar(self):
        return self.repository.list()
