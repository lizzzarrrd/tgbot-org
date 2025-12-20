def format_event(event: dict) -> str:
    name = event.get("name") or "Без названия"
    date_start = event.get("date_start") or "—"
    date_end = event.get("date_end") or "—"
    description = event.get("description") or "—"
    location = event.get("location") or "—"
    return (
        f"\n\nНазвание: {name}"
        f"\nДата начала: {date_start}"
        f"\nДата конца: {date_end}"
        f"\nОписание: {description}"
        f"\nМесто: {location}"
    )