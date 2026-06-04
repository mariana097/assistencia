from app.services.cliente_service import ClienteService
from app.services.ordem_servico_service import OrdemServicoService
from app.factories.estrategia_factory import EstrategiaFactory
from app.models.cliente import Cliente
from app.models.aparelho import Aparelho


def test_cliente_service_cadastrar_e_listar(session):
    service = ClienteService(session)

    cliente = service.cadastrar(
        nome="Lucas",
        cpf="32165498700",
        telefone="11999998888",
        email="lucas@example.com",
        endereco="Rua B, 456"
    )

    assert cliente.id is not None
    assert cliente.nome == "Lucas"
    assert cliente.endereco == "Rua B, 456"

    clientes = service.listar()
    assert any(item.cpf == "32165498700" for item in clientes)


def test_ordem_servico_service_criar_ordem_e_atualizar_valor(session):
    cliente = Cliente(nome="Mariana", cpf="45678912300", telefone="11988887777", email="mariana@example.com")
    session.add(cliente)
    session.commit()

    aparelho = Aparelho(tipo="Tablet", marca="Apple", modelo="iPad", numero_serie="IPAD123", cliente_id=cliente.id)
    session.add(aparelho)
    session.commit()

    service = OrdemServicoService(session)
    ordem = service.criar_ordem(
        cliente_id=cliente.id,
        aparelho_id=aparelho.id,
        valor_base=200,
        descricao_problema="Bateria descarrega rápido"
    )

    assert ordem.id is not None
    assert ordem.valor_total == 200

    estrategia = EstrategiaFactory.criar("urgente")
    ordem_atualizada = service.atualizar_valor(ordem, estrategia)

    assert ordem_atualizada.valor_total == 300
    assert ordem_atualizada.valor_total == ordem.valor_total
