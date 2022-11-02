from pathlib import Path
from tempfile import TemporaryDirectory
import cards
import pytest


# A problematic test:
# there is boiler plate code to set-up a database that we do not want to test
# there is a call to close the db before the assert that seems out of place
def test_empty():
    with TemporaryDirectory() as db_dir:
        # we need to point to the directory of the db
        db_path = Path(db_dir)
        # in order to call count we need a db object
        db = cards.CardsDB(db_path)

        count = db.count
        db.close()

        assert count == 0

# Fix: place the data outside the test with a fixture
@pytest.fixture()
def cards_db():
    # with assures that the tempdir stays around for the test
    with TemporaryDirectory() as db_dir:
        db_path = Path(db_dir)
        db = cards.CardsDB(db_path)
        yield db
        # after the test is done controls passes back to the fixture and the next bit is run
        db.close()


def test_emtpy_with_fixture(cards_db):
    assert cards_db.count() == 0

# Fixtures are reused
def test_two(cards_db):
    cards_db.add_card(cards.Card("first"))
    cards_db.add_card(cards.Card("seccond"))
    assert cards_db.count() == 2
