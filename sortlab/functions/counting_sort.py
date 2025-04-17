from .shared_imports import *


class CountingSort(ISorter):
    """Implementação do algoritmo Counting Sort para ordenação de inteiros não-negativos."""

    def __init__(self, counter: IMetricCounter) -> None:
        """Inicializa o Counting Sort com contador de métricas.

        Args:
            counter: Objeto para contabilizar operações do algoritmo.
        """
        self.counter = counter
        logger.info(f"{self.__class__.__name__} inicializado com contador.")

    def counting_sort(self, input_array: list[int]) -> list[int]:
        """Implementa o algoritmo Counting Sort.

        Args:
            input_array: Lista de inteiros não-negativos a ser ordenada.

        Returns:
            Lista ordenada em ordem crescente.

        Raises:
            EmptyArrException: Se a lista de entrada estiver vazia.
            SortingException: Se ocorrer erro durante a ordenação.
        """
        try:
            if not input_array:
                logger.warning(f"{self.__class__.__name__} - Lista vazia.")
                raise EmptyArrException(f"{self.__class__.__name__} - Lista vazia.")

            k = max(input_array) + 1
            sorted_array = [0] * len(input_array)
            count_array = [0] * k

            # Fase de contagem
            for value in input_array:
                count_array[value] += 1
                self.counter.increase()

            # Fase de soma cumulativa
            for i in range(1, k):
                count_array[i] += count_array[i - 1]
                self.counter.increase()

            # Fase de ordenação
            for value in reversed(input_array):
                sorted_array[count_array[value] - 1] = value
                count_array[value] -= 1
                self.counter.increase()

            # Contagem adicional para métricas
            for i in range(1, k):
                self.counter.increase()

            return sorted_array

        except Exception as e:
            logger.error(f"Erro no {self.__class__.__name__}: {e}")
            raise SortingException(f"Erro no {self.__class__.__name__}: {e}")

    def sort(self, input_array: list[int]) -> list[int]:
        """Interface pública para ordenação, implementando ISorter.

        Args:
            input_array: Lista de inteiros não-negativos a ser ordenada.

        Returns:
            Lista ordenada em ordem crescente.

        Raises:
            SortingException: Se ocorrer erro durante a ordenação.
        """
        try:
            return self.counting_sort(input_array)
        except SortingException:
            logger.error(f"Erro ao ordenar com {self.__class__.__name__}.")
            raise
