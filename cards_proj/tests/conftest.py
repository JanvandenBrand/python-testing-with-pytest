import cards
from cards import Card
import pytest
import faker

# Dynamic scoping
# Use case: we do not want to rely on a function call in the package during testing
def db_scope(fixture_name, config):
    if config.getoption("--func-db", None):
        return "function"
    return "session"


@pytest.fixture(scope=db_scope)
def db(tmp_path_factory):
    """CardsDB object connected to a temporary database using a built-in fixture
    """
    db_path = tmp_path_factory.mktemp("cards_db")
    db_ = cards.CardsDB(db_path)
    yield db_
    db_.close()


# @pytest.fixture(scope="session")
# def db():
#     """CardsDB object connected to a temporary database
#     """
#     with TemporaryDirectory() as db_dir:
#         db_path = Path(db_dir)
#         db_ = cards.CardsDB(db_path)
#         yield db_
#         db_.close()


# write a plugin for pytest
def pytest_addoption(parser):
    parser.addoption(
        "--func-db",
        action="store_true",
        default=False,
        help="new db for each test",
    )


# # The database is emptied with every test function that calls cards_db
@pytest.fixture(scope="function")
def cards_db(cards_db, request, faker):
    """Empty the database before every test

    Args:
        session_cards_db (DataBase): consumes the db object from the db fixture
        request ():
        faker ():
    """
    db = cards_db
    db.delete_all()
    
    faker.seed_instance(101)
    m = request.node.get_closest_marker("num_cards")
    if m and len(m.args) > 0:
        num_cards = m.args[0]
        for _ in range(num_cards):
            db.add_card(
                Card(
                    summary=faker.sentence(),
                    owner=faker.first_name()   
                )
            )

    return db


@pytest.fixture(scope="session")
def some_cards():
    """Create some cards and return them for testing
    """
    return [
        cards.Card("write book", "Brian", "done"),
        cards.Card("edit book", "Brian", "done"),
        cards.Card("write 2nd edition", "Brian", "todo"),
        cards.Card("edit 2nd edition", "Katie", "todo"),
    ]

# multiple fixtures used in a fixture (YO DAWG)
@pytest.fixture(scope="function")
def non_empty_db(cards_db, some_cards):
    """CardsDB object populated with some cards

    Args:
        cards_db (object): database yielded from db fixture
        some_cards (list): a list of cards yielded from some_cards fixture
    """
    for c in some_cards:
        cards_db.add_card(c)
    return cards_db
