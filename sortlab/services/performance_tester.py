from settings.logger import logger
from sortlab.utils.metrics import MetricCounter
from sortlab.errors import MetricsException

from typing import TYPE_CHECKING
from time import perf_counter


if TYPE_CHECKING:
    from sortlab.functions.interfaces import ISorter


class PerformanceTester:
    """Classe para testar o desempenho de algoritmos de ordenação.

    Mede o tempo de execução e número de operações para diferentes tamanhos de entrada.
    """

    def __init__(self, sorter_class: "ISorter") -> None:
        """Inicializa o testador de desempenho.

        Args:
            sorter_class: Classe do algoritmo de ordenação a ser testado (deve implementar ISorter)
        """
        self.sorter_class = sorter_class

    def run(
        self, sizes: list[int], base_vector: list[int]
    ) -> tuple[list[float], list[int], str]:
        """Executa os testes de desempenho para múltiplos tamanhos de entrada.

        Args:
            sizes: Lista de tamanhos de vetores a serem testados
            base_vector: Vetor base que será copiado e ordenado

        Returns:
            Tuple contendo:
            - Lista de tempos de execução (em segundos)
            - Lista de contagens de operações
            - Nome do algoritmo testado

        Raises:
            MetricsException: Se ocorrer erro durante a execução dos testes
        """
        times: list[float] = []
        comparisons: list[int] = []
        algorithm_name = self.sorter_class.__name__

        for size in sizes:
            # Cópia segura dos dados para teste
            data = base_vector[:size].copy()
            counter = MetricCounter()
            sorter: "ISorter" = self.sorter_class(counter)

            try:
                start = perf_counter()
                logger.info(f"Testando {algorithm_name} com tamanho {size}")
                sorter.sort(data)
                end = perf_counter()

                elapsed_time = end - start
                times.append(elapsed_time)
                comparisons.append(counter.value)

                logger.info(
                    f"Tamanho {size} concluído em {elapsed_time:.6f}s | "
                    f"Operações: {counter.value}"
                )

            except Exception as e:
                logger.error(f"Falha no teste para tamanho {size}: {e}")
                raise MetricsException(f"Erro nos testes de desempenho: {e}")

        return times, comparisons, algorithm_name
