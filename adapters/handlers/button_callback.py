from aiogram import types
from aiogram.fsm.context import FSMContext

from ..send_message import MessageSender
from domain import (ConfirmButton, MessagesToUser,
                    EditEventButton, EditEventKeyboard, TransformEventButton, TransformEventKeyboard)

from domain.state import MessageProcessingStates

class ConfirmHandler:
    def __init__(self, sender: MessageSender) -> None:
        self.sender: MessageSender = sender

    async def handle_for_confirm(self, callback: types.CallbackQuery) -> None:
        pressed_button: ConfirmButton = ConfirmButton(callback.data)
        if pressed_button == ConfirmButton.YES:
            await self.sender.send_text(callback.message, MessagesToUser.WHERE_ADD_EVENT, reply_markup=EditEventKeyboard.build())

        elif pressed_button == ConfirmButton.NO:
            await self.sender.send_text(callback.message, MessagesToUser.WHAT_CHANGE, reply_markup=TransformEventKeyboard.build())
    
        elif pressed_button == ConfirmButton.REJECT:
            await self.sender.send_text(callback.message, MessagesToUser.REJECT)





class AddictionToCalendarHandler:
    def __init__(self, sender: MessageSender) -> None:
        self.sender: MessageSender = sender

    async def handle_for_calendar_addiction(self,
                                            callback: types.CallbackQuery) -> None:
        pressed_button: EditEventButton = EditEventButton(callback.data)
        if pressed_button == EditEventButton.EDIT_TO_YANDEX:
            # Polina_s_module_for_yandex_calendar(parsed_event from Egor)
            await self.sender.send_text(callback.message,
                                        MessagesToUser.ADDED_TO_YANDEX)
        elif pressed_button == EditEventButton.EDIT_TO_GOOGLE:
            # Polina_s_module_for_google_calendar(parsed_event from Egor)
            await self.sender.send_text(callback.message,
                                        MessagesToUser.ADDED_TO_GOOGLE)
        elif pressed_button == EditEventButton.MAKE_ICS:
            # file_path = Polina_s_module_for_making_ics_calendar(parsed_event from Egor)
            await self.sender.send_file(callback.message, file_path,
                                        MessagesToUser.TAKE_ICS)
        await callback.answer()


class ChangeEventHandler:
    def __init__(self, sender: MessageSender) -> None:
        self.sender: MessageSender = sender

    async def handle_for_event_changing_info(self,
                                             callback: types.CallbackQuery, state: FSMContext) -> None:
        pressed_button: TransformEventButton = TransformEventButton(
            callback.data)
        if pressed_button == TransformEventButton.TRANSORM_DATE:
            await state.set_state(MessageProcessingStates.EDITING_DATE)
        elif pressed_button == TransformEventButton.TRANSORM_TIME:
            await state.set_state(MessageProcessingStates.EDITING_TIME)
        elif pressed_button == TransformEventButton.TRANSORM_NAME:
            await state.set_state(MessageProcessingStates.EDITING_NAME)
        elif pressed_button == TransformEventButton.TRANSORM_DESCRIPTION:
            await state.set_state(MessageProcessingStates.EDITING_DESCRIPTION)
        await callback.answer()