from __future__ import annotations
from aiogram import types
from ..send_message import MessageSender
from domain import MessagesToUser

class StartHandler:
    """
    Обработчик команды /start.
    Отвечает за первичную регистрацию пользователя в боте.
    """

    def __init__(self, sender: MessageSender):
        self.sender = sender

    async def handle(self, message: types.Message) -> None:
        await self.sender.send_text(message, text=MessagesToUser.HI_MESSAGE)
        # need some logic with saving in dabase etc.
