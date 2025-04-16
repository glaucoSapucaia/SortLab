from abc import ABC, abstractmethod

class IMetricCounter(ABC):
    @abstractmethod
    def increase(self) -> None:
        """
        Aumenta o valor do contador em 1.
        """
        pass

    @abstractmethod
    def decrease(self) -> None:
        """
        Diminui o valor do contador em 1.
        """
        pass

    @abstractmethod
    def reset(self) -> None:
        """
        Reseta o valor do contador para zero.
        """
        pass

    @abstractmethod
    def set(self, value: int) -> None:
        """
        Define o valor do contador para o valor especificado.
        """
        pass

    @property
    @abstractmethod
    def count(self) -> int:
        """
        Retorna o valor atual do contador.
        """
        pass
