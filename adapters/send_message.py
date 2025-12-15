from __future__ import annotations
from aiogram import Bot
from aiogram.types import Message

class MessageSender:
    """
    Унифицированный интерфейс отправки сообщений пользователю.
    Отправляет сообщение в чат.
    """

    def __init__(self, bot: Bot):
        self.bot = bot

    async def send_text(self, message: Message, text: str):
        await message.answer(text)