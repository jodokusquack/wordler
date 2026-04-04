import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from wordler.models import Base

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
