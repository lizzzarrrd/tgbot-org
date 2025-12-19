from enum import StrEnum


class EditEventButton(StrEnum):
    EDIT_TO_YANDEX: str = "Добавить в Яндекс-календарь"
    EDIT_TO_GOOGLE: str = "Добавить в Google-календарь"
    MAKE_ICS: str = "Вернуть ICS-файл"
