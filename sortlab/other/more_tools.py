import timeit
import csv
from tabulate import tabulate
from typing import Callable

def run(sort_function: Callable[[list[int]], None],
        vector: list[int]) -> float:
    """Mede o tempo de execução da função de ordenação."""
    try:
        def wrapper() -> None:
            sort_function(vector)

        performance = timeit.timeit(wrapper, number=1)
        return performance
    except Exception as e:
        print(f"Erro ao medir o tempo de execução: {e}")
        return -1  # Retorna -1 em caso de erro

def register(func: Callable[[list[int]], None],
             vector: list[int],
             performance: float,
             counter: int) -> None:
    """Registra os resultados de desempenho em um arquivo CSV."""
    try:
        with open(f"data/{func.__name__}.csv", "w", newline="", encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Função', 'Tamanho do vetor', 'Tempo', 'Qtd comparações'])
            writer.writerow([func.__name__, len(vector), performance, counter])
    except Exception as e:
        print(f"Erro ao registrar os dados no arquivo CSV: {e}")

def reader(func: Callable[[list[int]], None]) -> None:
    """Lê e exibe os resultados registrados no arquivo CSV."""
    try:
        with open(f"data/{func.__name__}.csv", newline="", encoding='utf-8') as file:
            reader = csv.reader(file)
            data = list(reader)
        
        print(tabulate(data, headers="firstrow", tablefmt="grid"))
    except FileNotFoundError:
        print(f"Arquivo de dados para a função {func.__name__} não encontrado.")
    except Exception as e:
        print(f"Erro ao ler o arquivo CSV: {e}")

def counter() -> tuple[Callable[[], None], Callable[[], int]]:
    """Retorna um contador de comparações/trocas."""
    total = 0
    def increase() -> None:
        nonlocal total
        total += 1

    def value() -> int:
        return total

    return increase, value
