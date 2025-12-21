"""
Тесты для MessageHandler - основной ручки обработки сообщений
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from aiogram import types
from aiogram.fsm.context import FSMContext

from tg_bot.adapters import MessageSender
from tg_bot.domain import ConfirmKeyboard, MessagesToUser, MessageProcessingStates
from tg_bot.adapters import MessageHandler


@pytest.fixture
def mock_sender():
    sender = MagicMock(spec=MessageSender)
    sender.send_text = AsyncMock()
    return sender


@pytest.fixture
def handler(mock_sender):
    return MessageHandler(sender=mock_sender)


@pytest.fixture
def mock_message():
    message = MagicMock(spec=types.Message)
    message.text = "Тестовое сообщение"
    message.from_user = MagicMock()
    message.from_user.id = 12345
    return message


@pytest.fixture
def mock_state():
    state = MagicMock(spec=FSMContext)
    state.get_state = AsyncMock()
    state.clear = AsyncMock()
    return state


@pytest.fixture
def mock_keyboard():
    with patch.object(ConfirmKeyboard, 'build') as mock_build:
        mock_build.return_value = MagicMock()
        yield mock_build

class TestMessageHandlerEditingStates:
    
    @pytest.mark.asyncio
    async def test_handle_editing_date_state(
        self, handler, mock_message, mock_state, mock_sender, mock_keyboard
    ):
        mock_state.get_state.return_value = MessageProcessingStates.EDITING_DATE.state
        
        await handler.handle(mock_message, mock_state)
        
        mock_state.get_state.assert_called_once()
        mock_sender.send_text.assert_called_once()
        
        call_args = mock_sender.send_text.call_args
        assert call_args[0][0] == mock_message
        assert "PARSED FROM EGOR CHANGED DATE" in call_args[0][1]
        assert MessagesToUser.CONFIRM_BUTTON_MESSAGE in call_args[0][1]
        assert call_args[1]['reply_markup'] is not None
    
    @pytest.mark.asyncio
    async def test_handle_editing_time_state(
        self, handler, mock_message, mock_state, mock_sender, mock_keyboard
    ):
        mock_state.get_state.return_value = MessageProcessingStates.EDITING_TIME.state
        
        await handler.handle(mock_message, mock_state)
        
        mock_state.get_state.assert_called_once()
        mock_sender.send_text.assert_called_once()
        
        call_args = mock_sender.send_text.call_args
        assert "PARSED FROM EGOR CHANGED TIME" in call_args[0][1]
        assert MessagesToUser.CONFIRM_BUTTON_MESSAGE in call_args[0][1]
    
    @pytest.mark.asyncio
    async def test_handle_editing_name_state(
        self, handler, mock_message, mock_state, mock_sender, mock_keyboard
    ):
        mock_state.get_state.return_value = MessageProcessingStates.EDITING_NAME.state
        
        await handler.handle(mock_message, mock_state)
        
        mock_state.get_state.assert_called_once()
        mock_sender.send_text.assert_called_once()
        
        call_args = mock_sender.send_text.call_args
        assert "PARSED FROM EGOR CHANGED NAME" in call_args[0][1]
        assert MessagesToUser.CONFIRM_BUTTON_MESSAGE in call_args[0][1]
    
    @pytest.mark.asyncio
    async def test_handle_editing_description_state(
        self, handler, mock_message, mock_state, mock_sender, mock_keyboard
    ):
        mock_state.get_state.return_value = MessageProcessingStates.EDITING_DESCRIPTION.state
        
        await handler.handle(mock_message, mock_state)
        
        mock_state.get_state.assert_called_once()
        mock_sender.send_text.assert_called_once()
        mock_state.clear.assert_called_once()
        
        call_args = mock_sender.send_text.call_args
        assert "PARSED FROM EGOR CHANGED DESCRIPTION" in call_args[0][1]
        assert MessagesToUser.CONFIRM_BUTTON_MESSAGE in call_args[0][1]
    
    @pytest.mark.asyncio
    async def test_state_cleared_after_editing_description(
        self, handler, mock_message, mock_state, mock_sender, mock_keyboard
    ):
        mock_state.get_state.return_value = MessageProcessingStates.EDITING_DESCRIPTION.state
        
        await handler.handle(mock_message, mock_state)
        
        mock_state.clear.assert_called_once()

class TestMessageHandlerInitialization:
    def test_handler_initialization(self, mock_sender):
        handler = MessageHandler(sender=mock_sender)
        
        assert handler.sender == mock_sender
    
    def test_handler_requires_sender(self):
        with pytest.raises(TypeError):
            MessageHandler()
