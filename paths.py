from pathlib import Path

# Diretórios principais do projeto
try:
    ############################## BASE ##############################

    BASE_DIR = Path(__file__).resolve().parent
    PROJECT_ROOT = BASE_DIR / 'sortlab'
    REPORT_FILE = PROJECT_ROOT / 'data' / 'relatorio_completo.pdf'

    ############################## PLOTS ##############################

    TEMP_FOLDER = PROJECT_ROOT / 'data'
    STATIC_FOLDER = PROJECT_ROOT / 'data' / 'plots' / 'static'
    INTERACTIVE_IMAGES_FOLDER = PROJECT_ROOT / 'data' / 'plots' / 'interactive' / 'images'

    def get_static_images() -> list[Path]:
        return list(STATIC_FOLDER.glob("*.png"))

    def get_interactive_images() -> list[Path]:
        return list(INTERACTIVE_IMAGES_FOLDER.glob("*.png"))

    ############################## PDF REPORTS ##############################

    FINAL_PDF_PATH = PROJECT_ROOT / 'data' / f"relatorio_completo.pdf"
    TEMP_PDF_PATH = PROJECT_ROOT / 'data' / 'temp_graficos.pdf'

    ############################## LINKS (HTML) REPORTS ##############################

    LINK_FOLDER = PROJECT_ROOT / 'data' / 'plots' / 'interactive' / 'html'
    LINKS_PAGE = PROJECT_ROOT / 'data' / 'plots' / 'interactive' / 'links.html'
    TEMP_LINK_PAGE = PROJECT_ROOT / 'data' / 'temp_links_page.pdf'

    ############################## LOGS #############################

    LOG_DIR = PROJECT_ROOT / 'logs'
    LOG_FILE = LOG_DIR / "app.log"
    ERROR_LOG_FILE = LOG_DIR / 'error.log'
    WARNING_LOG_FILE = LOG_DIR / 'warning.log'

    # Verificar se os diretórios existem
    if not BASE_DIR.exists():
        raise FileNotFoundError(f"O diretório base {BASE_DIR} não foi encontrado.")
    if not PROJECT_ROOT.exists():
        raise FileNotFoundError(f"O diretório do projeto {PROJECT_ROOT} não foi encontrado.")

except Exception as e:
    raise RuntimeError("Erro ao configurar os diretórios") from e
