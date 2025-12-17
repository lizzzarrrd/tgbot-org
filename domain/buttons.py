from enum import StrEnum


class ConfirmButton(StrEnum):
    YES: str = "Да, добавить событие в календарь"
    NO: str = "Нет, отредактировать событие"
    REJECT: str = "Отменить регистрацию события"


class TransformEventButton(StrEnum):
    TRANSORM_DATE: str = "Поменять дату"
    TRANSORM_TIME: str = "Поменять время"
    TRANSORM_NAME: str = "Поменять название"
    TRANSORM_DESCRIPTION: str = "Поменять описание"


class EditEventButton(StrEnum):
    EDIT_TO_YANDEX: str = "Добавить в Яндекс-календарь"
    EDIT_TO_GOOGLE: str = "Добавить в Google-календарь"
    MAKE_ICS: str = "Вернуть ICS-файл"


class MessagesToUser(StrEnum):
    HI_MESSAGE: str = "Привет! Напиши свои данные для регистрации."
    CONFIRM_BUTTON_MESSAGE: str = "Добавить событие в календарь:"
    WHERE_ADD_EVENT: str = (
        "Событие подтверждено. В какой календарь Вы хотите сохранить событие?"
    )
    WHAT_CHANGE: str = "Что Вы хотите изменить?"
    REJECT: str = "Событие отменено"
    ADDED_TO_YANDEX: str = "Событие добавлено в Яндекс-календарь."
    ADDED_TO_GOOGLE: str = "Событие добавлено в Google-календарь."
    TAKE_ICS: str = "Ваш ICS-файл с событием"
