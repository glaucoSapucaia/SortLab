from logger import logger
from sortlab.utils.interfaces import IMetricCounter
from sortlab.functions.interfaces import ISorter
from sortlab.errors import SortingException, EmptyArrException

class BubbleSort(ISorter):
    def __init__(self, counter: IMetricCounter) -> None:
        self.counter = counter
        logger.info("BubbleSort inicializado com contador.")

    def bubble_sort(self, arr: list[int]) -> list[int]:
        try:
            n = len(arr)
            # logger.info(f"Iniciando ordenação com BubbleSort para uma lista de tamanho {n}.")
            for i in range(n - 1):
                swapped = False
                for j in range(n - 1, i, -1):
                    self.counter.increase()  # Comparação
                    if arr[j] < arr[j - 1]:
                        self.counter.increase()  # Troca
                        arr[j], arr[j - 1] = arr[j - 1], arr[j]
                        swapped = True
                        # logger.info(f"Troca realizada: {arr[j]} e {arr[j - 1]}")
                # Se não houver troca, o array já está ordenado
                if not swapped:
                    # logger.info("Nenhuma troca realizada, a lista já está ordenada.")
                    break
            return arr
        except Exception as e:
            logger.error(f"Erro no {self.__class__.__name__}: {e}")
            raise SortingException(f"Erro no {self.__class__.__name__}: {e}")

    def sort(self, arr: list[int]) -> list[int]:
        try:
            if not arr:
                logger.warning(f"{self.__class__.__name__} - Lista vazia fornecida para ordenação.")
                raise EmptyArrException(f"{self.__class__.__name__} - Lista vazia fornecida para ordenação.")
            
            return self.bubble_sort(arr)
        except SortingException:
            logger.error(f"Erro ao tentar ordenar a lista com {self.__class__.__name__}.")
            raise
