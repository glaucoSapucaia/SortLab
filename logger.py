"""
Configuração do logger principal da aplicação DataWeaver.

Este módulo configura um logger com múltiplos *handlers* para registrar logs em diferentes arquivos,
de acordo com o nível da mensagem:

- app.log: registra todas as mensagens (INFO, WARNING, ERROR)
- warning.log: registra apenas mensagens de nível WARNING
- error.log: registra apenas mensagens de nível ERROR
- console: exibe mensagens a partir do nível INFO

A codificação dos arquivos de log é UTF-8 para evitar problemas com caracteres especiais.

Antes da configuração, o módulo garante que o diretório de logs existe, criando-o se necessário.

Também define a classe `ExactLevelFilter`, utilizada para garantir que certos arquivos
de log recebam apenas mensagens de um nível exato.
"""

import logging
import os

from paths import config


# paths
log_folder = config.get_path('LOG_DIR')
all_logs = config.get_path('LOG_FILE')
warning_logs = config.get_path('WARNING_LOG_FILE')
error_logs = config.get_path('ERROR_LOG_FILE')

# Criar diretório caso não exista
os.makedirs(log_folder, exist_ok=True)

# Verificar se o diretório existe
if not log_folder.exists():
    raise FileNotFoundError(f"O diretório base {log_folder} não foi encontrado.")

# ==================== FILTRO DE NÍVEL EXATO ====================

class ExactLevelFilter(logging.Filter):
    def __init__(self, level):
        super().__init__()
        self.level = level

    def filter(self, record):
        return record.levelno == self.level

# ==================== CONFIGURAÇÃO DO LOGGER ====================

logger = logging.getLogger("SortLab")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# ========== Handler: Todos os logs ==========

app_handler = logging.FileHandler(all_logs, encoding="utf-8")
app_handler.setLevel(logging.DEBUG)  # Captura tudo
app_handler.setFormatter(formatter)

# ========== Handler: Apenas WARNING ==========

warning_handler = logging.FileHandler(warning_logs, encoding="utf-8")
warning_handler.setLevel(logging.WARNING)
warning_handler.addFilter(ExactLevelFilter(logging.WARNING))
warning_handler.setFormatter(formatter)

# ========== Handler: Apenas ERROR ==========

error_handler = logging.FileHandler(error_logs, encoding="utf-8")
error_handler.setLevel(logging.ERROR)
error_handler.addFilter(ExactLevelFilter(logging.ERROR))
error_handler.setFormatter(formatter)

# ========== Handler: Console (INFO+) ==========

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# ========== Adiciona handlers ao logger ==========

logger.addHandler(app_handler)
logger.addHandler(warning_handler)
logger.addHandler(error_handler)
logger.addHandler(console_handler)
