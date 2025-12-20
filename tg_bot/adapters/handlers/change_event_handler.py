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
        if pressed_button == TransformEventButton.TRANSORM_DATE_START:
            await self.sender.send_text(callback.message,
                                        TransformEventButton.TRANSORM_DATE_PUSHED)
            await state.set_state(MessageProcessingStates.TRANSORM_DATE_START)

        elif pressed_button == TransformEventButton.TRANSORM_DATE_END:
            await self.sender.send_text(callback.message,
                                        TransformEventButton.TRANSORM_TIME_PUSHED)
            await state.set_state(MessageProcessingStates.TRANSORM_DATE_END)

        elif pressed_button == TransformEventButton.TRANSORM_NAME:
            await self.sender.send_text(callback.message,
                                        TransformEventButton.TRANSORM_NAME_PUSHED)
            await state.set_state(MessageProcessingStates.EDITING_NAME)

        elif pressed_button == TransformEventButton.TRANSORM_DESCRIPTION:
            await self.sender.send_text(callback.message,
                                        TransformEventButton.TRANSORM_DESCRIPTION_PUSHED)
            await state.set_state(MessageProcessingStates.EDITING_DESCRIPTION)

        elif pressed_button == TransformEventButton.TRANSORM_LOCATION:
            await self.sender.send_text(callback.message,
                                        TransformEventButton.TRANSORM_LOCATION_PUSHED)
            await state.set_state(MessageProcessingStates.EDITING_LOCATION)
        await callback.answer()