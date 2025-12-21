import pytest
from unittest.mock import AsyncMock
from tg_bot.adapters import AddictionToCalendarHandler
from tg_bot.domain import EditEventButton


@pytest.mark.asyncio
class TestAddictionToCalendarHandler:

        async def test_yandex_click(self):
            mock_sender = AsyncMock()
            handler = AddictionToCalendarHandler(mock_sender)
            callback = AsyncMock()
            callback.data = EditEventButton.EDIT_TO_YANDEX
            await handler.handle_for_calendar_addiction(callback)
            assert callback.answer.called is True
            assert mock_sender.send_text.called is True

        async def test_google_click(self):
            mock_sender = AsyncMock()
            handler = AddictionToCalendarHandler(mock_sender)
            callback = AsyncMock()
            callback.data = EditEventButton.EDIT_TO_GOOGLE
            await handler.handle_for_calendar_addiction(callback)
            assert callback.answer.called is True
            assert mock_sender.send_text.called is True

        async def test_ics_click(self):
            mock_sender = AsyncMock()
            handler = AddictionToCalendarHandler(mock_sender)
            callback = AsyncMock()
            callback.data = EditEventButton.MAKE_ICS
            await handler.handle_for_calendar_addiction(callback)
            assert callback.answer.called is True
            assert mock_sender.send_file.called is True