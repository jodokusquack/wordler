import pytest

from wordler.models import User
from wordler.crud import create_user, delete_user, get_user_by_telegram_id


class TestUser:
    def test_create_user(self, test_db_session, test_user):
        """Test creating a new user."""
        # user gets created in test_user fixture

        # Assert: Check if the user was created
        db_user = test_db_session.query(User).filter_by(username=test_user.username).first()
        assert db_user is not None
        assert db_user.telegram_user_id == test_user.telegram_user_id

    def test_get_user_by_telegram_id(self, test_db_session, test_user):
        user = get_user_by_telegram_id(test_db_session, test_user.telegram_user_id)

        assert user is not None
        assert user.username == "test_user"

    def test_delete_user(self, test_db_session, test_user):
        result = delete_user(test_db_session, test_user.telegram_user_id)
        assert result is True

        user = get_user_by_telegram_id(test_db_session, test_user.telegram_user_id)
        assert user is None

    def test_cannot_create_user_with_identical_id(self, test_db_session, test_user):
        with pytest.raises(ValueError, match="already exists"):
            create_user(test_db_session, username=test_user.username, telegram_user_id=test_user.telegram_user_id)
