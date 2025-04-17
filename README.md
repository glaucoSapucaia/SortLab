# SortLab  

**Projeto em Python** que executa algoritmos de ordenação, mede performance, exibe gráficos com Matplotlib (via PyQt5) e Plotly, e gera um relatório final em PDF contendo os dados e visualizações com o ReportLab.  

📌 **Funcionalidades**  
- Execução de algoritmos de ordenação com medição de tempo e comparações/trocas.  
- Geração de gráficos interativos (Plotly) e estáticos (Matplotlib).  
- Relatório em PDF com resultados consolidados.  
- Limpeza automática de arquivos temporários.  
- Suporte a múltiplos algoritmos via interface `ISorter`.  


🛠️ **Tecnologias Utilizadas**
- Python
- Matplotlib + PyQt6 para visualização gráfica
- Plotly para gráficos interativos
- ReportLab para geração de PDF
- Pytest-cov para testes


📦 **Instalação**  

Clone o repositório:

```bash
git clone https://github.com/glaucoSapucaia/SortLab.git .
```

Instale as dependências:

```bash
pip install -r requirements.txt  
```


▶️ **Como Executar**

**Execução Padrão** (com configurações pré-definidas)

Windows

```bash
python ./main.py
```

Linux

```bash
python3 ./main.py
```

Gera relatório PDF automaticamente e abre no navegador padrão.



**Personalização**  

Modifique os parâmetros em `sortlab.pipeline.execution.py` (tamanhos dos vetores):

```python
from sortlab.pipeline import AlgorithmRunner

# Vetores personalizados  
vector_sizes = [500, 1000, 1500]  
base_vector = [random.randint(0, 1000) for _ in range(max(vector_sizes))]  

AlgorithmRunner.run_algorithms(vector_sizes, base_vector)  
```

Crie novos algorítimos em `sortlab.functions` (exemplo: SelectionSort)

```python
from .shared_imports import *


class SelectionSort(ISorter):
    """Implementação do algoritmo de ordenação Selection Sort."""

    def __init__(self, counter: IMetricCounter) -> None:
        """Inicializa o Selection Sort com contador de métricas.

        Args:
            counter: Objeto para contabilizar comparações e trocas.
        """
        self.counter = counter
        logger.info(f"{self.__class__.__name__} inicializado com contador.")

    def selection_sort(self, arr: list[int]) -> list[int]:
        """Ordena a lista usando o algoritmo Selection Sort.

        Args:
            arr: Lista de inteiros a ser ordenada.

        Returns:
            Lista ordenada em ordem crescente.

        Raises:
            SortingException: Se ocorrer erro durante a ordenação.
        """
        try:
            for i in range(len(arr) - 1):
                _min = i
                for j in range(i + 1, len(arr)):
                    self.counter.increase()  # Contabiliza comparação
                    if arr[j] < arr[_min]:
                        _min = j

                if arr[i] != arr[_min]:
                    self.counter.increase()  # Contabiliza troca
                    arr[i], arr[_min] = arr[_min], arr[i]

            return arr

        except Exception as e:
            logger.error(f"Erro no {self.__class__.__name__}: {e}")
            raise SortingException(f"Erro no {self.__class__.__name__}: {e}")

    def sort(self, arr: list[int]) -> list[int]:
        """Interface pública para ordenação, implementando ISorter.

        Args:
            arr: Lista de inteiros a ser ordenada.

        Returns:
            Lista ordenada em ordem crescente.

        Raises:
            EmptyArrException: Se a lista estiver vazia.
            SortingException: Se ocorrer erro durante a ordenação.
        """
        try:
            if not arr:
                logger.warning(f"{self.__class__.__name__} - Lista vazia.")
                raise EmptyArrException(f"{self.__class__.__name__} - Lista vazia.")

            return self.selection_sort(arr)

        except SortingException:
            logger.error(f"Erro ao ordenar com {self.__class__.__name__}.")
            raise 
```


🏗️ **Estrutura do Código | sortlab.pipeline**

```
sortlab/  
├── pipeline/  
│   ├── algorithm_executor.py    # Executa algoritmos e gera gráficos  
│   ├── cleanup.py               # Limpeza de arquivos temporários  
│   ├── execution.py             # Ponto de entrada padrão  
│   ├── open_report.py           # Abre o relatório PDF  
│   └── report.py                # Gera o relatório final  
```


📊 **Exemplo de Saída**

Gráficos:

![Static Bucket Plot](docs/imgs/bucket_static.jpeg)

![Interactive Bucket Plot](docs/imgs/bucket_interactive.jpeg)


📝 **Principais Dependências**

- matplotlib==3.10.1
- plotly==6.0.1
- PyQt6==6.9.0
- reportlab==4.4.0

[Lista completa em requirements.txt]

📊 **Diagramas | sortlab.pipeline**

![Diagrama de Sequencias](docs/SortLabPipelineSequenceDiagram.png)

![Diagrama de Classes](docs/SortLabPipelineClassDiagram.png)

🤝 **Contribuição**

Faça um fork do projeto.

Adicione novos algoritmos (implementando ISorter).

Envie um PR!

**Desenvolvido com Python e** ❤️
