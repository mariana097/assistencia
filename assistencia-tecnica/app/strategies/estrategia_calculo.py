from abc import ABC, abstractmethod


class EstrategiaCalculo(ABC):

    @abstractmethod
    def calcular(self, valor_base):
        raise NotImplementedError
