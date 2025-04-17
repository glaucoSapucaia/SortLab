from logger import logger
from sortlab.scripts import generate_pdf_report

class ReportGenerator:
    @staticmethod
    def generate_report() -> None:
        try:
            logger.info("Gerando relatório PDF")
            generate_pdf_report()
            logger.info("Relatório gerado com sucesso")
        except Exception as e:
            logger.error(f"Falha ao gerar relatório: {str(e)}")
            raise