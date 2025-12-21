"""
из Event model (parser_module.domain.models.Event) в .ics
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional, Union
import uuid


def _to_utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _ics_escape(text: str) -> str:
    return (
        text.replace("\\", "\\\\")
        .replace(";", "\\;")
        .replace(",", "\\,")
        .replace("\n", "\\n")
        .replace("\r", "")
    )


def _fmt_dt_utc(dt: datetime) -> str:
    dt = _to_utc(dt)
    return dt.strftime("%Y%m%dT%H%M%SZ")


@dataclass
class IcsEvent:
    name: str
    date_start: datetime
    date_end: datetime
    description: str = ""
    location: str = ""
    uid: Optional[str] = None


def ics_content(event: IcsEvent, prodid: str = "-//tgbot-org//calendar//EN") -> str:
    """
    весь .ics файл как string
    """
    uid = event.uid or f"{uuid.uuid4()}@tgbot-org"
    now = _fmt_dt_utc(datetime.now(timezone.utc))

    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        f"PRODID:{prodid}",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "BEGIN:VEVENT",
        f"UID:{_ics_escape(uid)}",
        f"DTSTAMP:{now}",
        f"DTSTART:{_fmt_dt_utc(event.date_start)}",
        f"DTEND:{_fmt_dt_utc(event.date_end)}",
        f"SUMMARY:{_ics_escape(event.name)}",
    ]

    if event.description:
        lines.append(f"DESCRIPTION:{_ics_escape(event.description)}")
    if event.location:
        lines.append(f"LOCATION:{_ics_escape(event.location)}")

    lines += [
        "END:VEVENT",
        "END:VCALENDAR",
        "",
    ]

    return "\r\n".join(lines)


def build_ics_event_from_project_event(project_event,
                                       default_duration: timedelta = timedelta(hours=1)
                                       ) -> IcsEvent:
    """
    parser_module.domain.models.Event -> IcsEvent.
    еси не написалу дату конца, то используем date_start + default_duration.
    """
    date_start = project_event.date_start
    date_end = project_event.date_end or (project_event.date_start + default_duration)
    return IcsEvent(
        name=project_event.name,
        date_start=date_start,
        date_end=date_end,
        description=getattr(project_event, "description", "") or "",
        location=getattr(project_event, "location", "") or "",
    )


def write_ics_file(
    event: IcsEvent,
    out_path: Union[str, Path],
    prodid: str = "-//tgbot-org//calendar//EN",
) -> Path:
    """
    запись .ics файла в out_path и возвращаем это путь
    """
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(ics_content(event, prodid=prodid), encoding="utf-8")
    return out_path


def write_ics_for_project_event(
    project_event,
    out_path: Union[str, Path],
    default_duration: timedelta = timedelta(hours=1),
) -> Path:
    """
    объединила, чтобы быдл удобно в проекте использовать
    """
    return write_ics_file(build_ics_event_from_project_event(project_event, default_duration=default_duration), out_path)
