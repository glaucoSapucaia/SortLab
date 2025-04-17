from pathlib import Path
from typing import TypeVar
import os

T = TypeVar("T")


class EnvConfig:
    """Gerenciador de configurações e paths do projeto."""

    def __init__(self) -> None:
        self.BASE_DIR = Path(__file__).resolve().parent.parent
        self.PROJECT_ROOT = self.BASE_DIR / "sortlab"

        # Paths principais
        data_dir = self.PROJECT_ROOT / "data"
        plots_dir = data_dir / "plots"
        logs_dir = self.PROJECT_ROOT / "logs"

        # Estrutura de diretórios
        self.REPORT_FILE = data_dir / "relatorio_completo.pdf"
        self.TEMP_FOLDER = data_dir
        self.STATIC_FOLDER = plots_dir / "static"
        self.INTERACTIVE_IMAGES_FOLDER = plots_dir / "interactive" / "images"
        self.FINAL_PDF_PATH = data_dir / "relatorio_completo.pdf"
        self.TEMP_PDF_PATH = data_dir / "temp_graficos.pdf"
        self.LINK_FOLDER = plots_dir / "interactive" / "html"
        self.LINKS_PAGE = plots_dir / "interactive" / "links.html"
        self.TEMP_LINK_PAGE = data_dir / "temp_links_page.pdf"
        self.LOG_DIR = logs_dir
        self.LOG_FILE = logs_dir / "app.log"
        self.ERROR_LOG_FILE = logs_dir / "error.log"
        self.WARNING_LOG_FILE = logs_dir / "warning.log"

        self._validate_paths()

    def _validate_paths(self) -> None:
        """Verifica diretórios essenciais."""
        if not self.BASE_DIR.exists():
            raise FileNotFoundError(f"Diretório base não encontrado: {self.BASE_DIR}")
        if not self.PROJECT_ROOT.exists():
            raise FileNotFoundError(
                f"Diretório do projeto não encontrado: {self.PROJECT_ROOT}"
            )

    def get(self, key: str, default: T | None = None) -> T | None:
        """Obtém configuração dinamicamente."""
        try:
            return getattr(self, key)
        except AttributeError:
            return os.getenv(key, default)

    def get_path(self, key: str) -> Path:
        """Obtém path garantido como objeto Path."""
        value = self.get(key)
        if value is None:
            raise KeyError(f"Configuração não encontrada: {key}")
        return Path(value) if not isinstance(value, Path) else value

    def get_static_images(self) -> list[Path]:
        return list(self.STATIC_FOLDER.glob("*.png"))

    def get_interactive_images(self) -> list[Path]:
        return list(self.INTERACTIVE_IMAGES_FOLDER.glob("*.png"))

    def set_env(self, key: str, value: str) -> None:
        """Define variável de ambiente."""
        os.environ[key] = value


# Instância global
config = EnvConfig()
