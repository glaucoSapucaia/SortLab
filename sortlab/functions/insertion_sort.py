from .shared_imports import *


class InsertionSort(ISorter):
    def __init__(self, counter: IMetricCounter) -> None:
        self.counter = counter
        logger.info(f"{self.__class__.__name__} inicializado com contador.")

    def insertion_sort(self, arr: list[int]) -> list[int]:
        try:
            logger.info(
                f"Iniciando InsertionSort para uma lista de tamanho {len(arr)}."
            )
            for j in range(1, len(arr)):
                key = arr[j]
                i = j - 1

                # logger.info(f"Iniciando iteração {j} com chave {key}.")

                while i >= 0 and arr[i] > key:
                    self.counter.increase()  # Comparação
                    # logger.info(f"Comparando arr[{i}] = {arr[i]} com chave {key}.")
                    self.counter.increase()  # Troca (movimentação)
                    # logger.info(f"Trocando arr[{i + 1}] = {arr[i]} com arr[{i}] = {arr[i + 1]}.")
                    arr[i + 1] = arr[i]
                    i -= 1

                self.counter.increase()  # Inserção final do key (troca)
                arr[i + 1] = key
                # logger.info(f"Inserindo chave {key} na posição {i + 1}.")

            logger.info("Ordenação concluída com InsertionSort.")
            return arr
        except Exception as e:
            logger.error(f"Erro no {self.__class__.__name__}: {e}")
            raise SortingException(f"Erro no {self.__class__.__name__}: {e}")

    def sort(self, arr: list[int]) -> list[int]:
        try:
            if not arr:
                logger.warning(
                    f"{self.__class__.__name__} - Lista vazia fornecida para ordenação."
                )
                raise EmptyArrException(
                    f"{self.__class__.__name__} - Lista vazia fornecida para ordenação."
                )

            return self.insertion_sort(arr)
        except SortingException:
            logger.error(
                f"Erro ao tentar ordenar a lista com {self.__class__.__name__}."
            )
            raise
