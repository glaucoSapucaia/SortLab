from logger import logger
from sortlab.utils.interfaces import IMetricCounter
from sortlab.functions.interfaces import ISorter
from sortlab.errors import SortingException, EmptyArrException

class CountingSort(ISorter):
    def __init__(self, counter: IMetricCounter) -> None:
        self.counter = counter
        logger.info(f"{self.__class__.__name__} inicializado com contador.")

    def counting_sort(self, input_array: list[int]) -> list[int]:
        try:
            if not input_array:
                logger.warning(f"{self.__class__.__name__} - Lista vazia fornecida para ordenação.")
                raise EmptyArrException(f"{self.__class__.__name__} - Lista vazia fornecida para ordenação.")

            k = max(input_array) + 1
            sorted_array = [0] * len(input_array)
            count_array = [0] * k

            # logger.info(f"Iniciando CountingSort para uma lista de tamanho {len(input_array)} com k = {k}.")

            # Contagem das ocorrências
            for value in input_array:
                count_array[value] += 1
                self.counter.increase()  # Contabilizando a "comparação" de incremento no count_array
                # logger.info(f"Incrementando contagem para o valor {value}.")

            # Soma acumulada no count_array
            for i in range(1, k):
                count_array[i] += count_array[i - 1]
                self.counter.increase()  # Contabilizando a "comparação" de soma acumulada
                # logger.info(f"Soma acumulada no índice {i}: {count_array[i]}.")

            # Colocando os elementos ordenados no sorted_array
            for value in reversed(input_array):
                sorted_array[count_array[value] - 1] = value
                count_array[value] -= 1
                self.counter.increase()  # Movimentação do valor para o sorted_array
                # logger.info(f"Colocando valor {value} na posição {count_array[value] - 1}.")

            # Contabilizando uma última comparação no loop de soma acumulada
            for i in range(1, k):
                self.counter.increase()  # Contabilizando uma comparação
                # logger.info(f"Contabilizando comparação no índice {i}.")

            logger.info("Ordenação completa com CountingSort.")
            return sorted_array

        except Exception as e:
            logger.error(f"Erro no {self.__class__.__name__}: {e}")
            raise SortingException(f"Erro no {self.__class__.__name__}: {e}")

    def sort(self, input_array: list[int]) -> list[int]:
        try:
            return self.counting_sort(input_array)
        except SortingException:
            logger.error(f"Erro ao tentar ordenar a lista com {self.__class__.__name__}.")
            raise
