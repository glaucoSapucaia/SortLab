from sortlab.pipeline import ReportGenerator

import pytest
from unittest.mock import patch


class TestReportGenerator:
    @patch("sortlab.pipeline.report.generate_pdf_report")
    @patch("sortlab.pipeline.report.logger")
    def test_generate_report_success(self, mock_logger, mock_generate_pdf):
        """Testa a geração bem-sucedida do relatório"""
        # Chama o método
        ReportGenerator.generate_report()

        # Verifica as chamadas
        mock_logger.info.assert_any_call("Gerando relatório PDF")
        mock_logger.info.assert_any_call("Relatório gerado com sucesso")
        mock_generate_pdf.assert_called_once()

        # Verifica que não houve erros
        mock_logger.error.assert_not_called()

    @patch("sortlab.pipeline.report.generate_pdf_report")
    @patch("sortlab.pipeline.report.logger")
    def test_generate_report_failure(self, mock_logger, mock_generate_pdf):
        """Testa o tratamento de erro quando a geração do relatório falha"""
        # Configura o mock para levantar exceção
        test_exception = Exception("Erro simulado na geração")
        mock_generate_pdf.side_effect = test_exception

        # Verifica se a exceção é propagada
        with pytest.raises(Exception) as exc_info:
            ReportGenerator.generate_report()

        # Verifica as chamadas
        assert str(exc_info.value) == "Erro simulado na geração"
        mock_logger.info.assert_called_once_with("Gerando relatório PDF")
        mock_logger.error.assert_called_once_with(
            "Falha ao gerar relatório: Erro simulado na geração"
        )

        # Verifica que o log de sucesso não foi chamado
        assert all(
            "sucesso" not in call.args[0] for call in mock_logger.info.mock_calls
        )

    @patch("sortlab.pipeline.report.generate_pdf_report")
    @patch("sortlab.pipeline.report.logger")
    def test_generate_report_specific_exception(self, mock_logger, mock_generate_pdf):
        """Testa se exceções específicas são propagadas corretamente"""
        # Configura uma exceção específica
        test_exception = ValueError("Erro de valor inválido")
        mock_generate_pdf.side_effect = test_exception

        # Verifica se a exceção específica é propagada
        with pytest.raises(ValueError) as exc_info:
            ReportGenerator.generate_report()

        # Verificações
        assert exc_info.value == test_exception
        mock_logger.error.assert_called_once_with(
            "Falha ao gerar relatório: Erro de valor inválido"
        )
