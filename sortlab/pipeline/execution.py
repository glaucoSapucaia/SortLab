from typing import Optional
from sortlab.functions import get_sorting_algorithms
from sortlab.scripts import get_plot_functions
from .algorithm_executor import AlgorithmExecutor
import random

class AlgorithmRunner:
    DEFAULT_SIZES = [300, 600, 900, 1200, 1500, 2000]
    
    @staticmethod
    def run_algorithms(
        vector_sizes: list[int],
        base_vector: list[int],
        executor: Optional[AlgorithmExecutor] = None
    ) -> None:
        executor = executor or AlgorithmExecutor(
            algorithms=get_sorting_algorithms(),
            plots=get_plot_functions()
        )
        executor.run(vector_sizes, base_vector)

    @classmethod
    def execute_default_algorithms(cls) -> None:
        base_vector = cls._generate_random_vector(max(cls.DEFAULT_SIZES))
        cls.run_algorithms(cls.DEFAULT_SIZES, base_vector)

    @staticmethod
    def _generate_random_vector(size: int) -> list[int]:
        return [random.randint(0, 1000) for _ in range(size)]