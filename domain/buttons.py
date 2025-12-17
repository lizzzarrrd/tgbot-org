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
    TRANSORM_DATE_PUSHED: str = "Пожалуйста, введите корректную дату. Пример: 2023-09-15"
    TRANSORM_TIME_PUSHED: str = "Пожалуйста, введите корректное время. Пример: 14:00"
    TRANSORM_NAME_PUSHED: str = "Пожалуйста, введите корректное название события."
    TRANSORM_DESCRIPTION_PUSHED: str = "Пожалуйста, введите корректное описание события."




class EditEventButton(StrEnum):
    EDIT_TO_YANDEX: str = "Добавить в Яндекс-календарь"
    EDIT_TO_GOOGLE: str = "Добавить в Google-календарь"
    MAKE_ICS: str = "Вернуть ICS-файл"


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
