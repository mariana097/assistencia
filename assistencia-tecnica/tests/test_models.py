from app.models.cliente import Cliente
from app.models.aparelho import Aparelho
from app.models.funcionario import Tecnico


def test_cliente_e_aparelho_persistem_relacionamento(session):
    cliente = Cliente(
        nome="Maria Silva",
        cpf="12345678900",
        telefone="11999999999",
        email="maria@example.com",
        endereco="Rua das Flores, 123"
    )
    session.add(cliente)
    session.commit()

    aparelho = Aparelho(
        tipo="Notebook",
        marca="Dell",
        modelo="Inspiron",
        numero_serie="ABC123",
        cor="Preto",
        observacoes="Tela trincada",
        cliente_id=cliente.id
    )
    session.add(aparelho)
    session.commit()

    session.refresh(cliente)
    assert cliente.aparelhos
    assert cliente.aparelhos[0].marca == "Dell"
    assert cliente.endereco == "Rua das Flores, 123"
    assert cliente.aparelhos[0].cor == "Preto"


def test_tecnico_persistencia_e_campos_especificos(session):
    tecnico = Tecnico(
        nome="João Souza",
        cpf="98765432100",
        salario=3500.0,
        especialidade="Eletrônica",
        horario_expediente="08:00-17:00",
        status="ativo"
    )
    session.add(tecnico)
    session.commit()

    session.refresh(tecnico)
    assert tecnico.especialidade == "Eletrônica"
    assert tecnico.horario_expediente == "08:00-17:00"
    assert tecnico.status == "ativo"
