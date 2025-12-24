import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from tg_bot.infra.main import main

MAIN_MODULE = "tg_bot.infra.main"

@pytest.mark.asyncio
class TestMainEntrypoint:

    @pytest.fixture
    def mock_engine(self):
        with patch(f"{MAIN_MODULE}.engine") as mock_engine:
            mock_conn = AsyncMock()
            mock_context_manager = AsyncMock()
            mock_context_manager.__aenter__.return_value = mock_conn
            mock_engine.begin.return_value = mock_context_manager
            yield mock_engine, mock_conn

    @pytest.fixture
    def mock_base(self):
        with patch(f"{MAIN_MODULE}.Base") as mock:
            yield mock

    @pytest.fixture
    def mock_init_route(self):
        with patch(f"{MAIN_MODULE}.InitRoute") as mock:
            yield mock

    @pytest.fixture
    def mock_bot(self):
        with patch(f"{MAIN_MODULE}.bot") as mock:
            mock.delete_webhook = AsyncMock()
            yield mock

    @pytest.fixture
    def mock_dp(self):
        with patch(f"{MAIN_MODULE}.dp") as mock:
            mock.start_polling = AsyncMock()
            yield mock

    @pytest.fixture
    def mock_oauth(self):
        with patch(f"{MAIN_MODULE}.start_google_oauth_server", new_callable=AsyncMock) as mock:
            yield mock

    @pytest.fixture
    def mock_cleanup_task(self):
        """
        Мокаем задачу очистки как MagicMock (обычную функцию),
        чтобы она возвращала фиксированный объект, а не новую корутину.
        """
        with patch(f"{MAIN_MODULE}.cleanup_oauth_states_task", new_callable=MagicMock) as mock:
            mock.return_value = "dummy_coro_obj"
            yield mock

    @pytest.fixture
    def mock_asyncio_create_task(self):
        with patch(f"{MAIN_MODULE}.asyncio.create_task") as mock:
            yield mock

    async def test_main_execution_flow(
        self,
        mock_engine,
        mock_base,
        mock_init_route,
        mock_bot,
        mock_dp,
        mock_oauth,
        mock_cleanup_task,
        mock_asyncio_create_task
    ):
        _, mock_conn = mock_engine

        await main()

        mock_conn.run_sync.assert_called_once_with(mock_base.metadata.create_all)
        mock_init_route.setup_routes.assert_called_once()
        mock_oauth.assert_called_once()
        
        mock_asyncio_create_task.assert_called_once()
        assert mock_asyncio_create_task.call_args[0][0] == "dummy_coro_obj"

        mock_bot.delete_webhook.assert_called_once_with(drop_pending_updates=True)
        mock_dp.start_polling.assert_called_once_with(mock_bot)