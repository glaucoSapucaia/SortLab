from sortlab.functions.interfaces import ISorter
from sortlab.services.performance_tester import PerformanceTester
from settings.logger import logger

from collections.abc import Callable


class AlgorithmExecutor:
    """Executor de algoritmos de ordenação com medição de desempenho e geração de gráficos."""

    def __init__(
        self,
        algorithms: list[type[ISorter]],
        plots: list[Callable[[list[int], list[float], list[int], str], None]],
        tester_factory: type[PerformanceTester] = PerformanceTester,
        logger=logger,
    ) -> None:
        """Inicializa o executor de algoritmos.

        Args:
            algorithms: Lista de classes de algoritmos de ordenação (devem implementar ISorter)
            plots: Lista de funções para geração de gráficos de desempenho
            tester_factory: Classe para teste de desempenho (padrão: PerformanceTester)
            logger: Logger para registro de mensagens (padrão: logger global)
        """
        self._validate_algorithms(algorithms)
        self.algorithms = algorithms
        self.plots = plots
        self.tester_factory = tester_factory
        self.logger = logger

    def _validate_algorithms(self, algorithms: list[type[ISorter]]) -> None:
        """Valida se todos os algoritmos implementam a interface ISorter.

        Raises:
            TypeError: Se algum algoritmo não implementar ISorter
        """
        for algorithm in algorithms:
            if not isinstance(algorithm, type) or not issubclass(algorithm, ISorter):
                raise TypeError(
                    f"{getattr(algorithm, '__name__', 'Unknown')} deve implementar ISorter"
                )

    def run(self, vector_sizes: list[int], base_vector: list[int]) -> None:
        """Executa todos os algoritmos para os tamanhos de vetor especificados.

        Args:
            vector_sizes: Lista de tamanhos de vetores para teste
            base_vector: Vetor base que será copiado e ordenado
        """
        self.logger.info("Iniciando execução dos algoritmos")
        for algorithm in self.algorithms:
            self._execute_algorithm(algorithm, vector_sizes, base_vector)

    def _execute_algorithm(
        self, algorithm: type[ISorter], vector_sizes: list[int], base_vector: list[int]
    ) -> None:
        """Executa um algoritmo específico e gera seus gráficos de desempenho.

        Args:
            algorithm: Classe do algoritmo a ser executado
            vector_sizes: Tamanhos de vetores para teste
            base_vector: Vetor base para cópia e ordenação
        """
        self.logger.info(f"Executando {algorithm.__name__}")
        tester = self.tester_factory(algorithm)
        times, comparisons, _ = tester.run(vector_sizes, base_vector)
        self._generate_plots(vector_sizes, times, comparisons, algorithm.__name__)

    def _generate_plots(
        self, sizes: list[int], times: list[float], comparisons: list[int], name: str
    ) -> None:
        """Gera todos os gráficos para os resultados de um algoritmo.

        Args:
            sizes: Tamanhos dos vetores testados
            times: Tempos de execução para cada tamanho
            comparisons: Número de comparações para cada tamanho
            name: Nome do algoritmo para título dos gráficos
        """
        for plot in self.plots:
            self.logger.info(f"Gerando gráfico com {plot.__name__}")
            plot(sizes, times, comparisons, name)
