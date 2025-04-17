from abc import ABC, abstractmethod


class ISorter(ABC):
    """Interface abstrata para algoritmos de ordenação.

    Todas as implementações concretas devem fornecer um método `sort`.
    """

    @abstractmethod
    def sort(self, arr: list[int]) -> list[int]:
        pass
