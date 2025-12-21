from unittest.mock import patch
from parser_module.entrypoints.bot_handler import handle_message, handle_event_update

def test_handle_message_success():
    """Успешная обработка сообщения."""
    with patch("parser_module.adapters.llm_adapter.YandexGptAdapter.complete") as mock_complete:
        mock_complete.return_value = '{"date_start": "2025-12-31 23:59", "name": "Сессия"}'
        
        result = handle_message("С новым годом!")
        
        assert result["status"] == "success"
        assert result["data"]["name"] == "Сессия"

def test_handle_message_no_event():
    """Нет мероприятия."""
    with patch("parser_module.adapters.llm_adapter.YandexGptAdapter.complete") as mock_complete:
        mock_complete.return_value = "no mero"
        result = handle_message("Счастья в 2026!")
        assert result["status"] == "info"

def test_handle_event_update_success():
    """Ручное обновление через handler."""
    current_data = {
        "date_start": "2025-01-01T10:00:00",
        "name": "Old Name",
        "description": "",
        "location": ""
    }
    
    result = handle_event_update(current_data, "name", "New Name")
    
    assert result["status"] == "success"
    assert result["data"]["name"] == "New Name"

def test_handle_event_update_bad_field():
    """Попытка обновить несуществующее поле."""
    result = handle_event_update({}, "wrong_field", "val")
    assert result["status"] == "error"