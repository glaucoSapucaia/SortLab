from settings.logger import logger
from settings.paths import config
from sortlab.errors import PlotInteractiveException

import plotly.graph_objects as go
import os


html_folder = config.get_path("LINK_FOLDER")


def plot_interactive(
    vector_sizes: list[int],
    times: list[float],
    comparisons: list[int],
    algorithm_name: str,
) -> None:
    """Gera e salva um gráfico interativo HTML com o desempenho do algoritmo.

    Cria um gráfico duplo com eixos Y separados mostrando:
    - Tempo de execução em microssegundos (eixo Y esquerdo)
    - Número de comparações/trocas (eixo Y direito)

    Args:
        vector_sizes: Lista de tamanhos de vetores testados
        times: Lista de tempos de execução em segundos
        comparisons: Lista de comparações/trocas realizadas
        algorithm_name: Nome do algoritmo para título do gráfico

    Raises:
        PlotInteractiveException: Se ocorrer qualquer erro durante a geração
    """
    try:
        logger.info(f"Criando gráfico interativo para {algorithm_name}")

        # Converter tempos para microssegundos
        times_microseconds = [t * 1_000_000 for t in times]

        fig = go.Figure()

        # Adicionar traço para tempo de execução
        fig.add_trace(
            go.Scatter(
                x=vector_sizes,
                y=times_microseconds,
                mode="lines+markers",
                name="Tempo (μs)",
                line=dict(color="yellow", width=2),
                marker=dict(size=8),
                yaxis="y1",
            )
        )

        # Adicionar traço para comparações
        fig.add_trace(
            go.Scatter(
                x=vector_sizes,
                y=comparisons,
                mode="lines+markers",
                name="Comparações/Trocas",
                line=dict(color="orange", dash="dash", width=2),
                marker=dict(size=8, symbol="square"),
                yaxis="y2",
                hovertemplate="Tamanho: %{x}<br>Comparações/Trocas: %{y:,}",
            )
        )

        # Configurar layout do gráfico
        fig.update_layout(
            title=f"Desempenho do {algorithm_name}",
            xaxis=dict(title="Tamanho do Vetor"),
            yaxis=dict(
                title=dict(text="Tempo (μs)", font=dict(color="yellow")),
                tickfont=dict(color="yellow"),
                tickformat=".0f",
                autorange=True,
            ),
            yaxis2=dict(
                title=dict(text="Comparações/Trocas", font=dict(color="orange")),
                tickfont=dict(color="orange"),
                overlaying="y",
                side="right",
                tickformat=",.0f",
                autorange=True,
            ),
            hovermode="x unified",
            template="plotly_dark",
            width=1350,
            height=650,
            margin=dict(r=120),
            legend=dict(
                x=0.5,
                y=1.1,
                xanchor="center",
                yanchor="bottom",
                orientation="h",
            ),
        )

        # Criar diretório se não existir
        os.makedirs(html_folder, exist_ok=True)

        # Definir caminho do arquivo
        html_output_path = html_folder / f"{algorithm_name}_interativo_.html"

        # Remover arquivo existente
        if os.path.exists(html_output_path):
            os.remove(html_output_path)

        # Salvar gráfico como HTML
        fig.write_html(str(html_output_path))
        logger.info(f"Gráfico salvo em {html_output_path}")

    except Exception as e:
        logger.error(f"Erro ao gerar gráfico: {e}")
        raise PlotInteractiveException(f"Erro ao gerar gráfico: {e}") from e
