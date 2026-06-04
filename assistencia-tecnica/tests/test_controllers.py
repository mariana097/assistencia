from app.controllers.cliente_controller import ClienteController
from app.controllers.ordem_servico_controller import OrdemServicoController
from app.services.cliente_service import ClienteService
from app.services.ordem_servico_service import OrdemServicoService
from app.factories.estrategia_factory import EstrategiaFactory
from app.models.cliente import Cliente
from app.models.aparelho import Aparelho


def test_cliente_controller_cadastrar_cliente(session):
    controller = ClienteController(ClienteService(session))

    cliente = controller.cadastrar_cliente(
        nome="Raul",
        cpf="55544433322",
        telefone="11977776666",
        email="raul@example.com",
        endereco="Av. Central, 789"
    )

    assert cliente.id is not None
    assert cliente.email == "raul@example.com"


def test_ordem_servico_controller_calcular_valor(session):
    cliente = Cliente(nome="Bruna", cpf="11122233344", telefone="11966665555", email="bruna@example.com")
    session.add(cliente)
    session.commit()

    aparelho = Aparelho(tipo="Smartphone", marca="Xiaomi", modelo="Redmi", numero_serie="MI12345", cliente_id=cliente.id)
    session.add(aparelho)
    session.commit()

    service = OrdemServicoService(session)
    controller = OrdemServicoController(service)

    ordem = controller.criar_ordem(
        cliente_id=cliente.id,
        aparelho_id=aparelho.id,
        valor_base=120,
        descricao_problema="Não liga"
    )

    estrategia = EstrategiaFactory.criar("hora")
    ordem_calculada = controller.calcular_valor_ordem(ordem, estrategia)

    assert ordem_calculada.valor_total == 144
    assert ordem_calculada.id == ordem.id
