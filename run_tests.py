from paths import config
import pytest
import os

# Configura o PYTHONPATH para o processo atual
os.environ['PYTHONPATH'] = str(config.get_path('PROJECT_ROOT'))

# Executa o pytest diretamente (isso roda no mesmo processo)
# Altere o valor dos módulos para os testes!
pytest.main([
    '--cov=sortlab.pipeline',
    '--cov-report=html',
    'sortlab/tests'
])
