from datetime import datetime
from pydantic import ValidationError

from parser_module.domain.models import Event, EventField, EventParseError

class EventService:
    """
    Сервис для управления данными события (редактирование, валидация вручную).
    Не зависит от LLM.
    """

    def _parse_strict_date(self, date_str: str) -> datetime:
        """
        Пытается распарсить дату по строгому шаблону.
        """
        date_str = date_str.strip()
        formats = [
            "%d.%m.%Y %H:%M",
            "%Y-%m-%d %H:%M",
            "%d.%m.%y %H:%M",
            "%H:%M %d.%m.%Y"
        ]

        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue

        raise EventParseError(
            f"Неверный формат даты: '{date_str}'. Используйте: ДД.ММ.ГГГГ ЧЧ:ММ"
        )

    def update_field(self, current_event: Event, field: EventField, new_value: str) -> Event:
        """
        Обновляет поле события.
        """
        try:
            if field in [EventField.DATE_START, EventField.DATE_END]:
                if field == EventField.DATE_END and str(new_value).strip().lower() in ["-", "пусто", "none", "null"]:
                    parsed_value = None
                else:
                    parsed_value = self._parse_strict_date(new_value)

                return current_event.model_copy(update={field.value: parsed_value})

            else:
                return current_event.model_copy(update={field.value: str(new_value)})

        except ValidationError as e:
            raise EventParseError(f"Ошибка валидации данных: {e}")