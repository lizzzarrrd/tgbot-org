from enum import StrEnum


class MessagesToUser(StrEnum):
    HI_MESSAGE: str = "Привет! Напишите, пожалуйста, Ваши данные для регистрации."
    CONFIRM_BUTTON_MESSAGE: str = "Желаете добавить следующее событие в календарь?"
    WHERE_ADD_EVENT: str = (
        "Событие подтверждено. В какой календарь Вы хотите сохранить событие?"
    )
    WHAT_CHANGE: str = "Что Вы хотите изменить?"
    REJECT: str = "Событие отменено"
    ADDED_TO_YANDEX: str = "Событие добавлено в Яндекс-календарь."
    ADDED_TO_GOOGLE: str = "Событие добавлено в Google-календарь."
    TAKE_ICS: str = "Ваш ICS-файл с событием"
