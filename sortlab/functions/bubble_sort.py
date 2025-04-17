from .shared_imports import *


class BubbleSort(ISorter):
    """Implementação do algoritmo de ordenação Bubble Sort.

    Args:
        counter: Contador de métricas para comparações e trocas.
    """

    def __init__(self, counter: IMetricCounter) -> None:
        """Inicializa o Bubble Sort com um contador de métricas.

        Args:
            counter: Objeto para contabilizar operações do algoritmo.
        """
        self.counter = counter
        logger.info("BubbleSort inicializado com contador.")

    def bubble_sort(self, arr: list[int]) -> list[int]:
        """Executa o algoritmo Bubble Sort na lista fornecida.

        Args:
            arr: Lista de inteiros a ser ordenada.

        Returns:
            Lista ordenada em ordem crescente.

        Raises:
            SortingException: Se ocorrer um erro durante a ordenação.
        """
        try:
            n = len(arr)
            for i in range(n - 1):
                swapped = False
                for j in range(n - 1, i, -1):
                    self.counter.increase()  # Comparação
                    if arr[j] < arr[j - 1]:
                        self.counter.increase()  # Troca
                        arr[j], arr[j - 1] = arr[j - 1], arr[j]
                        swapped = True
                if not swapped:
                    break
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
            EmptyArrException: Se a lista fornecida estiver vazia.
            SortingException: Se ocorrer um erro durante a ordenação.
        """
        try:
            if not arr:
                logger.warning(
                    f"{self.__class__.__name__} - Lista vazia fornecida para ordenação."
                )
                raise EmptyArrException(
                    f"{self.__class__.__name__} - Lista vazia fornecida para ordenação."
                )

            return self.bubble_sort(arr)
        except SortingException:
            logger.error(
                f"Erro ao tentar ordenar a lista com {self.__class__.__name__}."
            )
            raise
