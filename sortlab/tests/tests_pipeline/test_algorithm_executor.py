from sortlab.pipeline.algorithm_executor import AlgorithmExecutor
from sortlab.functions.interfaces import ISorter

import pytest
from unittest.mock import MagicMock, call


# Dummy sorter válido
class DummySorter(ISorter):
    """Implementação mock de ISorter para testes."""

    def __init__(self, _=None):
        """Inicializador vazio para o sorter mock."""
        pass

    def sort(self, data):
        """Método de ordenação que simplesmente ordena os dados in-place."""
        data.sort()


def test_validate_algorithms_accepts_only_isorter():
    """Verifica se apenas classes que implementam ISorter são aceitas."""

    class NotASorter:
        """Classe que não implementa ISorter para testar validação."""

        pass

    with pytest.raises(TypeError, match="NotASorter deve implementar ISorter"):
        AlgorithmExecutor([NotASorter], plots=[])


def test_run_executes_all_algorithms_and_plots(monkeypatch):
    """Testa se o executor roda todos algoritmos e gera os plots corretamente."""
    # Arranjo
    mock_logger = MagicMock()
    mock_plot = MagicMock()
    mock_plot.__name__ = "mock_plot"

    mock_tester_instance = MagicMock()
    mock_tester_instance.run.return_value = ([0.1, 0.2], [5, 6], "DummySorter")

    mock_tester_factory = MagicMock(return_value=mock_tester_instance)

    executor = AlgorithmExecutor(
        algorithms=[DummySorter],
        plots=[mock_plot],
        tester_factory=mock_tester_factory,
        logger=mock_logger,
    )

    vector_sizes = [10, 20]
    base_vector = list(range(20, 0, -1))

    # Ato
    executor.run(vector_sizes, base_vector)

    # Assert
    mock_logger.info.assert_has_calls(
        [
            call("Iniciando execução dos algoritmos"),
            call("Executando DummySorter"),
            call("Gerando gráfico com mock_plot"),
        ]
    )

    mock_tester_factory.assert_called_once_with(DummySorter)
    mock_tester_instance.run.assert_called_once_with(vector_sizes, base_vector)
    mock_plot.assert_called_once_with([10, 20], [0.1, 0.2], [5, 6], "DummySorter")


def test_multiple_plots_are_generated():
    """Verifica se múltiplos plots são gerados quando fornecidos."""
    plot1 = MagicMock()
    plot1.__name__ = "plot1"
    plot2 = MagicMock()
    plot2.__name__ = "plot2"

    mock_tester = MagicMock()
    mock_tester.run.return_value = ([0.1], [3], "DummySorter")

    executor = AlgorithmExecutor(
        algorithms=[DummySorter],
        plots=[plot1, plot2],
        tester_factory=lambda algo: mock_tester,
        logger=MagicMock(),
    )

    executor.run([10], [5, 4, 3, 2, 1])

    plot1.assert_called_once()
    plot2.assert_called_once()
