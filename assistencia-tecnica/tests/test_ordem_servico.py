from app.models.ordem_servico import OrdemServico
from app.factories.estrategia_factory import EstrategiaFactory


def test_ordem_servico_calcula_valor_com_estrategia_urgente():
    estrategia = EstrategiaFactory.criar("urgente")
    ordem = OrdemServico(cliente_id=1, aparelho_id=1, valor_base=100, estrategia=estrategia)

    total = ordem.calcular_valor()

    assert total == 150
    assert ordem.valor_total == 150


def test_ordem_servico_calcula_valor_com_estrategia_padrao_por_default():
    ordem = OrdemServico(cliente_id=1, aparelho_id=1, valor_base=100)

    total = ordem.calcular_valor()

    assert total == 100
    assert ordem.valor_total == 100
