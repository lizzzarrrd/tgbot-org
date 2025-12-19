from enum import StrEnum


class TransformEventButton(StrEnum):
    TRANSORM_DATE: str = "Поменять дату"
    TRANSORM_TIME: str = "Поменять время"
    TRANSORM_NAME: str = "Поменять название"
    TRANSORM_DESCRIPTION: str = "Поменять описание"
    TRANSORM_DATE_PUSHED: str = "Пожалуйста, введите корректную дату. Пример: 2023-09-15"
    TRANSORM_TIME_PUSHED: str = "Пожалуйста, введите корректное время. Пример: 14:00"
    TRANSORM_NAME_PUSHED: str = "Пожалуйста, введите корректное название события."
    TRANSORM_DESCRIPTION_PUSHED: str = "Пожалуйста, введите корректное описание события."

