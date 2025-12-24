from enum import StrEnum


class MessagesToUser(StrEnum):
    HI_MESSAGE: str = "Привет! Отправь мне любое событие, и я добавлю тебе его в календрь"
    CONFIRM_BUTTON_MESSAGE: str = "Желаете добавить следующее событие в календарь?"
    WHERE_ADD_EVENT: str = (
        "Событие подтверждено. В какой календарь Вы хотите сохранить событие?"
    )
    WHAT_CHANGE: str = "Что Вы хотите изменить?"
    REJECT: str = "Событие отменено"
    ADDED_TO_YANDEX: str = "Событие добавлено в Яндекс-календарь."
    ADDED_TO_GOOGLE: str = "Событие добавлено в Google-календарь."
    TAKE_ICS: str = "Ваш ICS-файл с событием"
    WRONG: str = "Я не понял, что ты имеешь виду"
    PLUG:str = "Этот функционал пока не реализован"
    GOOGLE_ERROR: str = "Ошибка на стороне Google"
    GOOGLE_M1: str = "Чтобы добавить в Google Calendar, нужно один раз авторизоваться.\n\n 1) Нажмите ссылку ниже и подтвердите доступ\n 2) После подтверждения можно закрыть вкладку — бот сам добавит событие\n\n Ссылка: "
    ADDED_TO_GOOGLE_CAL: str = "Событие добавлено в Google Calendar!"
    



