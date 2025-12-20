from aiogram.fsm.state import StatesGroup, State


class MessageProcessingStates(StatesGroup):
    
    EDITING_DATE_START = State()
    EDITING_DATE_END = State()
    EDITING_NAME = State()
    EDITING_DESCRIPTION = State()
    EDITING_LOCATION = State()


    