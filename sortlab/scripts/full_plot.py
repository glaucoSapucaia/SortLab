from logger import logger
from paths import (
    get_static_images,
    get_interactive_images,
    FINAL_PDF_PATH as pdf_output,
    TEMP_PDF_PATH as pdf_temp_path
)
from sortlab.errors import ImageSaveException, ImageSearchException, ReportException
from sortlab.scripts.html_link_page import generate_html_links_page
from typing import TYPE_CHECKING
from PyPDF2 import PdfMerger
from PIL import Image
import inspect

if TYPE_CHECKING:
    from pathlib import Path

def get_image_paths() -> list[str]:
    try:
        logger.info("Buscando imagens estáticas e interativas.")
        result = get_static_images() + get_interactive_images()
        logger.info(f"Imagens encontradas: {result}")
        return result
    except Exception as e:
        logger.error(f"Erro ao buscar imagens: {e}")
        raise ImageSearchException(f"Erro em {inspect.currentframe().f_code.co_name}: {e}")

def save_images_to_pdf(image_paths: list['Path'], temp_pdf_path: 'Path') -> None:
    try:
        logger.info("Iniciando o processo de conversão das imagens para PDF.")
        images = [Image.open(img).convert('RGB') for img in image_paths]
        if images:
            images[0].save(temp_pdf_path, save_all=True, append_images=images[1:])
            logger.info(f"PDF temporário gerado em: {temp_pdf_path}")
        else:
            logger.warning("Nenhuma imagem encontrada para salvar como PDF.")
    except Exception as e:
        logger.error(f"Erro ao salvar as imagens no PDF: {e}")
        raise ImageSaveException(f"Erro em {inspect.currentframe().f_code.co_name}: {e}")

def generate_pdf_report() -> None:
    try:
        logger.info("Iniciando a geração do relatório PDF.")

        # 1. Gerar PDF com links
        links_pdf = generate_html_links_page()

        # 2. Gerar PDF com imagens dos gráficos
        image_paths = get_image_paths()
        if image_paths:
            save_images_to_pdf(image_paths, pdf_temp_path)
        else:
            logger.warning("Nenhuma imagem encontrada para gerar o PDF com gráficos.")

        # 3. Mesclar os dois PDFs
        if links_pdf.exists() and pdf_temp_path.exists():
            logger.info("Mesclando os PDFs gerados.")
            merger = PdfMerger()
            merger.append(str(links_pdf))
            merger.append(str(pdf_temp_path))
            merger.write(pdf_output)
            merger.close()
            logger.info(f"Relatório PDF gerado com sucesso em: {pdf_output}")
        else:
            logger.error("Erro: um ou ambos os PDFs não foram gerados corretamente.")

    except Exception as e:
        logger.error(f"Erro ao gerar o relatório PDF: {e}")
        raise ReportException(f"Erro em {inspect.currentframe().f_code.co_name}: {e}")
