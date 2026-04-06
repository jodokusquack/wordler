from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from tests.shared_test_cases import test_cases
from wordler.bot import reply_wordle
from wordler.db.models import Wordle


@pytest.fixture
def mock_update():
    return AsyncMock()


@pytest.mark.asyncio
async def test_valid_message_creates_db_entry(test_db_session, mock_update, mocker):
    # Set the message text to a valid test case
    message = MagicMock()
    message.text = test_cases["tc_success_1"]
    mock_update.effective_message = message
    # Set the user to the correct one
    user = MagicMock()
    user.id = 1
    user.username = "test_user"
    user.first_name = "Test"
    mock_update.effective_user = user
    # Set a correct date
    mock_update.message.date = datetime.now()

    # Call the handler
    await reply_wordle(mock_update, MagicMock(), session=test_db_session)

    # check the values of the added object
    wordle_entry = test_db_session.query(Wordle).filter_by(wordle_id=1715).first()
    assert wordle_entry is not None
    assert wordle_entry.solved is True


@pytest.mark.asyncio
async def test_invalid_message_does_not_create_db_entry(
    test_db_session, mock_update, mocker
):
    # Set the message text to an invalid test case
    mock_update.effective_message.text = test_cases["tc_wrong_text"]

    # Call the handler
    await reply_wordle(mock_update, MagicMock(), session=test_db_session)

    # check that no entry was added or commited
    wordle_entry = test_db_session.query(Wordle).all()
    assert len(wordle_entry) == 0
