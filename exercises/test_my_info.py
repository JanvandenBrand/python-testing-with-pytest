import pytest
from pathlib import Path
from unittest import mock
from unittest.mock import MagicMock
import my_info


def test_home_dir():
    with mock.patch.object(Path, "home", autospec=True) as MockPathHome:
        MockPathHome.return_value = "/users/fake_user"
        value = my_info.home_dir()
        assert value == "/users/fake_user"


# Add fixture
@pytest.fixture()
def mock_my_info():
    with mock.patch.object(
            my_info, "home_dir", autospec=True
            ) as mock_home_dir:
        yield mock_home_dir


def test_home_dir_fixture(mock_my_info):
    mock_my_info.return_value = "/users/fake_user"
    value = my_info.home_dir()
    assert value == "/users/fake_user"


def test_my_home_is_called():
    assert str(my_info.home_dir()) == str(Path.home())
