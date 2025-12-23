import pytest
from datetime import datetime
from parser_module.domain.models import EventField, EventParseError

def test_update_name(event_service, base_event):
    """Изменение имени."""
    new_event = event_service.update_field(base_event, EventField.NAME, "New Name")
    assert new_event.name == "New Name"
    assert new_event.date_start == base_event.date_start

def test_update_date_iso(event_service, base_event):
    """Изменение даты (ISO)."""
    new_event = event_service.update_field(base_event, EventField.DATE_START, "2025-10-10 10:00")
    assert new_event.date_start == datetime(2025, 10, 10, 10, 0)

def test_update_date_russian(event_service, base_event):
    """Изменение даты (RUS)."""
    new_event = event_service.update_field(base_event, EventField.DATE_START, "31.12.2025 23:59")
    assert new_event.date_start == datetime(2025, 12, 31, 23, 59)

def test_update_date_invalid(event_service, base_event):
    """Ошибка при кривом формате даты."""
    with pytest.raises(EventParseError):
        event_service.update_field(base_event, EventField.DATE_START, "завтра")

def test_clear_date_end(event_service, base_event):
    """Очистка даты окончания."""
    base_event.date_end = datetime.now()
    
    new_event = event_service.update_field(base_event, EventField.DATE_END, "none")
    assert new_event.date_end is None