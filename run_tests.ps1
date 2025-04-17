# Definir o PYTHONPATH para o diretório raiz do projeto
$env:PYTHONPATH="D:/estruturaDados"

# Rodar o pytest com a cobertura e o relatório em HTML
pytest --cov=sortlab.pipeline --cov-report=html sortlab/tests
