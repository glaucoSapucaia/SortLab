import pytest
from unittest import mock
from sortlab.utils.delete_temp_files import clean_temp_files
from settings.logger import logger
from sortlab.pipeline import CleanupService  # Ajuste o import conforme necessário

@mock.patch('sortlab.pipeline.cleanup.logger')
@mock.patch('sortlab.pipeline.cleanup.clean_temp_files')
def test_cleanup_success(mock_clean_func, mock_logger):
    """Testa o fluxo bem-sucedido"""
    CleanupService.clean_temp_files()
    
    mock_logger.info.assert_any_call("Iniciando limpeza de arquivos temporários")
    mock_clean_func.assert_called_once()
    mock_logger.info.assert_any_call("Limpeza concluída com sucesso")
    mock_logger.error.assert_not_called()

@pytest.mark.parametrize("exception,error_message", [
    (PermissionError("Permissão negada"), "Permissão negada"),
    (FileNotFoundError("Arquivo não encontrado"), "Arquivo não encontrado"),
    (Exception("Erro genérico"), "Erro genérico"),
    (RuntimeError("Falha crítica"), "Falha crítica"),
])

@mock.patch('sortlab.pipeline.cleanup.logger')
@mock.patch('sortlab.pipeline.cleanup.clean_temp_files')
def test_cleanup_with_exceptions(mock_cleanup, mock_logger, exception, error_message):
    """Testa diferentes tipos de exceções"""
    mock_cleanup.side_effect = exception
    
    with pytest.raises(type(exception)) as exc_info:
        CleanupService.clean_temp_files()
    
    assert str(exc_info.value) == error_message
    mock_logger.error.assert_called_once_with(f"Falha na limpeza: {error_message}")


@mock.patch('sortlab.pipeline.cleanup.logger')
@mock.patch('sortlab.pipeline.cleanup.clean_temp_files')
def test_cleanup_logs_correct_sequence_on_error(mock_cleanup, mock_logger):
    """Testa a sequência de logs em caso de erro"""
    mock_cleanup.side_effect = Exception("Erro teste")
    
    with pytest.raises(Exception):
        CleanupService.clean_temp_files()
    
    assert mock_logger.method_calls == [
        mock.call.info("Iniciando limpeza de arquivos temporários"),
        mock.call.error("Falha na limpeza: Erro teste")
    ]

@mock.patch('sortlab.pipeline.cleanup.clean_temp_files')
def test_cleanup_propagates_exception_unchanged(mock_cleanup):
    """Testa se a exceção original é propagada sem modificação"""
    test_exception = ValueError("Valor inválido")
    mock_cleanup.side_effect = test_exception
    
    with pytest.raises(ValueError) as exc_info:
        CleanupService.clean_temp_files()
    
    assert exc_info.value is test_exception

@mock.patch('sortlab.pipeline.cleanup.logger')
@mock.patch('sortlab.pipeline.cleanup.clean_temp_files')
def test_cleanup_with_empty_error_message(mock_cleanup, mock_logger):
    """Testa comportamento com mensagem de erro vazia"""
    mock_cleanup.side_effect = Exception("")
    
    with pytest.raises(Exception):
        CleanupService.clean_temp_files()
    
    mock_logger.error.assert_called_once_with("Falha na limpeza: ")