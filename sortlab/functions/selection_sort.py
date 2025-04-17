from .shared_imports import *


class SelectionSort(ISorter):
    def __init__(self, counter: IMetricCounter) -> None:
        self.counter = counter
        logger.info(f"{self.__class__.__name__} inicializado com contador.")

    def selection_sort(self, arr: list[int]) -> list[int]:
        try:
            # logger.info(f"Iniciando SelectionSort para uma lista de tamanho {len(arr)}.")
            for i in range(len(arr) - 1):
                _min = i
                # logger.info(f"Iniciando iteração {i}.")

                for j in range(i + 1, len(arr)):
                    self.counter.increase()  # Comparação
                    # logger.info(f"Comparando arr[{j}] = {arr[j]} com arr[{_min}] = {arr[_min]}.")
                    if arr[j] < arr[_min]:
                        _min = j
                        # logger.info(f"Novo mínimo encontrado em arr[{_min}] = {arr[_min]}.")

                if arr[i] != arr[_min]:
                    self.counter.increase()  # Troca
                    # logger.info(f"Trocando arr[{i}] = {arr[i]} com arr[{_min}] = {arr[_min]}.")
                    arr[i], arr[_min] = arr[_min], arr[i]

            logger.info("Ordenação concluída com SelectionSort.")
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

            return self.selection_sort(arr)
        except SortingException:
            logger.error(
                f"Erro ao tentar ordenar a lista com {self.__class__.__name__}."
            )
            raise
