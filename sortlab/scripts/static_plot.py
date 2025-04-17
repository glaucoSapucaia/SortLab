import matplotlib

matplotlib.use('QtAgg') # backend alternativo ao tkinter

from logger import logger
import matplotlib.pyplot as plt
import seaborn as sns

from sortlab.errors import PlotStaticException
from paths import STATIC_FOLDER as data_folder

sns.set_theme(style="darkgrid")

def plot_static(vector_sizes: list[int], times: list[float],
                comparisons: list[int], algorithm_name: str) -> None:
    try:
        logger.info(f"Iniciando a criação do gráfico estático para o algoritmo {algorithm_name}.")

        # Definindo a paleta de cores do Seaborn
        color_palette = sns.color_palette("Set2", 2)

        # Criar figura e eixos
        _, axes = plt.subplots(1, 2, figsize=(12, 5))

        # Plotando o tempo de execução
        axes[0].plot(vector_sizes, times, marker='o', linestyle='-', color=color_palette[0], linewidth=2, markersize=6)
        axes[0].set_title(f'Execução - {algorithm_name}', fontsize=16, fontweight='bold')
        axes[0].set_xlabel('Tamanho do Vetor', fontsize=14)
        axes[0].set_ylabel('Tempo (s)', fontsize=14)
        axes[0].grid(True)
        axes[0].ticklabel_format(style='plain')  # Evita notação científica

        # Plotando as comparações/trocas
        axes[1].plot(vector_sizes, comparisons, marker='s', linestyle='--', color=color_palette[1], linewidth=2, markersize=6)
        axes[1].set_title(f'Comparações/Trocas - {algorithm_name}', fontsize=16, fontweight='bold')
        axes[1].set_xlabel('Tamanho do Vetor', fontsize=14)
        axes[1].set_ylabel('Comparações/Trocas', fontsize=14)
        axes[1].grid(True)
        axes[1].ticklabel_format(style='plain')

        # Ajustando o layout para não sobrepor os elementos
        plt.tight_layout()

        try:
            # Garantir que a pasta de saída exista
            data_folder.mkdir(parents=True, exist_ok=True)
            logger.info(f"Diretório {data_folder} criado com sucesso ou já existe.")
        except Exception as e:
            logger.error(f"Erro ao criar diretório {data_folder}: {e}")
            raise PlotStaticException(f"Erro ao criar diretório: {e}")

        output_path = data_folder / f'{algorithm_name}_estatico_.png'

        # Salvando a imagem com resolução ajustada
        try:
            plt.savefig(output_path, dpi=150)
            plt.close()
            logger.info(f"Gráfico estático salvo com sucesso em {output_path}.")
        except Exception as e:
            logger.error(f"Erro ao salvar gráfico estático em {output_path}: {e}")
            raise PlotStaticException(f"Erro ao salvar gráfico estático: {e}")

    except Exception as e:
        logger.error(f"Erro na função '{plot_static.__name__}': {e}")
        raise PlotStaticException(
            f"Erro na função '{plot_static.__name__}': {e}"
        ) from e
