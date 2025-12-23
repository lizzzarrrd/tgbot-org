import pytest
from unittest.mock import AsyncMock, MagicMock
from aiogram import types

from tg_bot.adapters import MessageSender, StartHandler
from tg_bot.use_cases import BdInteractor
from tg_bot.domain import MessagesToUser


@pytest.fixture
def mock_sender():
    sender = MagicMock(spec=MessageSender)
    sender.send_text = AsyncMock()
    return sender


@pytest.fixture
def mock_db_interactor():
    interactor = MagicMock(spec=BdInteractor)
    interactor.get_or_create = AsyncMock()
    return interactor


@pytest.fixture
def mock_message():
    mock = MagicMock(spec=types.Message)
    mock_from_user = MagicMock()
    mock_from_user.id = 123456
    mock.from_user = mock_from_user
    return mock


@pytest.fixture
def start_handler(mock_sender, mock_db_interactor):
    return StartHandler(mock_sender, mock_db_interactor)


class TestStartHandler:
    
    @pytest.mark.asyncio
    async def test_init(self, mock_sender, mock_db_interactor):
        handler = StartHandler(mock_sender, mock_db_interactor)
        
        assert handler.sender == mock_sender
        assert handler.interactor_with_db == mock_db_interactor
    
    @pytest.mark.asyncio
    async def test_handle_sends_hi_message(
        self, start_handler, mock_sender, mock_message
    ):
        await start_handler.handle(mock_message)
        
        assert mock_sender.send_text.call_count == 2
        
        first_call = mock_sender.send_text.call_args_list[0]
        assert first_call[0][0] == mock_message
        assert first_call[1]['text'] == MessagesToUser.HI_MESSAGE
    
    @pytest.mark.asyncio
    async def test_handle_creates_user_in_db(
        self, start_handler, mock_db_interactor, mock_message
    ):
        await start_handler.handle(mock_message)
        
        mock_db_interactor.get_or_create.assert_called_once_with(123456)
    
    @pytest.mark.asyncio
    async def test_handle_with_different_user_id(
        self, mock_sender, mock_db_interactor
    ):
        handler = StartHandler(mock_sender, mock_db_interactor)
        message = MagicMock(spec=types.Message)
        message.from_user = MagicMock()
        message.from_user.id = 999999
        
        await handler.handle(message)
        
        mock_db_interactor.get_or_create.assert_called_once_with(999999)
        
        second_call = mock_sender.send_text.call_args_list[1]
        assert "999999" in second_call[1]['text']

