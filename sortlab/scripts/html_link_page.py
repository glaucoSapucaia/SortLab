from settings.logger import logger
from settings.paths import config
from sortlab.errors import LinksPDFException

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from typing import TYPE_CHECKING
import inspect
import os


if TYPE_CHECKING:
    from pathlib import Path

html_folder = config.get_path("LINK_FOLDER")
temp_link = config.get_path("TEMP_LINK_PAGE")


def generate_html_links_page() -> "Path":
    """Gera um PDF com links clicáveis para os gráficos interativos em HTML.

    O PDF gerado contém:
    - Um título centralizado
    - Lista de links para cada arquivo HTML encontrado
    - Quebras de página automáticas quando necessário

    Returns:
        Path: Caminho para o PDF gerado com os links

    Raises:
        FileNotFoundError: Se o diretório não existir ou estiver vazio
        LinksPDFException: Se ocorrer qualquer erro durante a geração
    """
    try:
        logger.info(f"Verificando diretório {html_folder}")

        # Validação do diretório
        if not os.path.exists(html_folder):
            logger.error(f"Diretório {html_folder} não encontrado")
            raise FileNotFoundError(f"Diretório {html_folder} não encontrado")

        logger.info("Iniciando geração do PDF de links")

        # Configuração inicial do PDF
        c = canvas.Canvas(str(temp_link), pagesize=A4)
        width, height = A4

        # Cabeçalho
        c.setFont("Helvetica-Bold", 24)
        c.drawCentredString(width / 2, height - inch, "LINKS PARA GRÁFICOS INTERATIVOS")

        # Configuração dos links
        c.setFont("Helvetica", 16)
        y = height - 1.8 * inch
        spacing = 0.6 * inch

        # Processamento dos arquivos HTML
        html_files = sorted(os.listdir(html_folder))
        if not html_files:
            logger.warning(f"Nenhum HTML em {html_folder}")
            raise FileNotFoundError(f"Nenhum HTML em {html_folder}")

        logger.info(f"HTMLs encontrados: {html_files}")

        for filename in html_files:
            if filename.endswith(".html"):
                filepath = os.path.abspath(os.path.join(html_folder, filename))
                display_text = filename.replace("_interativo_.html", "")

                # Adiciona link ao PDF
                c.drawString(1.5 * inch, y, f"• {display_text}")
                c.linkURL(f"file://{filepath}", (1.5 * inch, y - 4, 6.5 * inch, y + 16))

                y -= spacing
                if y < inch:  # Quebra de página
                    c.showPage()
                    c.setFont("Helvetica", 16)
                    y = height - inch

        c.save()
        logger.info(f"PDF de links gerado em {temp_link}")
        return temp_link

    except Exception as e:
        logger.error(f"Erro ao gerar PDF de links: {e}")
        raise LinksPDFException(f"Erro em {inspect.currentframe().f_code.co_name}: {e}")
