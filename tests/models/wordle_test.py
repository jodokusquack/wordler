import pytest

from wordler.crud import create_wordle, delete_wordle, update_wordle


@pytest.fixture()
def test_wordle(test_db_session):
    wordle_data = {
        "wordle_id": 1715,
        "hard_mode": True,
        "solved": True,
        "guesses_needed": 4,
        "guesses": ("⬛️⬛️⬛️⬛️🟩\n" "⬛⬛️⬛️⬛️🟩\n" "⬛️🟨⬛️⬛️🟩\n" "🟩🟩🟩🟩🟩"),
    }
    wordle = create_wordle(test_db_session, **wordle_data)
    return wordle


class TestWordle:
    def test_create_wordle(self, test_db_session, test_wordle):
        pass

    def test_update_wordle(self, test_db_session, test_wordle):
        pass

    def test_delete_wordle(self, test_db_session, test_wordle):
        pass
