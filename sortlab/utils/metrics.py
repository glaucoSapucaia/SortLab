from logger import logger
from sortlab.utils.interfaces import IMetricCounter

class MetricCounter(IMetricCounter):
    """
    Classe responsável por contar métricas (incrementos, resets e decrementos).
    """
    def __init__(self) -> None:
        """
        Inicializa o contador com valor zero.
        """
        self.value = 0
        # logger.info("Contador inicializado com valor zero.")

    def increase(self) -> None:
        """
        Aumenta o valor do contador em 1.
        """
        self.value += 1
        # logger.info(f"Contador incrementado: {self.value}")

    def decrease(self) -> None:
        """
        Diminui o valor do contador em 1.
        """
        if self.value > 0:
            self.value -= 1
            # logger.info(f"Contador decrementado: {self.value}")

    def reset(self) -> None:
        """
        Reseta o valor do contador para zero.
        """
        self.value = 0
        # logger.info("Contador resetado para zero.")

    def set(self, value: int) -> None:
        """
        Define o valor do contador para o valor especificado.
        """
        self.value = value
        # logger.info(f"Contador definido para o valor: {self.value}")

    @property
    def count(self) -> int:
        """
        Retorna o valor atual do contador.
        """
        # logger.info(f"Valor atual do contador: {self.value}")
        return self.value
