from sortlab.settings import logger
from sortlab.scripts import generate_pdf_report


class ReportGenerator:
    """Responsável pela geração do relatório final em formato PDF."""

    @staticmethod
    def generate_report() -> None:
        """Gera o relatório PDF com os resultados das ordenações.

        Executa o script de geração do relatório e trata possíveis erros.

        Raises:
            Exception: Se ocorrer falha na geração do relatório.
            Logs o erro antes de relançar a exceção.
        """
        try:
            logger.info("Gerando relatório PDF")
            generate_pdf_report()
            logger.info("Relatório gerado com sucesso")
        except Exception as e:
            logger.error(f"Falha ao gerar relatório: {str(e)}")
            raise
