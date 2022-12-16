import pytest
from pathlib import Path
from unittest import mock
import my_info


# Add fixture


def test_home_dir():
    with mock.patch.object(Path, "home", autospec=True) as MockPathHome:
        MockPathHome.return_value = "/users/fake_user"
        value = my_info.home_dir()
        assert value == "/users/fake_user"


def test_my_home_is_called():
    my_info.home_dir()