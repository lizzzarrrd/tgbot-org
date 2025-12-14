from __future__ import annotations
from aiogram import types
from datetime import datetime
from adapters.send_message import MessageSender
from adapters.utils import clean_text
from adapters.buttons import confirm_buttons


class MessageHandler:
    """
    Основная ручка: получает любое текстовое сообщение от пользователя.
    """

    def __init__(self, sender: MessageSender):
        self.sender = sender

    async def handle(self, message: types.Message) -> None:
        # need some logic with parsing message
        pass