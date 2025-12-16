from dataclasses import dataclass
from datetime import datetime
from typing import Optional


class NoEventFound(Exception):
    pass


class EventParseError(Exception):
    pass


@dataclass()
class Event:
    date_start: datetime
    date_end: Optional[datetime]
    name: str
    description: str = ""
    location: str = ""
