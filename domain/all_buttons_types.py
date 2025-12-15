from enum import StrEnum


class MainMenuButton(StrEnum):
    CREATE_EVENT = "Создать событие"
    MY_EVENTS = "Мои события"
    MY_GROUPS = "Мои группы"


class ConfirmButton(StrEnum):
    YES = "Да"
    NO = "Нет"
    REJECT = "Отменить регистрацию события"


class EditEventButton(StrEnum):
    EDIT_DATE = "Поменять дату"
    EDIT_TIME = "Поменять время"
    MAKE_ICS = "Вернуть .ics"
    SAVE_CALENDAR = "Сохранить в календарь"