from time import perf_counter
from sortlab.utils.metrics import MetricCounter
from sortlab.errors import MetricsException
from typing import TYPE_CHECKING
from settings.logger import logger

if TYPE_CHECKING:
    from sortlab.functions.interfaces import ISorter # pragma: no cover

class PerformanceTester:
    def __init__(self, sorter_class: 'ISorter') -> None:
        self.sorter_class = sorter_class

    def run(self, sizes: list[int], base_vector: list[int]) -> tuple[list[float], list[int], str]:
        times: list[float] = []
        comparisons: list[int] = []
        algorithm_name = self.sorter_class.__name__

        for size in sizes:
            # Cópia dos dados para evitar mutação do vetor original
            data = base_vector[:size].copy()
            counter = MetricCounter()
            sorter: 'ISorter' = self.sorter_class(counter)

            try:
                start = perf_counter()
                logger.info(f"Iniciando a ordenação para o tamanho {size}...")
                sorter.sort(data)
                end = perf_counter()
                logger.info(f"Ordenação concluída para o tamanho {size}. Tempo: {end - start:.6f} segundos.")
            except Exception as e:
                logger.error(f"Erro no {self.__class__.__name__} para o tamanho {size}: {e}")
                raise MetricsException(f"Erro no {self.__class__.__name__}: {e}")

            times.append(end - start)
            comparisons.append(counter.value)

        return times, comparisons, algorithm_name
