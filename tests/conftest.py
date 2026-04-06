import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from wordler.db.crud import create_user
from wordler.db.models import Base

engine = create_engine("sqlite:///:memory:")
# Create a session factory bound to the test engine
TestingSession = sessionmaker(bind=engine)


# Create an in-memory SQLite database for testing
@pytest.fixture(scope="function")
def test_db_session():
    Base.metadata.create_all(engine)  # Create all tables
    session = TestingSession()

    # Yield the session factory to the test
    yield session

    session.close()
    # Teardown: Drop all tables after the test
    Base.metadata.drop_all(engine)


@pytest.fixture()
def test_user(test_db_session):
    user_data = {
        "telegram_user_id": 12345,
        "username": "test_user",
    }
    user = create_user(test_db_session, **user_data)
    return user
