from paths import config
import pytest
import os

# Configura o PYTHONPATH para o processo atual
os.environ['PYTHONPATH'] = str(config.get_path('PROJECT_ROOT'))

# Executa o pytest diretamente (isso roda no mesmo processo)
pytest.main([
    '--cov=sortlab.utils',
    '--cov-report=html',
    'sortlab/tests'
])