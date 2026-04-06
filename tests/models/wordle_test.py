from datetime import datetime

import pytest
from sqlalchemy import select

from wordler.crud import create_wordle, delete_wordle, get_wordle, update_wordle
from wordler.models import Wordle


@pytest.fixture()
def test_wordle(test_db_session, test_user):
    wordle_data = {
        "timestamp": None,
        "wordle_id": 1715,
        "hard_mode": True,
        "solved": True,
        "guesses_needed": 4,
        "guesses": ("⬛️⬛️⬛️⬛️🟩\n" "⬛⬛️⬛️⬛️🟩\n" "⬛️🟨⬛️⬛️🟩\n" "🟩🟩🟩🟩🟩"),
        "user_id": test_user.telegram_user_id,
    }
    wordle = create_wordle(test_db_session, **wordle_data)
    return wordle


class TestWordle:
    def test_create_wordle(self, test_db_session, test_wordle):
        stmt = select(Wordle).where(Wordle.wordle_id == test_wordle.wordle_id)
        wordle = test_db_session.scalar(stmt)

        assert wordle is not None
        assert wordle.wordle_id == test_wordle.wordle_id
        assert wordle.user_id == test_wordle.user_id
        assert wordle.solved is True

    def test_get_wordle(self, test_db_session, test_wordle):
        wordle = get_wordle(test_db_session, test_wordle.wordle_id, test_wordle.user_id)

        assert wordle is not None
        assert wordle.hard_mode == test_wordle.hard_mode
        assert wordle.guesses == test_wordle.guesses

    def test_get_nonexistent_wordle(self, test_db_session, test_wordle):
        non_existent_wordle = get_wordle(test_db_session, wordle_id=123, user_id=123)

        assert non_existent_wordle is None

    def test_update_wordle(self, test_db_session, test_wordle):
        timestamp = datetime.now()
        update_wordle(
            test_db_session,
            wordle_id=test_wordle.wordle_id,
            user_id=test_wordle.user_id,
            timestamp=timestamp,
            hard_mode=False,
            solved=False,
            guesses_needed=2,
            guesses="Test Guess String",
        )

        wordle = get_wordle(test_db_session, test_wordle.wordle_id, test_wordle.user_id)

        assert wordle.timestamp == timestamp
        assert wordle.hard_mode is False
        assert wordle.solved is False
        assert wordle.guesses_needed == 2
        assert wordle.guesses == "Test Guess String"

    def test_partial_update_wordle(self, test_db_session, test_wordle):
        update_wordle(
            test_db_session,
            wordle_id=test_wordle.wordle_id,
            user_id=test_wordle.user_id,
            guesses_needed=10,
        )

        wordle = get_wordle(test_db_session, test_wordle.wordle_id, test_wordle.user_id)

        assert wordle.guesses_needed == 10
        assert wordle.solved is True
        assert wordle.guesses is test_wordle.guesses

    def test_delete_wordle(self, test_db_session, test_wordle):
        result = delete_wordle(
            test_db_session,
            wordle_id=test_wordle.wordle_id,
            user_id=test_wordle.user_id,
        )

        assert result is True

        wordle = get_wordle(
            test_db_session,
            wordle_id=test_wordle.wordle_id,
            user_id=test_wordle.user_id,
        )
        assert wordle is None
