from logger import logger
import webbrowser

from paths import config

pdf = config.get_path('REPORT_FILE')

class ReportViewer:
    @staticmethod
    def open_report() -> None:
        try:
            logger.info(f"Abrindo relatório: {pdf}")
            webbrowser.open(str(pdf))
            logger.info("Relatório aberto com sucesso")
        except Exception as e:
            logger.error(f"Falha ao abrir relatório: {str(e)}")
            raise