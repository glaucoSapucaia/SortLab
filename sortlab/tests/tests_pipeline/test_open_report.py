import pytest
from unittest.mock import patch, MagicMock
from sortlab.pipeline import ReportViewer
from paths import config
import webbrowser
from logger import logger

class TestReportViewer:
    @patch('sortlab.pipeline.open_report.webbrowser.open')
    @patch('sortlab.pipeline.open_report.logger')
    @patch('sortlab.pipeline.open_report.config.get_path')
    def test_open_report_success(self, mock_get_path, mock_logger, mock_webbrowser):
        """Testa a abertura bem-sucedida do relatório"""
        # Configura os mocks
        test_pdf_path = "/caminho/para/relatorio.pdf"
        mock_get_path.return_value = test_pdf_path
        mock_webbrowser.return_value = True
        
        # Chama o método
        ReportViewer.open_report()
        
        # Verifica as chamadas
        mock_get_path.assert_called_once_with('REPORT_FILE')
        mock_logger.info.assert_any_call(f"Abrindo relatório: {test_pdf_path}")
        mock_logger.info.assert_any_call("Relatório aberto com sucesso")
        mock_webbrowser.assert_called_once_with(str(test_pdf_path))

    @patch('sortlab.pipeline.open_report.webbrowser.open')
    @patch('sortlab.pipeline.open_report.logger')
    @patch('sortlab.pipeline.open_report.config.get_path')
    def test_open_report_failure(self, mock_get_path, mock_logger, mock_webbrowser):
        """Testa o tratamento de erro quando a abertura do relatório falha"""
        # Configura os mocks
        test_pdf_path = "/caminho/para/relatorio.pdf"
        mock_get_path.return_value = test_pdf_path
        test_exception = Exception("Erro simulado")
        mock_webbrowser.side_effect = test_exception
        
        # Verifica se a exceção é levantada
        with pytest.raises(Exception) as exc_info:
            ReportViewer.open_report()
        
        # Verifica as chamadas e a mensagem de erro
        assert str(exc_info.value) == "Erro simulado"
        mock_logger.info.assert_called_once_with(f"Abrindo relatório: {test_pdf_path}")
        mock_logger.error.assert_called_once_with("Falha ao abrir relatório: Erro simulado")

