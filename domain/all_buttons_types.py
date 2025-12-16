from enum import StrEnum

class ConfirmButton(StrEnum):
    YES = "Да, добавить событие в календарь"
    NO = "Нет, отредактировать событие"
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


class MessagesToUser(StrEnum):
    HI_MASSAGE = "Привет! Напиши свои данные для регистрации."
    CONFIRMBUTTON_MASSAGE = "Добавить событий в календарь?"
    WHERE_ADD_EVENT = "Событие подтверждено. В какой календарь Вы хотите сохранить событие?"
    WHAT_CHANGE = "Что Вы хотите изменить?"
    REJECT = "Событие отменено"
    