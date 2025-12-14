from __future__ import annotations
from aiogram import types
from datetime import datetime
from adapters.handlers.send_message import MessageSender



class MessageHandler:
    """
    Основная ручка: получает любое текстовое сообщение от пользователя.
    """

    def __init__(self, sender: MessageSender):
        self.sender = sender

    async def handle(self, message: types.Message) -> None:
        # need some logic with parsing message
        pass