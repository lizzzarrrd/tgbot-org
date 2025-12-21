import pytest
from unittest.mock import AsyncMock
from tg_bot.adapters import ChangeEventHandler
from tg_bot.domain import TransformEventButton, MessageProcessingStates


@pytest.mark.asyncio
class TestChangeEventHandler:
    async def test_init(self):
        mock_sender = AsyncMock()
        handler = ChangeEventHandler(mock_sender)

        assert handler.sender == mock_sender

    async def test_handle_change_date(self):
        mock_sender = AsyncMock()
        handler = ChangeEventHandler(mock_sender)
        callback = AsyncMock()
        callback.data = TransformEventButton.TRANSORM_DATE
        state = AsyncMock()
        await handler.handle_for_event_changing_info(callback, state)
        state.set_state.assert_called_once_with(
            MessageProcessingStates.EDITING_DATE)
        assert callback.answer.called is True