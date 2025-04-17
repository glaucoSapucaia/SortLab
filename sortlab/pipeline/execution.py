from .algorithm_executor import AlgorithmExecutor
from sortlab.functions import get_sorting_algorithms
from sortlab.scripts import plot_interactive, plot_static

import random


class AlgorithmRunner:
    """Coordena a execução de algoritmos de ordenação com configurações padrão."""

    DEFAULT_SIZES = [300, 600, 900, 1200, 1500, 2000]
    """Lista de tamanhos de vetores usados para testes de desempenho padrão."""

    @staticmethod
    def run_algorithms(
        vector_sizes: list[int],
        base_vector: list[int],
        executor: AlgorithmExecutor | None = None,
    ) -> None:
        """Executa os algoritmos de ordenação nos vetores especificados.

        Args:
            vector_sizes: Tamanhos dos vetores a serem testados
            base_vector: Vetor base que será copiado e ordenado
            executor: Executor personalizado (usa o padrão se None)
        """
        executor = executor or AlgorithmExecutor(
            algorithms=get_sorting_algorithms(), plots=[plot_static, plot_interactive]
        )
        executor.run(vector_sizes, base_vector)

    @classmethod
    def execute_default_algorithms(cls) -> None:
        """Executa os algoritmos com configurações padrão (tamanhos e vetor aleatório)."""
        base_vector = cls._generate_random_vector(max(cls.DEFAULT_SIZES))
        cls.run_algorithms(cls.DEFAULT_SIZES, base_vector)

    @staticmethod
    def _generate_random_vector(size: int) -> list[int]:
        """Gera um vetor de inteiros aleatórios.

        Args:
            size: Tamanho do vetor a ser gerado

        Returns:
            Lista de inteiros aleatórios entre 0 e 1000
        """
        return [random.randint(0, 1000) for _ in range(size)]
