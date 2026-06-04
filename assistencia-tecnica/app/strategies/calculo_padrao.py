from app.strategies.estrategia_calculo import EstrategiaCalculo


class CalculoPadrao(EstrategiaCalculo):

    def calcular(self, valor_base):
        return valor_base
