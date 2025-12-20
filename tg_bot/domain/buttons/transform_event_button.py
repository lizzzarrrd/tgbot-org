from enum import StrEnum


class TransformEventButton(StrEnum):
    TRANSORM_DATE_START: str = "Поменять дату начала"
    TRANSORM_DATE_END: str = "Поменять дату конца"
    TRANSORM_NAME: str = "Поменять название"
    TRANSORM_DESCRIPTION: str = "Поменять описание"
    TRANSORM_LOCATION: str = "Поменять место"
    TRANSORM_DATE_PUSHED: str = "Пожалуйста, введите корректную дату. Пример: 2023-09-15 14:00"
    TRANSORM_NAME_PUSHED: str = "Пожалуйста, введите корректное название события."
    TRANSORM_DESCRIPTION_PUSHED: str = "Пожалуйста, введите корректное описание события."
    TRANSORM_LOCATION_PUSHED: str = "Пожалуйста, введите корректное место события."


