from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from tests.shared_test_cases import test_cases

# Import your handler and models
from wordler.db.crud import get_user_by_telegram_id, get_wordle
from wordler.db.models import Wordle
from wordler.handlers.message_handlers import reply_wordle


@pytest.mark.asyncio
async def test_reply_wordle_success(test_db_session):
    """Test that a valid Wordle string creates a user and a Wordle record."""

    # 1. Mock the Telegram Update and Message
    mock_update = MagicMock()
    mock_update.effective_message.text = test_cases["tc_success_1"]
    mock_update.effective_user.id = 12345
    mock_update.effective_user.username = "TestUser"
    mock_update.effective_user.mention_html.return_value = "@TestUser"
    mock_update.message.date = datetime.now()

    # Mock the reply function
    mock_update.message.reply_html = AsyncMock()

    mock_context = MagicMock()

    # 2. Call the handler directly (bypassing the decorator's automatic session)
    # Use .__wrapped__ to avoid the decorator creating a real production DB session
    await reply_wordle.__wrapped__(
        update=mock_update, context=mock_context, session=test_db_session
    )

    # 3. Assertions
    # Check User was created
    user = get_user_by_telegram_id(test_db_session, telegram_user_id=12345)
    assert user is not None
    assert user.username == "TestUser"

    # Check Wordle was created
    wordle = get_wordle(test_db_session, wordle_id=1715, user_id=user.id)
    assert wordle is not None
    assert wordle.wordle_id == 1715
    assert wordle.guesses_needed == 4

    # Check the bot replied with success
    mock_update.message.reply_html.assert_called_once()
    args, _ = mock_update.message.reply_html.call_args
    assert "Succesfully registered" in args[0]


@pytest.mark.asyncio
async def test_reply_wordle_invalid_text(test_db_session):
    """Test that 'Cool story bro' is returned and no Wordle is created for junk text."""

    mock_update = MagicMock()
    mock_update.effective_message.text = test_cases["tc_wrong_text"]
    mock_update.effective_user.id = 99999
    mock_update.effective_user.username = "Spammer"
    mock_update.message.reply_html = AsyncMock()

    mock_context = MagicMock()

    await reply_wordle.__wrapped__(mock_update, mock_context, session=test_db_session)

    # Assertions
    # no user should be created
    user = get_user_by_telegram_id(test_db_session, telegram_user_id=99999)
    assert user is None

    # Wordle should NOT be created
    wordle_count = test_db_session.query(Wordle).count()
    assert wordle_count == 0

    # Check for the "Cool story bro" reply
    args, _ = mock_update.message.reply_html.call_args
    assert "Cool story bro" in args[0]


@pytest.mark.asyncio
async def test_duplicate_wordle_submission_fails(test_db_session):
    """Test that submitting the same Wordle ID for the same user twice fails."""

    # 1. Setup shared data
    user_id = 555
    wordle_text = test_cases["tc_success_1"]

    # Mock the Update and Context
    mock_update = MagicMock()
    mock_update.effective_user.id = user_id
    mock_update.effective_user.username = "DoublePlayer"
    mock_update.message.date = datetime.now()
    mock_update.message.reply_html = AsyncMock()
    mock_context = MagicMock()

    # 2. First Submission: Should succeed
    mock_update.effective_message.text = wordle_text
    await reply_wordle.__wrapped__(mock_update, mock_context, session=test_db_session)
    # manually commit the session after the first call which should be succesful.
    test_db_session.commit()

    # Verify first entry exists
    assert test_db_session.query(Wordle).count() == 1

    # 3. Second Submission: Same Wordle ID, same User
    # The handler logic catches the error and sets a specific message
    mock_update.effective_message.text = wordle_text
    await reply_wordle.__wrapped__(mock_update, mock_context, session=test_db_session)

    # 4. Assertions
    # Count should still be 1 (the second one was never saved/committed)
    assert test_db_session.query(Wordle).count() == 1

    # Check the bot's reply message for the "already registered" text
    args, _ = mock_update.message.reply_html.call_args
    assert "already has a Wordle registered" in args[0]
