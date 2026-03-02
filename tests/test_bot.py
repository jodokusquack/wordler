import pytest
from unittest.mock import MagicMock, AsyncMock
from src.bot import reply_wordle
from shared_test_cases import test_cases


@pytest.fixture
def mock_update():
    update = AsyncMock()
    update.effective_message = MagicMock()
    return update


@pytest.mark.asyncio
async def test_valid_message_creates_db_entry(mock_update, mocker):
    # Mock the database connection
    mock_db_session = MagicMock()
    # mock SessionLocal to return a Mock Session that supports the context manager protocol
    mock_session = mocker.patch('src.database_connection.SessionLocal')
    mock_session.return_value.__enter__.return_value = mock_db_session

    # Set the message text to a valid test case
    mock_update.effective_message.text = test_cases['tc_success_1']

    # Call the handler
    await reply_wordle(mock_update, AsyncMock())

    # check if the session was used to add and commit a Wordle
    assert mock_db_session.add.call_count == 1
    assert mock_db_session.commit.call_count == 1

    # check the values of the added object
    added_result = mock_db_session.add.call_args[0][0]
    assert added_result.wordle_id == 1715
    assert added_result.solved is True


@pytest.mark.asyncio
async def test_invalid_message_does_not_create_db_entry(mock_update, mocker):
    # Mock the database connection
    mock_db_session = MagicMock()
    # mock SessionLocal to return a Mock Session that supports the context manager protocol
    mock_session = mocker.patch('src.database_connection.SessionLocal')
    mock_session.return_value.__enter__.return_value = mock_db_session

    # Set the message text to a valid test case
    mock_update.effective_message.text = test_cases['tc_wrong_text']

    # Call the handler
    await reply_wordle(mock_update, AsyncMock())

    # check that no entry was added or commited
    assert mock_db_session.add.call_count == 0
    assert mock_db_session.commit.call_count == 0
