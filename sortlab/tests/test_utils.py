import pytest
from unittest import mock
from pathlib import Path
from sortlab.utils.metrics import MetricCounter
from sortlab.utils.delete_temp_files import clean_temp_files, static_folder

@pytest.fixture
def mock_folders():
    with mock.patch("sortlab.utils.delete_temp_files.static_folder", mock.MagicMock(spec=Path)) as static_folder, \
         mock.patch("sortlab.utils.delete_temp_files.interactive_images_folder", mock.MagicMock(spec=Path)) as interactive_images_folder, \
         mock.patch("sortlab.utils.delete_temp_files.links_page", mock.MagicMock(spec=Path)) as links_page, \
         mock.patch("sortlab.utils.delete_temp_files.temp_files", mock.MagicMock(spec=Path)) as temp_files:
        
        # Mocking the folders and their behavior
        static_folder.exists.return_value = True
        static_folder.iterdir.return_value = [mock.Mock()]
        
        interactive_images_folder.exists.return_value = True
        interactive_images_folder.iterdir.return_value = [mock.Mock()]
        
        links_page.exists.return_value = True
        temp_files.glob.return_value = [mock.Mock(is_file=mock.Mock(return_value=True))]
        
        yield static_folder, interactive_images_folder, links_page, temp_files

def test_clean_temp_files_removes_folders_and_files(mock_folders):
    static_folder, interactive_images_folder, links_page, temp_files = mock_folders

    # mocks individuais de .unlink() para cada path
    static_folder.unlink = mock.Mock()
    interactive_images_folder.unlink = mock.Mock()
    links_page.unlink = mock.Mock()

    temp_file_mock = mock.Mock()
    temp_file_mock.is_file.return_value = True
    temp_file_mock.unlink = mock.Mock()
    temp_files.glob.return_value = [temp_file_mock]

    with mock.patch("shutil.rmtree") as mock_rmtree:
        clean_temp_files()

        mock_rmtree.assert_any_call(static_folder)
        mock_rmtree.assert_any_call(interactive_images_folder)
        links_page.unlink.assert_called_once()
        temp_file_mock.unlink.assert_called_once()


def test_clean_temp_files_does_nothing_when_folders_are_empty(mock_folders):
    static_folder, interactive_images_folder, _, _ = mock_folders

    # Mockando os diretórios vazios
    static_folder.iterdir.return_value = []
    interactive_images_folder.iterdir.return_value = []
    
    with mock.patch("shutil.rmtree") as mock_rmtree, \
         mock.patch("pathlib.Path.unlink") as mock_unlink:
        
        clean_temp_files()
        
        # Verificar se nenhuma função de remoção foi chamada
        mock_rmtree.assert_not_called()
        mock_unlink.assert_not_called()

def test_clean_temp_files_handles_exceptions(mock_folders):
    static_folder, _, _, _ = mock_folders

    static_folder.exists.return_value = True
    static_folder.iterdir.return_value = [mock.Mock()]
    
    with mock.patch("shutil.rmtree", side_effect=Exception("Erro no rmtree")), \
         mock.patch("sortlab.utils.delete_temp_files.logger") as mock_logger:
        
        clean_temp_files()
        mock_logger.error.assert_called_once()



@pytest.fixture
def counter():
    return MetricCounter()

def test_initial_value(counter):
    """Testa se o valor inicial do contador é zero."""
    assert counter.count == 0

def test_increase(counter):
    """Testa o aumento do contador."""
    counter.increase()
    assert counter.count == 1
    counter.increase()
    assert counter.count == 2

def test_decrease(counter):
    """Testa a diminuição do contador."""
    counter.increase()  # Primeiro, incrementa para que o valor seja positivo
    counter.decrease()
    assert counter.count == 0

def test_decrease_when_zero(counter):
    """Testa que o contador não diminui abaixo de zero."""
    counter.decrease()
    assert counter.count == 0

def test_reset(counter):
    """Testa o reset do contador."""
    counter.increase()
    counter.reset()
    assert counter.count == 0

def test_set(counter):
    """Testa a definição de um valor específico para o contador."""
    counter.set(10)
    assert counter.count == 10
    counter.set(5)
    assert counter.count == 5
