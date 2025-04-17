from logger import logger
import webbrowser

from paths import config

class ReportViewer:
    @staticmethod
    def open_report() -> None:
        try:
            pdf = config.get_path('REPORT_FILE')  # <-- agora está dentro do método
            logger.info(f"Abrindo relatório: {pdf}")
            webbrowser.open(str(pdf))
            logger.info("Relatório aberto com sucesso")
        except Exception as e:
            logger.error(f"Falha ao abrir relatório: {str(e)}")
            raise