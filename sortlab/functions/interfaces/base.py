from abc import ABC, abstractmethod


class ISorter(ABC):
    @abstractmethod
    def sort(self, arr: list[int]) -> list[int]:
        pass
