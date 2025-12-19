from enum import StrEnum


class ConfirmButton(StrEnum):
    YES: str = "Да, добавить событие в календарь"
    NO: str = "Нет, отредактировать событие"
    REJECT: str = "Отменить регистрацию события"

