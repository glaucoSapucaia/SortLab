from typing import Callable, Type
from sortlab.functions.interfaces import ISorter
from sortlab.services.performance_tester import PerformanceTester
from logger import logger

class AlgorithmExecutor:
    def __init__(self, 
                 algorithms: list[Type[ISorter]], 
                 plots: list[Callable[[list[int], list[float], list[int], str], None]], 
                 tester_factory: Callable = PerformanceTester,
                 logger=logger):
        self._validate_algorithms(algorithms)
        self.algorithms = algorithms
        self.plots = plots
        self.tester_factory = tester_factory
        self.logger = logger

    def _validate_algorithms(self, algorithms):
        for algorithm in algorithms:
            if not isinstance(algorithm, type) or not issubclass(algorithm, ISorter):
                raise TypeError(f"{getattr(algorithm, '__name__', 'Unknown')} deve ser uma classe que implementa ISorter")

    def run(self, vector_sizes: list[int], base_vector: list[int]) -> None:
        self.logger.info("Iniciando execução dos algoritmos")
        
        for algorithm in self.algorithms:
            self._execute_algorithm(algorithm, vector_sizes, base_vector)

    def _execute_algorithm(self, algorithm, vector_sizes, base_vector):
        self.logger.info(f"Executando {algorithm.__name__}")
        tester = self.tester_factory(algorithm)
        times, comparisons, _ = tester.run(vector_sizes, base_vector)
        self._generate_plots(vector_sizes, times, comparisons, algorithm.__name__)

    def _generate_plots(self, sizes, times, comparisons, name):
        for plot in self.plots:
            self.logger.info(f"Gerando gráfico com {plot.__name__}")
            plot(sizes, times, comparisons, name)