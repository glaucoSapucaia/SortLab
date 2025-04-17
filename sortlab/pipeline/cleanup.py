from settings.logger import logger
from sortlab.utils.delete_temp_files import clean_temp_files

class CleanupService:
    @staticmethod
    def clean_temp_files() -> None:
        try:
            logger.info("Iniciando limpeza de arquivos temporários")
            clean_temp_files()
            logger.info("Limpeza concluída com sucesso")
        except Exception as e:
            logger.error(f"Falha na limpeza: {str(e)}")
            raise