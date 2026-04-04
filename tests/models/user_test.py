import pytest

from wordler.models import User
from wordler.crud import create_user, delete_user, get_user_by_telegram_id


@pytest.fixture()
def test_user(test_db_session):
    user_data = {
        'user_id': 12345,
        'username': "test_user",
    }
    user = create_user(test_db_session, **user_data)
    return user


class TestUser:
    def test_create_user(self, test_db_session, test_user):
        """Test creating a new user."""
        # user gets created in test_user fixture

        # Assert: Check if the user was created
        db_user = test_db_session.query(User).filter_by(username="test_user").first()
        assert db_user is not None
        assert db_user.user_id == 12345

    def test_get_user_by_telegram_id(self, test_db_session, test_user):
        user = get_user_by_telegram_id(test_db_session, 12345)

        assert user is not None
        assert user.username == "test_user"

    def test_delete_user(self, test_db_session, test_user):
        delete_user(test_db_session, 12345)

        user = get_user_by_telegram_id(test_db_session, 12345)
        assert user is None
