from .shared_imports import *

import math


class BucketSort(ISorter):
    def __init__(self, counter: IMetricCounter, sorter=None) -> None:
        self.counter = counter
        self.sorter = (
            sorter or self.insertion_sort
        )  # Permite injetar outro algoritmo de ordenação
        logger.info(
            f"{self.__class__.__name__} inicializado com contador e {self.sorter.__name__} como algoritmo de ordenação."
        )

    def insertion_sort(self, arr: list[int]) -> list[int]:
        try:
            # logger.info(f"Iniciando ordenação com Insertion Sort para uma lista de tamanho {len(arr)}.")
            for j in range(1, len(arr)):
                self.counter.increase()  # Iteração do for externo
                key = arr[j]
                i = j - 1
                while i >= 0 and arr[i] > key:
                    self.counter.increase()  # Comparação dentro do while
                    arr[i + 1] = arr[i]
                    self.counter.increase()  # Movimentação de elementos
                    i -= 1
                arr[i + 1] = key
                self.counter.increase()  # Movimentação para inserir o key
            # logger.info("Ordenação por Insertion Sort concluída.")
            return arr
        except Exception as e:
            logger.error(
                f"Erro no {self.__class__.__name__} durante o Insertion Sort: {e}"
            )
            raise SortingException(f"Erro no {self.__class__.__name__}: {e}")

    def sort(self, data: list[int]) -> list[int]:
        try:
            if not data:
                logger.warning(
                    f"{self.__class__.__name__} - Lista vazia fornecida para ordenação."
                )
                raise EmptyArrException(
                    f"{self.__class__.__name__} - Lista vazia fornecida para ordenação."
                )

            # logger.info(f"Distribuindo {len(data)} elementos em buckets.")
            buckets = [[] for _ in range(len(data))]

            max_value = max(data)
            if max_value == 0:
                max_value = 1  # Evita divisão por zero

            for i, val in enumerate(data):
                self.counter.increase()  # Iteração para distribuir valores nos buckets
                index = math.floor(
                    len(data) * (val / max_value)
                )  # Normaliza dados entre 0 e 1
                if index == len(data):  # Evita IndexError
                    index -= 1
                buckets[index].append(val)

            for i in range(len(buckets)):
                self.counter.increase()  # Iteração para ordenar cada bucket
                # logger.info(f"Ordenando o bucket {i} com {len(buckets[i])} elementos.")
                buckets[i] = self.sorter(buckets[i])

            sorted_data: list[int] = []
            for bucket in buckets:
                self.counter.increase()  # Iteração para concatenar os buckets
                sorted_data.extend(bucket)

            logger.info("Ordenação completa com Bucket Sort.")
            return sorted_data

        except SortingException:
            logger.error(
                f"Erro ao tentar ordenar a lista com {self.__class__.__name__}."
            )
            raise
