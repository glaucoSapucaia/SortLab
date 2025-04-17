import os
from settings.logger import logger
from sortlab.errors import PlotInteractiveException
import plotly.graph_objects as go

from settings.paths import config

html_folder = config.get_path('LINK_FOLDER')


def plot_interactive(vector_sizes: list[int], times: list[float],
                     comparisons: list[int], algorithm_name: str) -> None:
    try:
        logger.info(f"Iniciando a criação do gráfico interativo para o algoritmo {algorithm_name}.")

        times_microseconds = [t * 1_000_000 for t in times]

        fig = go.Figure()

        # Adicionando trace para tempo
        fig.add_trace(go.Scatter(
            x=vector_sizes,
            y=times_microseconds,
            mode='lines+markers',
            name='Tempo (μs)',
            line=dict(color='yellow', width=2),
            marker=dict(size=8),
            yaxis='y1'
        ))

        # Adicionando trace para comparações/trocas
        fig.add_trace(go.Scatter(
            x=vector_sizes,
            y=comparisons,
            mode='lines+markers',
            name='Comparações/Trocas',
            line=dict(color='orange', dash='dash', width=2),
            marker=dict(size=8, symbol='square'),
            yaxis='y2',
            hovertemplate='Tamanho: %{x}<br>Comparações/Trocas: %{y:,}',
        ))

        # Atualizando o layout do gráfico
        fig.update_layout(
            title=f'Desempenho do Algoritmo {algorithm_name}',
            xaxis=dict(title='Tamanho do Vetor'),
            yaxis=dict(
                title=dict(text='Tempo (μs)', font=dict(color='yellow')),
                tickfont=dict(color='yellow'),
                tickformat=".0f",
                autorange=True
            ),
            yaxis2=dict(
                title=dict(text='Comparações/Trocas', font=dict(color='orange')),
                tickfont=dict(color='orange'),
                overlaying='y',
                side='right',
                tickformat=",.0f",
                autorange=True
            ),
            hovermode='x unified',
            template='plotly_dark',
            width=1350,
            height=650,
            margin=dict(r=120),
            legend=dict(
                x=0.5,
                y=1.1,
                xanchor='center',
                yanchor='bottom',
                orientation='h',
                traceorder='normal',
                font=dict(size=12),
                bgcolor='rgba(0, 0, 0, 0)',
                borderwidth=1
            ),
        )

        # Criar diretório caso não exista
        try:
            os.makedirs(html_folder, exist_ok=True)
            logger.info(f"Diretório {html_folder} criado com sucesso ou já existe.")
        except Exception as e:
            logger.error(f"Erro ao criar diretório {html_folder}: {e}")
            raise PlotInteractiveException(f"Erro ao criar diretório: {e}")

        html_output_path = html_folder / f'{algorithm_name}_interativo_.html'

        # Remover arquivo existente, se necessário
        if os.path.exists(html_output_path):
            try:
                os.remove(html_output_path)
                logger.info(f"Arquivo existente {html_output_path} removido com sucesso.")
            except Exception as e:
                logger.error(f"Erro ao remover arquivo existente {html_output_path}: {e}")
                raise PlotInteractiveException(f"Erro ao remover arquivo existente: {e}")

        # Salvar gráfico como HTML
        try:
            fig.write_html(str(html_output_path))
            logger.info(f"Gráfico interativo salvo com sucesso em {html_output_path}.")
        except Exception as e:
            logger.error(f"Erro ao salvar gráfico HTML em {html_output_path}: {e}")
            raise PlotInteractiveException(f"Erro ao salvar gráfico HTML: {e}")

    except Exception as e:
        logger.error(f"Erro na função '{plot_interactive.__name__}': {e}")
        raise PlotInteractiveException(
            f"Erro na função '{plot_interactive.__name__}': {e}"
        ) from e
