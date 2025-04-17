import shutil
from logger import logger

from paths import config

static_folder = config.get_path('STATIC_FOLDER')
interactive_images_folder = config.get_path('INTERACTIVE_IMAGES_FOLDER')
links_page = config.get_path('LINKS_PAGE')
temp_files = config.get_path('TEMP_FOLDER')


def clean_temp_files() -> None:
    try:
        # Remover diretório de imagens estáticas (temp gráficos)
        if static_folder.exists() and any(static_folder.iterdir()):  # Verifica se o diretório não está vazio
            shutil.rmtree(static_folder)
            logger.info(f"Removido: {static_folder}")

        # Remover diretório de imagens interativas (pngs)
        if interactive_images_folder.exists() and any(interactive_images_folder.iterdir()):  # Verifica se o diretório não está vazio
            shutil.rmtree(interactive_images_folder)
            logger.info(f"Removido: {interactive_images_folder}")

        # Remover página de links
        if links_page.exists():
            links_page.unlink()
            logger.info(f"Removido: {links_page}")

        # Remover arquivos que começam com 'temp_' na pasta de gráficos interativos
        for temp_file in temp_files.glob("temp_*"):
            if temp_file.is_file():
                temp_file.unlink()
                logger.info(f"Removido: {temp_file}")

    except Exception as e:
        logger.error(f"Erro ao limpar arquivos temporários: {e}")
