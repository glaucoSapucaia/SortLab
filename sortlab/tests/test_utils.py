from sortlab.utils import MetricCounter, clean_temp_files

import pytest
from unittest import mock
from pathlib import Path


@pytest.fixture
def mock_folders():
    """Fixture para simular diretórios usados nos testes."""
    with (
        mock.patch(
            "sortlab.utils.delete_temp_files.static_folder",
            new=mock.MagicMock(spec=Path),
        ) as static,
        mock.patch(
            "sortlab.utils.delete_temp_files.interactive_images_folder",
            new=mock.MagicMock(spec=Path),
        ) as interactive,
        mock.patch(
            "sortlab.utils.delete_temp_files.links_page", new=mock.MagicMock(spec=Path)
        ) as links,
        mock.patch(
            "sortlab.utils.delete_temp_files.temp_files", new=mock.MagicMock(spec=Path)
        ) as temp,
    ):
        # Configuração comum para todos os mocks
        for folder in (static, interactive, links):
            folder.exists.return_value = True
            folder.iterdir.return_value = [mock.Mock()]

        temp.glob.return_value = [mock.Mock(is_file=mock.Mock(return_value=True))]
        yield static, interactive, links, temp


def test_clean_temp_files(mock_folders):
    """Testa a limpeza de arquivos temporários em todos os diretórios."""
    static, interactive, links, temp = mock_folders
    file_mock = mock.Mock()
    temp.glob.return_value = [file_mock]

    with mock.patch("shutil.rmtree") as rmtree:
        clean_temp_files()

        rmtree.assert_any_call(static)
        rmtree.assert_any_call(interactive)
        links.unlink.assert_called_once()
        file_mock.unlink.assert_called_once()


def test_clean_empty_folders(mock_folders):
    """Verifica se diretórios vazios não são removidos."""
    static, interactive, _, _ = mock_folders
    static.iterdir.return_value = []
    interactive.iterdir.return_value = []

    with (
        mock.patch("shutil.rmtree") as rmtree,
        mock.patch("pathlib.Path.unlink") as unlink,
    ):
        clean_temp_files()
        rmtree.assert_not_called()
        unlink.assert_not_called()


def test_clean_temp_files_error(mock_folders, caplog):
    """Testa o tratamento de erros durante a limpeza de arquivos."""
    static, _, _, _ = mock_folders
    static.exists.return_value = True
    static.iterdir.side_effect = Exception("Test error")

    with pytest.raises(Exception) as exc_info:
        clean_temp_files()

    assert "Falha na limpeza de arquivos temporários: Test error" in caplog.text
    assert "Test error" in str(exc_info.value)


@pytest.fixture
def counter():
    """Fixture que fornece uma instância de MetricCounter para os testes."""
    return MetricCounter()


@pytest.mark.parametrize(
    "operation,expected",
    [
        (lambda c: c.increase(), 1),
        (lambda c: c.set(5), 5),
        (lambda c: c.reset(), 0),
    ],
)
def test_counter_operations(counter, operation, expected):
    """Testa operações básicas do contador (incrementar, definir valor e resetar)."""
    operation(counter)
    assert counter.count == expected


@pytest.mark.parametrize(
    "initial_value,expected",
    [
        (1, 0),  # Caso normal
        (2, 1),  # Valor maior que 1
        (0, 0),  # Valor zero (não deve decrementar)
        (-1, -1),  # Valor negativo (não deve decrementar)
    ],
)
def test_decrease_with_different_values(counter, initial_value, expected):
    """Testa o decremento do contador com diferentes valores iniciais."""
    counter.set(initial_value)
    counter.decrease()
    assert counter.count == expected


def test_multiple_decreases(counter):
    """Verifica o comportamento de múltiplos decrementos no contador."""
    counter.set(3)
    counter.decrease()
    assert counter.count == 2
    counter.decrease()
    assert counter.count == 1
    counter.decrease()
    assert counter.count == 0
    counter.decrease()  # Não deve ir abaixo de zero
    assert counter.count == 0


def test_counter_no_negative(counter):
    """Garante que o contador nunca fica negativo após decremento."""
    counter.decrease()
    assert counter.count == 0
    counter.set(-5)
    counter.decrease()
    assert (
        counter.count == -5
    )  # Assume que valores negativos são permitidos, mas não decrementados
