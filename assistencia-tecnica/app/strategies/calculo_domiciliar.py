from app.strategies.estrategia_calculo import EstrategiaCalculo


class CalculoDomiciliar(EstrategiaCalculo):

    def calcular(self, valor_base):
        return valor_base + 50
