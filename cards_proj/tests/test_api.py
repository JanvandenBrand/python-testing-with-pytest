import cards
from cards import Card
import pytest


# Test Cases for count():
# I: non-trivial happy path tests
# II: Interesting sets of input
# III: Interesting starting states

# I: happy paths for count():
#1 (x) For an empty database count returns 0 -> trivial
#1a (v)  For a database with three elements count returns 3

# II: inputs for count()
#2 (x)  None, count() does not take any parameters

# III: States for count()
#3 (): Start states
#3a (): Empty database
#3b (): Database with one item
#3c (): Database with more than one item
#4 (): End states -> there are none
#5 (): Error States -> none

# Test plan:
# 3a, 3b, 3c fulfill all criteria
@pytest.fixture(scope="session")
def empty_db(temp_path_factory):
    """Start with an empty database
    """
    db_path = temp_path_factory.mktemp("cards_db")
    db_ = cards.CardDB(db_path)
    yield db_
    db_.close()

@pytest.fixture(scope="function")
def some_cards():
    """generate some test cards

    Yields:
        card: _description_
    """
    return [
        cards.Card("do the first thing", "John Doe", "to do"),
        cards.Card("do the second thing", "Jane Doe", "in prog"),
        cards.Card("do the third thing", "Someone else", "done")
    ]

@pytest.fixture(scope="session")
def db_with_one_item(temp_path_factory):
    """Start with an empty database
    """
    db_path = temp_path_factory.mktemp("cards_db")
    db_ = cards.CardDB(db_path)
    yield db_
    db_.close()


@pytest.fixture(scope="function")
def database_with_one_item(empty_db, some_cards):
    """Create a cards database with a single item

    Args:
        empty_db (_type_): database yielded from empty_db fixture
        some_cards (_type_): cards yielded from some_cards fixture
        number_of_cards
    """
    db_with_one_item = empty_db.add_card(some_cards[0])
    return db_with_one_item


@pytest.fixture(scope="function")
def database_more_than_one_item(empty_db, some_cards):
    """Create a cards database with a single item

    Args:
        empty_db (_type_): database yielded from empty_db fixture
        some_cards (_type_): cards yielded from some_cards fixture
        number_of_cards
    """
    for n in some_cards:
        db_with_more_than_one_item = empty_db.add_card(n)
    return db_with_more_than_one_item

@pytest.mark.parametrize(
    "cards_db, result", 
    [
        pytest.param(
            empty_db(), 0,
            id="empty database"
        ),
        pytest.param(
            database_with_one_item(), 1,
            id="databasee with one item"
        ),
        pytest.param(
            database_more_than_one_item(), 3,
            id="database with three items"
        )
    ]
)
def test_count(cards_db, result):
    expected = result
    actual = cards_db.count()
    assert expected == actual

# Test cases for add()
# I: non-trivial happy path tests
# 1: For an empty database add one item, with summary
# 2: For a database with more than one item add one, with summary


# II: Interesting sets of input
# 3: add a card with summary (required parameter) and owner

# III: Interesting starting states
# Error: MissingSummary
# 4: Add a card with missing summary
# 5: Add a duplicate card


# Test cases for add()
# I: non-trivial happy path tests
# delete a card from the a database with more than one item
# delete a card from the a database with  one item

# II: Interesting sets of input

# III: Interesting starting states
# delete a non-existant card

# Test Cases start() and finish() conditions
# I: non-trivial happy path tests
# 1: set start, in-prog, and done conditions
# 2: set finish from start, in prog and done conditions

# II: Interesting sets of input

# III: Interesting starting states
# 3: set invalid start id
# 4: set invalid finish id

# Test Cases for update(), list(), config(), version()
# I: non-trivial happy path tests
# 1: version returns the correct version
# 2: config returns the correct database path
# 3: return a list of cards from a databse with more than one item
# 4: return a list of cards from an empty database
#
# II: Interesting sets of input
# 5: update the owner of a card
# 6: update the status of a card
# 7: update the status and owner of a card
#
# III: Interesting starting states
# 8: update an invalid card
