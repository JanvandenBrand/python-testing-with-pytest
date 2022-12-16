from unittest import mock
import shlex
import cards
import pytest
from typer.testing import CliRunner
from cards.cli import app


runner = CliRunner()


def cards_cli(command_string):
    command_list = shlex.split(command_string)
    result = runner.invoke(app, command_list)
    output = result.stdout.rstrip()
    return output


def test_typer_runner():
    result = runner.invoke(app, ["version"])
    print()
    print(f"version: {result.stdout}")

    result = runner.invoke(app, ["list", "-o", "brian"])
    print(f"list:\n{result.stdout}")


def test_mock_version():
    with mock.patch.object(cards, "__version__", "1.2.3"):
        result = runner.invoke(app, ["version"])
        assert result.stdout.rstrip() == "1.2.3"


def test_mock_CardsDB():
    with mock.patch.object(cards, "CardsDB") as MockCardsDB:
        print()
        print(f"class:{MockCardsDB}")
        print(f"return_value:{MockCardsDB.return_value}")
        with cards.cli.cards_db() as db:
            print(f"object: {db}")

# Test the the config command:
# cards config calls the cards_db() context manager. 
# In turn this:
# a) calls the get_path() function to return the db_path
# b) calls the CardsDB class associated with the db_path
# passes control back to config 
# config prints the path() method
def test_mock_path():
    with mock.patch.object(cards, "CardsDB") as MockCardsDB:
        MockCardsDB.return_value.path.return_value = "/foo/"
        with cards.cli.cards_db() as db:
            print()
            print(f"{db.path=}")
            print(f"{db.path()=}")


@pytest.fixture()
def mock_cardsdb():
    with mock.patch.object(cards, "CardsDB", autospec=True) as CardsDB:
        yield CardsDB.return_value


def test_config(mock_cardsdb):
    mock_cardsdb.path.return_value = "/foo/"
    result = runner.invoke(app, ["config"])
    assert result.stdout.rstrip() == "/foo/"


# count also prints a valiue and can be tested like condig
def test_count(mock_cardsdb):
    mock_cardsdb.count.return_value = 1
    result = runner.invoke(app, ["count"])
    assert result.stdout.rstrip() == "1"


# Add card doesn't return a value
# instead we need to verify that it is called correctly.
# card add should have the kwargs: summary, owner and state (default is to do)
def test_add_with_owner(mock_cardsdb):
    cards_cli("add some task -o brian")
    expected = cards.Card("some task", owner="brian", state="todo")
    mock_cardsdb.add_card.assert_called_with(expected)


# Handle errors with a mock
def test_delete_invalid(mock_cardsdb):
    mock_cardsdb.delete_card.side_effect = cards.api.InvalidCardId
    out = cards_cli("delete 25")
    assert "Error: Invalid card id 25" in out
