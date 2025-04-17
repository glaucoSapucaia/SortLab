import pytest
from unittest.mock import MagicMock, patch
from sortlab.pipeline import AlgorithmRunner
from typing import Optional

class TestAlgorithmRunner:
    @patch('sortlab.algorithm_runner.AlgorithmExecutor')
    def test_run_algorithms_with_custom_executor(self, mock_executor):
        """Testa se run_algorithms usa o executor fornecido"""
        mock_executor_instance = MagicMock()
        sizes = [100, 200]
        base_vector = [3, 1, 2]
        
        AlgorithmRunner.run_algorithms(sizes, base_vector, mock_executor_instance)
        
        mock_executor_instance.run.assert_called_once_with(sizes, base_vector)
        mock_executor.assert_not_called()

    @patch('sortlab.algorithm_runner.AlgorithmExecutor')
    def test_run_algorithms_with_default_executor(self, mock_executor):
        """Testa se run_algorithms cria um executor padrão quando nenhum é fornecido"""
        mock_executor_instance = MagicMock()
        mock_executor.return_value = mock_executor_instance
        sizes = [100, 200]
        base_vector = [3, 1, 2]
        
        AlgorithmRunner.run_algorithms(sizes, base_vector)
        
        mock_executor.assert_called_once()
        mock_executor_instance.run.assert_called_once_with(sizes, base_vector)

    @patch('sortlab.algorithm_runner.random.randint')
    def test_generate_random_vector(self, mock_randint):
        """Testa a geração de vetor aleatório"""
        mock_randint.return_value = 42
        size = 5
        
        result = AlgorithmRunner._generate_random_vector(size)
        
        assert result == [42, 42, 42, 42, 42]
        assert mock_randint.call_count == size
        mock_randint.assert_called_with(0, 1000)

    @patch('sortlab.algorithm_runner.AlgorithmRunner.run_algorithms')
    @patch('sortlab.algorithm_runner.AlgorithmRunner._generate_random_vector')
    def test_execute_default_algorithms(self, mock_generate, mock_run):
        """Testa o método execute_default_algorithms"""
        mock_generate.return_value = [1, 2, 3]
        
        AlgorithmRunner.execute_default_algorithms()
        
        mock_generate.assert_called_once_with(max(AlgorithmRunner.DEFAULT_SIZES))
        mock_run.assert_called_once_with(AlgorithmRunner.DEFAULT_SIZES, [1, 2, 3], None)

    def test_default_sizes(self):
        """Testa se DEFAULT_SIZES tem os valores esperados"""
        assert AlgorithmRunner.DEFAULT_SIZES == [300, 600, 900, 1200, 1500, 2000]