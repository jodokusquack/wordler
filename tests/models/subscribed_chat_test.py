import pytest

from wordler.db.crud import (
    get_all_subscribed_chats,
    get_subscribed_chat,
    subscribe_chat,
    unsubscribe_chat,
)
from wordler.db.models import SubscribedChat

telegram_test_id = 1045401580


@pytest.fixture()
def test_chat(test_db_session):
    chat_data = {
        "telegram_chat_id": telegram_test_id,
    }
    chat = subscribe_chat(test_db_session, **chat_data)
    return chat


@pytest.fixture()
def test_multiple_chats(test_db_session):
    chat_data = [
        {"telegram_chat_id": telegram_test_id},
        {"telegram_chat_id": telegram_test_id + 1},
        {"telegram_chat_id": telegram_test_id + 2},
        {"telegram_chat_id": telegram_test_id + 3},
    ]
    chats = [subscribe_chat(test_db_session, **chat) for chat in chat_data]

    return chats


class TestSubscribedChat:
    def test_subscribe_chat(self, test_db_session, test_chat):
        # test chat gets subscribed in the test_chat fixture
        subscribed_chat = (
            test_db_session.query(SubscribedChat)
            .filter_by(telegram_chat_id=test_chat.telegram_chat_id)
            .first()
        )
        assert subscribed_chat is not None
        assert subscribed_chat.subscribed is True

    def test_get_subscribed_chat(self, test_db_session, test_chat):
        subscribed_chat = get_subscribed_chat(
            test_db_session, test_chat.telegram_chat_id
        )
        assert subscribed_chat is not None
        assert subscribed_chat.subscribed is True

    def test_get_all_subscribed_chats(self, test_db_session, test_multiple_chats):
        all_subscribed_chats = get_all_subscribed_chats(test_db_session)
        assert len(all_subscribed_chats) == len(test_multiple_chats)

        multiple_chat_ids = set([chat.telegram_chat_id for chat in test_multiple_chats])
        assert (
            set([chat.telegram_chat_id for chat in all_subscribed_chats])
            == multiple_chat_ids
        )

    def test_unsubscribe_chat(self, test_db_session, test_chat):
        result = unsubscribe_chat(test_db_session, test_chat.telegram_chat_id)
        assert result is True

        subscribed_chat = get_subscribed_chat(
            test_db_session, test_chat.telegram_chat_id
        )
        assert subscribed_chat is None

    def test_cannot_subscribe_identical_chat(self, test_db_session, test_chat):
        with pytest.raises(ValueError, match="already exists"):
            subscribe_chat(test_db_session, test_chat.telegram_chat_id)
