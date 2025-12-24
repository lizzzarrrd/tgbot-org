from enum import StrEnum


class MessagesToUser(StrEnum):
    HI_MESSAGE: str = "Здравствуйте! Пришлите, пожалуйста, Ваше событие, а я добавлю его в календарь."
    CONFIRM_BUTTON_MESSAGE: str = "Желаете добавить следующее событие в календарь?"
    WHERE_ADD_EVENT: str = (
        "Событие подтверждено. В какой календарь Вы хотите сохранить событие?"
    )
    WHAT_CHANGE: str = "Что Вы хотите изменить в событии?"
    REJECT: str = "Событие отменено"
    ADDED_TO_YANDEX: str = "Событие добавлено в Яндекс-календарь."
    ADDED_TO_GOOGLE: str = "Событие добавлено в Google-календарь."
    TAKE_ICS: str = "Ваш ICS-файл с событием:"
