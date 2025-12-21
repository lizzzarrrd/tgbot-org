from datetime import datetime
from parser_module.domain.models import Event

def test_create_event_valid():
    """Проверка создания корректного события."""
    event = Event(
        date_start=datetime(2025, 1, 1, 10, 0),
        name="Встреча"
    )
    assert event.name == "Встреча"
    assert event.description == ""

def test_none_convertion():
    """Проверка, что None в описании превращается в пустую строку."""
    event = Event(
        date_start=datetime(2025, 1, 1, 10, 0),
        name="Встреча",
        description=None,
        location=None
    )
    assert event.description == ""
    assert event.location == ""