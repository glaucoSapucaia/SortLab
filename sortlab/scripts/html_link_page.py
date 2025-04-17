from logger import logger
from sortlab.errors import LinksPDFException
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch

from paths import config

html_folder = config.get_path('LINK_FOLDER')
temp_link = config.get_path('TEMP_LINK_PAGE')


from typing import TYPE_CHECKING
import inspect
import os

if TYPE_CHECKING:
    from pathlib import Path

def generate_html_links_page() -> 'Path':
    try:
        logger.info(f"Verificando a existência do diretório {html_folder} para arquivos HTML.")
        
        # Verificar se o diretório de arquivos HTML existe
        if not os.path.exists(html_folder):
            logger.error(f"O diretório {html_folder} não foi encontrado.")
            raise FileNotFoundError(f"O diretório {html_folder} não foi encontrado.")
        
        logger.info(f"Iniciando a geração do PDF com links interativos.")
        
        # Criar o canvas para gerar o PDF
        c = canvas.Canvas(str(temp_link), pagesize=A4)
        width, height = A4

        # Título grande
        c.setFont("Helvetica-Bold", 24)
        c.drawCentredString(width / 2, height - 1 * inch, "LINKS PARA GRÁFICOS INTERATIVOS")

        # Fonte maior para os links
        c.setFont("Helvetica", 16)

        y = height - 1.8 * inch
        spacing = 0.6 * inch  # espaço maior entre os links

        # Tentar listar os arquivos HTML
        html_files = sorted(os.listdir(html_folder))
        if not html_files:
            logger.warning(f"Nenhum arquivo HTML encontrado em {html_folder}.")
            raise FileNotFoundError(f"Nenhum arquivo HTML encontrado em {html_folder}.")

        logger.info(f"Arquivos HTML encontrados: {html_files}")
        
        for filename in html_files:
            if filename.endswith(".html"):
                filepath = os.path.abspath(os.path.join(html_folder, filename))
                display_text = filename.replace("_interativo_.html", "")

                # Texto do link
                c.drawString(1.5 * inch, y, f"• {display_text}")
                c.linkURL(
                    f"file://{filepath}",
                    (1.5 * inch, y - 4, 6.5 * inch, y + 16)
                )

                y -= spacing

                # Quebra de página se passar do limite
                if y < 1 * inch:
                    c.showPage()
                    c.setFont("Helvetica", 16)
                    y = height - 1 * inch

        c.save()
        logger.info(f"PDF com links gerado com sucesso em {temp_link}.")
        return temp_link

    except Exception as e:
        logger.error(f"Erro ao gerar o PDF com links interativos: {e}")
        raise LinksPDFException(f"Erro em {inspect.currentframe().f_code.co_name}: {e}")
