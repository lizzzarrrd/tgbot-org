from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass()
class Event:
    date_start: datetime
    date_end: Optional[datetime]
    name: str
    description: str = ""
    location: str = ""
