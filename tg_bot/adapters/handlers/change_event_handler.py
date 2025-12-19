from aiogram import types
from aiogram.fsm.context import FSMContext

from tg_bot.adapters import MessageSender
from tg_bot.domain import (TransformEventButton)

from tg_bot.domain import MessageProcessingStates

class ChangeEventHandler:
    def __init__(self, sender: MessageSender) -> None:
        self.sender: MessageSender = sender

    async def handle_for_event_changing_info(self,
                                             callback: types.CallbackQuery, state: FSMContext) -> None:
        pressed_button: TransformEventButton = TransformEventButton(
            callback.data)
        await callback.message.edit_reply_markup(reply_markup=None)
        if pressed_button == TransformEventButton.TRANSORM_DATE:
            await self.sender.send_text(callback.message,
                                        TransformEventButton.TRANSORM_DATE_PUSHED)
            await state.set_state(MessageProcessingStates.EDITING_DATE)
        elif pressed_button == TransformEventButton.TRANSORM_TIME:
            await self.sender.send_text(callback.message,
                                        TransformEventButton.TRANSORM_TIME_PUSHED)
            await state.set_state(MessageProcessingStates.EDITING_TIME)
        elif pressed_button == TransformEventButton.TRANSORM_NAME:
            await self.sender.send_text(callback.message,
                                        TransformEventButton.TRANSORM_NAME_PUSHED)
            await state.set_state(MessageProcessingStates.EDITING_NAME)
        elif pressed_button == TransformEventButton.TRANSORM_DESCRIPTION:
            await self.sender.send_text(callback.message,
                                        TransformEventButton.TRANSORM_DESCRIPTION_PUSHED)
            await state.set_state(MessageProcessingStates.EDITING_DESCRIPTION)
        await callback.answer()