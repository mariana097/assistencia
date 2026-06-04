from app.factories.estrategia_factory import EstrategiaFactory
from app.strategies.calculo_padrao import CalculoPadrao
from app.strategies.calculo_urgente import CalculoUrgente
from app.strategies.calculo_por_hora import CalculoPorHora
from app.strategies.calculo_domiciliar import CalculoDomiciliar


def test_factory_cria_calculo_padrao_por_default():
    estrategia = EstrategiaFactory.criar("invalido")
    assert isinstance(estrategia, CalculoPadrao)


def test_factory_cria_calculo_urgente():
    estrategia = EstrategiaFactory.criar("urgente")
    assert isinstance(estrategia, CalculoUrgente)


def test_factory_cria_calculo_por_hora():
    estrategia = EstrategiaFactory.criar("hora")
    assert isinstance(estrategia, CalculoPorHora)


def test_factory_cria_calculo_domiciliar():
    estrategia = EstrategiaFactory.criar("domiciliar")
    assert isinstance(estrategia, CalculoDomiciliar)
