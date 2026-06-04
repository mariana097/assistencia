from app.repositories.funcionario_repository import FuncionarioRepository


class FuncionarioService:
    def __init__(self, session):
        self.repository = FuncionarioRepository(session)

    def cadastrar_tecnico(self, nome, cpf, salario):
        from app.models.funcionario import Tecnico

        tecnico = Tecnico(nome=nome, cpf=cpf, salario=salario, tipo="tecnico")
        return self.repository.add(tecnico)

    def cadastrar_administrador(self, nome, cpf, salario):
        from app.models.funcionario import Administrador

        administrador = Administrador(nome=nome, cpf=cpf, salario=salario, tipo="administrador")
        return self.repository.add(administrador)

    def listar(self):
        return self.repository.list()
