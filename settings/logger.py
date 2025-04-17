from .paths import config

from typing import Literal
import logging
import os

LogLevel = int | str

# ==================== Paths ====================
log_folder = config.get_path("LOG_DIR")
all_logs = config.get_path("LOG_FILE")
warning_logs = config.get_path("WARNING_LOG_FILE")
error_logs = config.get_path("ERROR_LOG_FILE")

os.makedirs(log_folder, exist_ok=True)
if not log_folder.exists():
    raise FileNotFoundError(f"O diretório base {log_folder} não foi encontrado.")


# ==================== FILTRO DE NÍVEL EXATO ====================
class ExactLevelFilter(logging.Filter):
    """Filtra registros de log para capturar apenas um nível específico (ex: só WARNING)."""

    def __init__(self, level: LogLevel) -> None:
        """Inicializa o filtro com o nível desejado (ex: logging.WARNING)."""
        super().__init__()
        self.level = level

    def filter(self, record: logging.LogRecord) -> Literal[True, False]:
        """Retorna True se o nível do log for igual ao nível configurado."""
        return record.levelno == self.level


# ==================== CONFIGURAÇÃO DO LOGGER ====================
logger = logging.getLogger("SortLab")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# Handlers
app_handler = logging.FileHandler(all_logs, encoding="utf-8")
warning_handler = logging.FileHandler(warning_logs, encoding="utf-8")
error_handler = logging.FileHandler(error_logs, encoding="utf-8")
console_handler = logging.StreamHandler()

# Configuração dos handlers (sem docstrings, pois são configurações diretas)
app_handler.setLevel(logging.DEBUG)
app_handler.setFormatter(formatter)

warning_handler.setLevel(logging.WARNING)
warning_handler.addFilter(ExactLevelFilter(logging.WARNING))
warning_handler.setFormatter(formatter)

error_handler.setLevel(logging.ERROR)
error_handler.addFilter(ExactLevelFilter(logging.ERROR))
error_handler.setFormatter(formatter)

console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# Adiciona handlers
logger.addHandler(app_handler)
logger.addHandler(warning_handler)
logger.addHandler(error_handler)
logger.addHandler(console_handler)
