from sortlab.settings import logger
from sortlab.pipeline import (
    AlgorithmRunner,
    ReportGenerator,
    ReportViewer,
    CleanupService,
)


def main() -> None:
    """Orquestra a execução dos algoritmos de ordenação, geração de relatório e limpeza.

    Esta função é o ponto de entrada principal do pipeline do SortLab:
    1. Executa algoritmos de ordenação pré-definidos.
    2. Gera um relatório com os resultados.
    3. Abre o relatório no navegador padrão.
    4. Remove arquivos temporários.

    Raises:
        Exception: Se qualquer etapa falhar, registra o erro e relança a exceção.
    """
    try:
        # 1. Executa os algoritmos de ordenação
        AlgorithmRunner.execute_default_algorithms()

        # 2. Gera o relatório
        ReportGenerator.generate_report()

        # 3. Abre o relatório no browser
        ReportViewer.open_report()

        # 4. Limpeza final
        CleanupService.clean_temp_files()

    except Exception as e:
        logger.error(f"Erro na execução principal: {e}")
        raise


if __name__ == "__main__":
    main()
