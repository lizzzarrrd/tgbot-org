from enum import Enum
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator

class NoEventFound(Exception):
    """Событие не найдено в тексте."""
    pass

class EventParseError(Exception):
    """Ошибка валидации данных или логики."""
    pass

class EventField(str, Enum):
    """Список полей, которые разрешено редактировать."""
    NAME = "name"
    DESCRIPTION = "description"
    LOCATION = "location"
    DATE_START = "date_start"
    DATE_END = "date_end"

class Event(BaseModel):
    date_start: datetime
    date_end: Optional[datetime] = None
    name: str
    description: Optional[str] = Field(default="")
    location: Optional[str] = Field(default="")

    @field_validator("description", "location", mode="before")
    @classmethod
    def none_to_empty_string(cls, v):
        if v is None:
            return ""
        return v