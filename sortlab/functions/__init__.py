from .bucket_sort import BucketSort
from .counting_sort import CountingSort
from .insertion_sort import InsertionSort
from .selection_sort import SelectionSort
from .bubble_sort import BubbleSort

def get_sorting_algorithms():
    """Retorna todas as classes de algoritmos de ordenação disponíveis"""
    return [
        BubbleSort,
        InsertionSort,
        SelectionSort,
        CountingSort,
        BucketSort
    ]

__all__ = ['BucketSort', 'CountingSort', 'InsertionSort',
           'SelectionSort', 'BubbleSort']
