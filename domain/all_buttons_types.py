from enum import StrEnum


class MainMenuButton(StrEnum):
    CREATE_EVENT = "Создать событие"
    MY_EVENTS = "Мои события"
    MY_GROUPS = "Мои группы"


class ConfirmButton(StrEnum):
    YES = "event_yes"
    NO = "event_no"


class EditEventButton(StrEnum):
    EDIT_DATE = "edit_date"
    EDIT_TIME = "edit_time"
    MAKE_ICS = "make_ics"
    SAVE_CALENDAR = "save_calendar"