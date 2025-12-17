from __future__ import annotations
from aiogram import types
from ..send_message import MessageSender
from domain import ConfirmKeyboard
from domain import MessagesToUser

class MessageHandler:
    """
    Основная ручка: получает любое текстовое сообщение от пользователя.
    """

    def __init__(self, sender: MessageSender) -> None:
        self.sender: MessageSender = sender

    async def handle(self, message: types.Message) -> None:
        
        #call parsed func and get:
        parsed_event = "PARSED FROM EGOR"

        await self.sender.send_text(
            message,
            f"{MessagesToUser.CONFIRM_BUTTON_MESSAGE} {parsed_event}",
            reply_markup=ConfirmKeyboard.build(),
        )


