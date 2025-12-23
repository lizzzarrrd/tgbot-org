import pytest
from parser_module.use_cases.parse_service import ParseService
from parser_module.domain.models import NoEventFound, EventParseError

def test_parse_simple_json(mock_llm):
    """Парсинг чистого JSON."""
    mock_llm.complete.return_value = '{"date_start": "2025-05-01 12:00", "name": "Тайный Санта"}'
    service = ParseService(llm=mock_llm)
    
    event = service.parse_event("Какой-то текст")
    assert event.name == "Тайный Санта"
    assert event.date_start.month == 5

def test_parse_markdown_json(mock_llm):
    """Очистка от ```json```."""
    mock_llm.complete.return_value = '```json\n{"date_start": "2025-05-01 12:00", "name": "Елка"}\n```'
    service = ParseService(llm=mock_llm)
    
    event = service.parse_event("Какой-то текст")
    assert event.name == "Елка"

def test_parse_list_returns_first(mock_llm):
    """Если вернулся список, берем первый элемент."""
    mock_llm.complete.return_value = '[{"date_start": "2025-01-01 10:00", "name": "Всегда первый!"}, {"name": "Или второй?"}]'
    service = ParseService(llm=mock_llm)
    
    event = service.parse_event("Какой-то текст")
    assert event.name == "Всегда первый!"

def test_no_event_found(mock_llm):
    """Ответ 'no mero'."""
    mock_llm.complete.return_value = "no mero"
    service = ParseService(llm=mock_llm)
    
    with pytest.raises(NoEventFound):
        service.parse_event("Какой-то текст")

def test_invalid_json(mock_llm):
    """Битый ответ."""
    mock_llm.complete.return_value = "Not a JSON"
    service = ParseService(llm=mock_llm)
    
    with pytest.raises(EventParseError):
        service.parse_event("Какой-то текст")