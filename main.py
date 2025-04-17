from sortlab.pipeline import (
    AlgorithmRunner,
    ReportGenerator,
    ReportViewer,
    CleanupService
)
from logger import logger

def main() -> None:
    try:
        # 1. Executa os algoritmos de ordenação
        AlgorithmRunner.execute_default_algorithms()
        
        # 2. Gera o relatório
        ReportGenerator.generate_report()
        
        # 3. Abre o relatório
        ReportViewer.open_report()
        
        # 4. Limpeza final
        CleanupService.clean_temp_files()
        
    except Exception as e:
        logger.error(f"Erro na execução principal: {e}")
        raise

if __name__ == "__main__":
    main()