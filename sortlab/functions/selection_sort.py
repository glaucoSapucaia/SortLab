from .shared_imports import *


class SelectionSort(ISorter):
    """Implementação do algoritmo de ordenação Selection Sort."""

    def __init__(self, counter: IMetricCounter) -> None:
        """Inicializa o Selection Sort com contador de métricas.

        Args:
            counter: Objeto para contabilizar comparações e trocas.
        """
        self.counter = counter
        logger.info(f"{self.__class__.__name__} inicializado com contador.")

    def selection_sort(self, arr: list[int]) -> list[int]:
        """Ordena a lista usando o algoritmo Selection Sort.

        Args:
            arr: Lista de inteiros a ser ordenada.

        Returns:
            Lista ordenada em ordem crescente.

        Raises:
            SortingException: Se ocorrer erro durante a ordenação.
        """
        try:
            for i in range(len(arr) - 1):
                _min = i
                for j in range(i + 1, len(arr)):
                    self.counter.increase()  # Contabiliza comparação
                    if arr[j] < arr[_min]:
                        _min = j

                if arr[i] != arr[_min]:
                    self.counter.increase()  # Contabiliza troca
                    arr[i], arr[_min] = arr[_min], arr[i]

            return arr

        except Exception as e:
            logger.error(f"Erro no {self.__class__.__name__}: {e}")
            raise SortingException(f"Erro no {self.__class__.__name__}: {e}")

    def sort(self, arr: list[int]) -> list[int]:
        """Interface pública para ordenação, implementando ISorter.

        Args:
            arr: Lista de inteiros a ser ordenada.

        Returns:
            Lista ordenada em ordem crescente.

        Raises:
            EmptyArrException: Se a lista estiver vazia.
            SortingException: Se ocorrer erro durante a ordenação.
        """
        try:
            if not arr:
                logger.warning(f"{self.__class__.__name__} - Lista vazia.")
                raise EmptyArrException(f"{self.__class__.__name__} - Lista vazia.")

            return self.selection_sort(arr)

        except SortingException:
            logger.error(f"Erro ao ordenar com {self.__class__.__name__}.")
            raise
