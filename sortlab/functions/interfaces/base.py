from abc import ABC, abstractmethod
from typing import List

class ISorter(ABC):
    @abstractmethod
    def sort(self, arr: List[int]) -> List[int]:
        pass
