from app.strategies.calculo_padrao import CalculoPadrao
from app.strategies.calculo_urgente import CalculoUrgente
from app.strategies.calculo_por_hora import CalculoPorHora
from app.strategies.calculo_domiciliar import CalculoDomiciliar


def test_calculo_padrao_retornando_valor_base():
    estrategia = CalculoPadrao()
    assert estrategia.calcular(100) == 100


def test_calculo_urgente_aplica_multiplicador():
    estrategia = CalculoUrgente()
    assert estrategia.calcular(100) == 150


def test_calculo_por_hora_aplica_hora_extra():
    estrategia = CalculoPorHora()
    assert estrategia.calcular(100) == 120


def test_calculo_domiciliar_soma_valor_fixo():
    estrategia = CalculoDomiciliar()
    assert estrategia.calcular(100) == 150
