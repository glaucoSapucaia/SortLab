from sortlab.settings import *
from sortlab.errors import PlotStaticException

import matplotlib

matplotlib.use("QtAgg")  # Backend alternativo para evitar conflitos

import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="darkgrid")


data_folder = config.get_path("STATIC_FOLDER")


def plot_static(
    vector_sizes: list[int],
    times: list[float],
    comparisons: list[int],
    algorithm_name: str,
) -> None:
    """Gera e salva um gráfico estático com o desempenho do algoritmo.

    Cria uma figura com dois subplots lado a lado mostrando:
    - Tempo de execução em segundos (gráfico da esquerda)
    - Número de comparações/trocas (gráfico da direita)

    Args:
        vector_sizes: Lista de tamanhos de vetores testados
        times: Tempos de execução em segundos para cada tamanho
        comparisons: Número de operações para cada tamanho
        algorithm_name: Nome do algoritmo para títulos dos gráficos

    Raises:
        PlotStaticException: Se ocorrer erro durante a geração ou salvamento
    """
    try:
        logger.info(f"Criando gráfico estático para {algorithm_name}")

        # Configuração visual
        color_palette = sns.color_palette("Set2", 2)
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))

        # Gráfico de tempo de execução
        axes[0].plot(
            vector_sizes,
            times,
            marker="o",
            linestyle="-",
            color=color_palette[0],
            linewidth=2,
            markersize=6,
        )
        axes[0].set_title(
            f"Execução - {algorithm_name}", fontsize=16, fontweight="bold"
        )
        axes[0].set_xlabel("Tamanho do Vetor", fontsize=14)
        axes[0].set_ylabel("Tempo (s)", fontsize=14)
        axes[0].grid(True)
        axes[0].ticklabel_format(style="plain")

        # Gráfico de comparações/trocas
        axes[1].plot(
            vector_sizes,
            comparisons,
            marker="s",
            linestyle="--",
            color=color_palette[1],
            linewidth=2,
            markersize=6,
        )
        axes[1].set_title(
            f"Operações - {algorithm_name}", fontsize=16, fontweight="bold"
        )
        axes[1].set_xlabel("Tamanho do Vetor", fontsize=14)
        axes[1].set_ylabel("Comparações/Trocas", fontsize=14)
        axes[1].grid(True)
        axes[1].ticklabel_format(style="plain")

        plt.tight_layout()

        # Garantir diretório existe
        data_folder.mkdir(parents=True, exist_ok=True)

        # Caminho de saída
        output_path = data_folder / f"{algorithm_name}_estatico_.png"

        # Salvar figura
        plt.savefig(output_path, dpi=150)
        plt.close()
        logger.info(f"Gráfico salvo em {output_path}")

    except Exception as e:
        logger.error(f"Erro ao gerar gráfico estático: {e}")
        raise PlotStaticException(f"Erro ao gerar gráfico estático: {e}") from e
