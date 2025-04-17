from .bucket_sort import BucketSort
from .counting_sort import CountingSort
from .insertion_sort import InsertionSort
from .selection_sort import SelectionSort
from .bubble_sort import BubbleSort

# Lista única como fonte de verdade
_SORTING_ALGORITHMS = [
    BubbleSort,
    InsertionSort,
    SelectionSort,
    CountingSort,
    BucketSort,
]


def get_sorting_algorithms():
    """Retorna todas as classes de algoritmos de ordenação disponíveis"""
    return _SORTING_ALGORITHMS.copy()  # Retorna cópia para evitar mutações externas


__all__ = [cls.__name__ for cls in _SORTING_ALGORITHMS]  # Gera automaticamente
