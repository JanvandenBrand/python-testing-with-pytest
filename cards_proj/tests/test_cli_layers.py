"""
Mocking tested the implementation of the CLI, making sure a specific API 
call was called with specific parameters. The mixed-layer approach tests 
the behavior, making sure the outcome is what we want. This kind of 
approach is much less of a change detector and has a greater chance of 
remaining valid during refactoring. It does not require mocking.
"""

from typer.testing import CliRunner
from cards.cli import app
import pytest
import cards
import shlex


runner = CliRunner()


@pytest.fixture(scope="module")
def db_path(tmp_path_factory):
    db_path = tmp_path_factory.mktemp("cards_db")
    return db_path


@pytest.fixture()
def cards_db(db_path, monkeypatch):
    monkeypatch.setenv("CARDS_DB_DIR", str(db_path))
    db_ = cards.CardsDB(db_path)
    db_.delete_all()
    yield db_
    db_.close()


@pytest.fixture(scope="function")
def cards_db_with_cards(cards_db):
    cards_db.add_card(cards.Card("foo"))
    cards_db.add_card(cards.Card("bar"))
    cards_db.add_card(cards.Card("baz"))
    return cards_db


def cards_cli(command_string):
    """helper function to generate cli string inputs

    Args:
        command_string (_type_): the cards cli command string

    Returns:
        stdout: standard output
    """
    command_list = shlex.split(command_string)
    result = runner.invoke(app, command_list)
    output = result.stdout.rstrip()
    return output


def test_version():
    assert cards_cli("version") == cards.__version__


def test_config(db_path, cards_db):
    assert cards_cli("config") == str(db_path)


def test_config_normal_path(db_path):
    assert cards_cli("config") != str(db_path)


def test_count(cards_db_with_cards):
    assert cards_cli("count") == "3"


def test_start(cards_db):
    i = cards_db.add_card(cards.Card("some task"))
    cards_cli(f"start {i}")
    after = cards_db.get_card(i)
    assert after.state == "in prog"


def test_finish(cards_db):
    i = cards_db.add_card(cards.Card("another task"))
    cards_cli(f"finish {i}")
    after = cards_db.get_card(i)
    assert after.state == "done"


def test_add(cards_db):
    cards_cli("add some task -o brian")
    expected = cards.Card(summary="some task", owner="brian", state="todo")
    all_cards = cards_db.list_cards()
    assert len(all_cards) == 1
    assert all_cards[0] == expected


def test_delete(cards_db):
    i = cards_db.add_card(cards.Card("another task"))
    cards_cli(f"delete {i}")
    assert cards_db.count() == 0


# Error Cases
@pytest.mark.parametrize(
    "command",
    [
        "delete 25", 
        "start 25",
        "finish 25",
        "update 25 -s foo -o brian"
    ]
)
def test_invalid_card_id(cards_db, command):
    out = cards_cli(command)
    assert out == "Error: Invalid card id 25"


def test_missing_summary(cards_db):
    out = cards_cli("add")
    assert "Error: Missing argument 'SUMMARY...'" in out
