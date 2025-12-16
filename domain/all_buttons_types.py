from enum import StrEnum

class ConfirmButton(StrEnum):
    YES = "Да"
    NO = "Нет"
    REJECT = "Отменить регистрацию события"


class TransformEventButton(StrEnum):
    TRANSORM_DATE = "Поменять дату"
    TRANSORM_TIME = "Поменять время"
    TRANSORM_NAME = "Поменять название"
    TRANSORM_DESCRIPTION = "Поменять описание"

class EditEventButton(StrEnum):
    EDIT_TO_YANDEX = "Добавить в Яндекс-календарь"
    EDIT_TO_GOOGLE = "Добавить в Google-календарь"
    MAKE_ICS = "Вернуть ICS-файл"