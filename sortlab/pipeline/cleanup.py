from sortlab.settings import logger
from sortlab.utils.delete_temp_files import clean_temp_files


class CleanupService:
    """Serviço para limpeza de arquivos temporários do sistema."""

    @staticmethod
    def clean_temp_files() -> None:
        """Remove todos os arquivos temporários do diretório configurado.

        Raises:
            Exception: Se ocorrer algum erro durante a limpeza.
            Logs do erro antes de relançar a exceção.
        """
        try:
            logger.info("Iniciando limpeza de arquivos temporários")
            clean_temp_files()
            logger.info("Limpeza concluída com sucesso")
        except Exception as e:
            logger.error(f"Falha na limpeza: {str(e)}")
            raise
