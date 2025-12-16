from __future__ import annotations
from aiogram import types
from adapters.send_message import MessageSender
from domain.all_keyboards import ConfirmKeyboard
from domain.all_buttons_types import MessagesToUser

class MessageHandler:
    """
    Основная ручка: получает любое текстовое сообщение от пользователя.
    """

    def __init__(self, sender: MessageSender):
        self.sender = sender

    async def handle(self, message: types.Message) -> None:

        await self.sender.send_text(
            message,
            MessagesToUser.CONFIRMBUTTON_MASSAGE,
            reply_markup=ConfirmKeyboard.build(),
        )


