# parser_module/domain/models.py
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


class NoEventFound(Exception):
    """Сигнал: в тексте нет мероприятия (аналог 'no mero')."""


class EventParseError(Exception):
    """Сигнал: модель ответила, но не удалось распарсить/валидировать."""


@dataclass(frozen=True, slots=True)
class Event:
    date_start: datetime
    date_end: Optional[datetime]
    name: str
    description: str = ""
    location: str = ""
