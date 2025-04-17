from settings.logger import logger
from settings.paths import config

import webbrowser


class ReportViewer:
    """Responsável por abrir o relatório gerado no visualizador padrão do sistema."""

    @staticmethod
    def open_report() -> None:
        """Abre o arquivo do relatório PDF no navegador padrão do sistema.

        Obtém o caminho do arquivo de relatório das configurações e tenta abri-lo
        usando o navegador padrão do sistema.

        Raises:
            Exception: Se ocorrer qualquer erro ao tentar abrir o arquivo.
            Logs o erro antes de relançar a exceção.
        """
        try:
            pdf = config.get_path("REPORT_FILE")
            logger.info(f"Abrindo relatório: {pdf}")
            webbrowser.open(str(pdf))
            logger.info("Relatório aberto com sucesso")
        except Exception as e:
            logger.error(f"Falha ao abrir relatório: {str(e)}")
            raise
