from .interactive_plot import plot_interactive
from .static_plot import plot_static
from .full_plot import generate_pdf_report

from .static_plot import plot_static
from .interactive_plot import plot_interactive

def get_plot_functions():
    """Retorna todas as funções de plotagem disponíveis"""
    return [
        plot_static,
        plot_interactive
    ]

__all__ = ['plot_interactive', 'plot_static', 'generate_pdf_report']
