from sortlab.settings import config

import pytest
import os

# Configura o PYTHONPATH para o processo atual
os.environ["PYTHONPATH"] = str(config.get_path("BASE_DIR"))

# Executa o pytest diretamente (isso roda no mesmo processo)
pytest.main(["--cov=sortlab", "--cov-report=html", "sortlab/tests"])
