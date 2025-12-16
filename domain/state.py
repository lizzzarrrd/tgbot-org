from enum import StrEnum

class State(StrEnum):
    IS_REGISTERED = "is_registered"
    NOT_REGISTERED = "not_is_registered"

    NEW_MESSAGE = "new_message"
    OLD_MESSAGE = "old_message"

    CHANGE_TIME = "change time"
    CHANGE_DATE = "change date"
    CHANGE_NAME = "change name"
    CHANGE_EVENT = "change event"