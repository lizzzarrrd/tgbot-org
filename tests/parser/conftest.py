import pytest
from datetime import datetime
from unittest.mock import MagicMock

@pytest.fixture(autouse=True)
def mock_env(monkeypatch):
    monkeypatch.setenv("YANDEX_API_KEY", "test_key")
    monkeypatch.setenv("YANDEX_MODEL_URI", "gpt://test/yandexgpt")

@pytest.fixture
def mock_llm():
    mock = MagicMock()
    mock.complete.return_value = '{"date_start": "2025-12-31 23:00", "name": "Mock Event"}'
    return mock

@pytest.fixture
def base_event():
    from parser_module.domain.models import Event
    return Event(
        date_start=datetime(2025, 12, 31, 23, 0),
        name="Новый Год",
        description="Праздник",
        location="Дома"
    )

@pytest.fixture
def event_service():
    from parser_module.use_cases.event_service import EventService
    return EventService()