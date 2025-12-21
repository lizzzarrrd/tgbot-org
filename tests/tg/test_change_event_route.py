import pytest
from unittest.mock import AsyncMock
from tg_bot.adapters import ChangeEventHandler
from tg_bot.domain import TransformEventButton


@pytest.mark.asyncio
class TestChangeEventHandler:

    async def test_init(self):
        mock_sender = AsyncMock()
        handler = ChangeEventHandler(mock_sender)
        assert handler.sender == mock_sender

    async def test_handle_change_name(self):
        mock_sender = AsyncMock()
        handler = ChangeEventHandler(mock_sender)
        callback = AsyncMock()
        callback.data = TransformEventButton.TRANSORM_NAME.value
        callback.message = AsyncMock()
        callback.message.edit_reply_markup = AsyncMock()
        state = AsyncMock()
        await handler.handle_for_event_changing_info(callback, state)
        assert mock_sender.send_text.called is True
        assert callback.answer.called is True
        assert state.set_state.called is True