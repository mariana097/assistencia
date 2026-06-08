from app.strategies.calculo_padrao import CalculoPadrao
from app.strategies.calculo_urgente import CalculoUrgente
from app.strategies.calculo_por_hora import CalculoPorHora
from app.strategies.calculo_domiciliar import CalculoDomiciliar


class EstrategiaFactory:

    @staticmethod
    def criar(tipo: str):
        if tipo == "urgente":
            return CalculoUrgente()

        if tipo == "hora":
            return CalculoPorHora()

        if tipo == "domiciliar":
            return CalculoDomiciliar()

        return CalculoPadrao()
