from app.strategies.estrategia_calculo import EstrategiaCalculo


class CalculoUrgente(EstrategiaCalculo):

    def calcular(self, valor_base):
        return valor_base * 1.5
