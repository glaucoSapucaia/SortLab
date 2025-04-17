import pytest
from unittest.mock import MagicMock
from sortlab.services import PerformanceTester
from sortlab.errors import MetricsException

@pytest.fixture
def dummy_sorter_class():
    """Mock de uma classe que implementa ISorter"""
    class DummySorter:
        __name__ = "DummySorter"

        def __init__(self, counter):
            self.counter = counter

        def sort(self, data):
            self.counter.increase()
            data.sort()

    return DummySorter

def test_run_returns_correct_structure(dummy_sorter_class):
    tester = PerformanceTester(dummy_sorter_class)
    base_vector = [5, 3, 2, 4, 1, 6, 7, 8, 9, 10]
    sizes = [5, 10]

    times, comparisons, name = tester.run(sizes, base_vector)

    assert len(times) == len(sizes)
    assert len(comparisons) == len(sizes)
    assert all(isinstance(t, float) for t in times)
    assert all(isinstance(c, int) for c in comparisons)
    assert name == "DummySorter"

def test_sorter_exception_raises_metrics_exception(dummy_sorter_class):
    class FailingSorter(dummy_sorter_class):
        def sort(self, data):
            raise ValueError("Erro simulado na ordenação")

    tester = PerformanceTester(FailingSorter)
    base_vector = [5, 4, 3, 2, 1]

    with pytest.raises(MetricsException) as exc_info:
        tester.run([5], base_vector)

    assert "Erro no PerformanceTester" in str(exc_info.value)

def test_base_vector_is_not_modified(dummy_sorter_class):
    tester = PerformanceTester(dummy_sorter_class)
    original_vector = [5, 4, 3, 2, 1]
    base_copy = original_vector.copy()

    tester.run([5], original_vector)

    assert original_vector == base_copy, "O vetor original foi modificado"
