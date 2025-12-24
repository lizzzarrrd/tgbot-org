import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from tg_bot.adapters import AddictionToCalendarHandler
from tg_bot.domain import EditEventButton, MessagesToUser

HANDLER_MODULE = AddictionToCalendarHandler.__module__


@pytest.mark.asyncio
class TestAddictionToCalendarHandler:
    """Тесты для обработчика добавления событий в календари."""

    @pytest.fixture
    def mock_sender(self) -> AsyncMock:
        """Мок для отправителя сообщений."""
        return AsyncMock()

    @pytest.fixture
    def handler(self, mock_sender) -> AddictionToCalendarHandler:
        """Экземпляр тестируемого хендлера."""
        return AddictionToCalendarHandler(sender=mock_sender)

    @pytest.fixture
    def mock_state(self) -> AsyncMock:
        """Мок FSMContext с предустановленными данными события."""
        state = AsyncMock()
        state.get_data.return_value = {"event": {"dummy_key": "dummy_val"}}
        return state

    @pytest.fixture
    def mock_callback(self) -> AsyncMock:
        """Базовый мок для CallbackQuery."""
        callback = AsyncMock()
        callback.message = AsyncMock()
        callback.from_user.id = 12345
        return callback

    @pytest.fixture
    def mock_event_cls(self):
        """Патчит класс Event внутри модуля хендлера."""
        with patch(f"{HANDLER_MODULE}.Event") as mock:
            yield mock

    @pytest.fixture
    def mock_settings(self):
        """Патчит настройки (settings) внутри модуля хендлера."""
        with patch(f"{HANDLER_MODULE}.settings", new=MagicMock()) as mock:
            yield mock

    @pytest.fixture
    def mock_ics_writer(self):
        """Патчит функцию записи ICS файла."""
        with patch(f"{HANDLER_MODULE}.write_ics_for_project_event") as mock:
            mock.return_value = "/tmp/fake_event.ics"
            yield mock

    async def test_yandex_click(
        self,
        handler: AddictionToCalendarHandler,
        mock_sender: AsyncMock,
        mock_callback: AsyncMock,
        mock_state: AsyncMock,
        mock_event_cls: MagicMock,
    ):
        """Проверка нажатия кнопки 'Добавить в Яндекс'."""
        mock_callback.data = EditEventButton.EDIT_TO_YANDEX

        await handler.handle_for_calendar_addiction(mock_callback, mock_state)

        mock_callback.answer.assert_called_once()
        mock_sender.send_text.assert_called_once()

    async def test_google_click_not_configured(
        self,
        handler: AddictionToCalendarHandler,
        mock_sender: AsyncMock,
        mock_callback: AsyncMock,
        mock_state: AsyncMock,
        mock_event_cls: MagicMock,
        mock_settings: MagicMock,
    ):
        """Проверка нажатия 'Google', если не заданы настройки (client_id)."""
        mock_callback.data = EditEventButton.EDIT_TO_GOOGLE
        
        mock_settings.google_client_id = None

        await handler.handle_for_calendar_addiction(mock_callback, mock_state)

        mock_callback.answer.assert_called_once()
        mock_sender.send_text.assert_called_once()
        
        _, kwargs = mock_sender.send_text.call_args
        assert kwargs['text'] == MessagesToUser.PLUG

    async def test_ics_click(
        self,
        handler: AddictionToCalendarHandler,
        mock_sender: AsyncMock,
        mock_callback: AsyncMock,
        mock_state: AsyncMock,
        mock_event_cls: MagicMock,
        mock_ics_writer: MagicMock,
    ):
        """Проверка нажатия 'Скачать ICS'."""
        mock_callback.data = EditEventButton.MAKE_ICS

        await handler.handle_for_calendar_addiction(mock_callback, mock_state)

        mock_callback.answer.assert_called_once()
        mock_sender.send_file.assert_called_once()
        
        _, kwargs = mock_sender.send_file.call_args
        assert kwargs["file_path"] == "/tmp/fake_event.ics"