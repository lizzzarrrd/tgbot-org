from aiogram import types

from tg_bot.adapters import MessageSender
from tg_bot.domain import (ConfirmButton, MessagesToUser,
                    EditEventKeyboard, TransformEventKeyboard)


class ConfirmHandler:
    def __init__(self, sender: MessageSender) -> None:
        self.sender: MessageSender = sender

    async def handle_for_confirm(self, callback: types.CallbackQuery) -> None:
        pressed_button: ConfirmButton = ConfirmButton(callback.data)
        await callback.message.edit_reply_markup(reply_markup=None)
        if pressed_button == ConfirmButton.YES:
            await self.sender.send_text(callback.message, MessagesToUser.WHERE_ADD_EVENT, reply_markup=EditEventKeyboard.build())

        elif pressed_button == ConfirmButton.NO:
            await self.sender.send_text(callback.message, MessagesToUser.WHAT_CHANGE, reply_markup=TransformEventKeyboard.build())

        elif pressed_button == ConfirmButton.REJECT:
            await self.sender.send_text(callback.message, MessagesToUser.REJECT)

