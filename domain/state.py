from enum import StrEnum


class State(StrEnum):
    IS_REGISTERED: str = "is_registered"
    NOT_REGISTERED: str = "not_is_registered"

    NEW_MESSAGE: str = "new_message"
    OLD_MESSAGE: str = "old_message"

    CHANGE_TIME: str = "change time"
    CHANGE_DATE: str = "change date"
    CHANGE_NAME: str = "change name"
    CHANGE_EVENT: str = "change event"