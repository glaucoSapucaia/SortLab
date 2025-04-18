from sortlab.settings import *

import shutil

# Paths
static_folder = config.get_path("STATIC_FOLDER")
interactive_images_folder = config.get_path("INTERACTIVE_IMAGES_FOLDER")
links_page = config.get_path("LINKS_PAGE")
temp_files = config.get_path("TEMP_FOLDER")


def clean_temp_files() -> None:
    """Remove todos os arquivos e diretórios temporários gerados durante a execução.

    Limpeza inclui:
    - Gráficos estáticos (.png)
    - Imagens interativas temporárias
    - Página de links HTML
    - Arquivos temporários com prefixo 'temp_'

    Raises:
        Exception: Se ocorrer erro durante a limpeza (logado antes de ser relançado)
    """
    try:
        # Limpar gráficos estáticos
        if static_folder.exists() and any(static_folder.iterdir()):
            shutil.rmtree(static_folder)
            logger.info(f"Diretório de gráficos estáticos removido: {static_folder}")

        # Limpar imagens interativas
        if interactive_images_folder.exists() and any(
            interactive_images_folder.iterdir()
        ):
            shutil.rmtree(interactive_images_folder)
            logger.info(
                f"Diretório de imagens interativas removido: {interactive_images_folder}"
            )

        # Remover página de links
        if links_page.exists():
            links_page.unlink()
            logger.info(f"Página de links removida: {links_page}")

        # Limpar arquivos temporários
        temp_files_removed = 0
        for temp_file in temp_files.glob("temp_*"):
            if temp_file.is_file():
                temp_file.unlink()
                temp_files_removed += 1

        if temp_files_removed > 0:
            logger.info(f"Removidos {temp_files_removed} arquivos temporários")
        else:
            logger.info("Nenhum arquivo temporário encontrado para remoção")

    except Exception as e:
        logger.error(f"Falha na limpeza de arquivos temporários: {e}")
        raise
