from aiogram.fsm.state import StatesGroup, State

class MessageProcessingStates(StatesGroup):
    
    EDITING_DATE = State()
    EDITING_TIME = State()
    EDITING_NAME = State()
    EDITING_DESCRIPTION = State()


    