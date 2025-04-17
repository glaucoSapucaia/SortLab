from .shared_imports import *

import math


class BucketSort(ISorter):
    """Implementação do algoritmo Bucket Sort com possibilidade de customização do algoritmo de ordenação dos buckets."""

    def __init__(self, counter: IMetricCounter, sorter=None) -> None:
        """Inicializa o Bucket Sort com contador de métricas e algoritmo auxiliar.

        Args:
            counter: Contador para métricas de operações
            sorter: Algoritmo para ordenar os buckets (padrão: insertion_sort)
        """
        self.counter = counter
        self.sorter = sorter or self.insertion_sort
        logger.info(
            f"{self.__class__.__name__} inicializado com contador e {self.sorter.__name__}."
        )

    def insertion_sort(self, arr: list[int]) -> list[int]:
        """Ordena um bucket usando Insertion Sort.

        Args:
            arr: Lista a ser ordenada

        Returns:
            Lista ordenada

        Raises:
            SortingException: Se ocorrer erro durante a ordenação
        """
        try:
            for j in range(1, len(arr)):
                self.counter.increase()
                key = arr[j]
                i = j - 1
                while i >= 0 and arr[i] > key:
                    self.counter.increase()
                    arr[i + 1] = arr[i]
                    self.counter.increase()
                    i -= 1
                arr[i + 1] = key
                self.counter.increase()
            return arr
        except Exception as e:
            logger.error(
                f"Erro no {self.__class__.__name__} durante Insertion Sort: {e}"
            )
            raise SortingException(f"Erro no {self.__class__.__name__}: {e}")

    def sort(self, data: list[int]) -> list[int]:
        """Implementa a interface ISorter para ordenação via Bucket Sort.

        Args:
            data: Lista de inteiros a ser ordenada

        Returns:
            Lista ordenada

        Raises:
            EmptyArrException: Se a lista estiver vazia
            SortingException: Se ocorrer erro durante a ordenação
        """
        try:
            if not data:
                logger.warning(f"{self.__class__.__name__} - Lista vazia.")
                raise EmptyArrException(f"{self.__class__.__name__} - Lista vazia.")

            buckets = [[] for _ in range(len(data))]
            max_value = max(data) or 1  # Evita divisão por zero

            for val in data:
                self.counter.increase()
                index = min(math.floor(len(data) * (val / max_value)), len(data) - 1)
                buckets[index].append(val)

            for bucket in buckets:
                self.counter.increase()
                bucket = self.sorter(bucket)

            return [item for bucket in buckets for item in bucket]

        except SortingException:
            logger.error(f"Erro ao ordenar com {self.__class__.__name__}.")
            raise
