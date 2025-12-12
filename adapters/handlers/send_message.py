from __future__ import annotations
from aiogram import Bot


class MessageSender:
    """
    Унифицированный интерфейс отправки сообщений пользователю.
    Отправляет сообщение в чат.
    """

    def __init__(self, bot: Bot):
        self.bot = bot

    async def send_text(self, chat_id: int, text: str, reply_markup=None):
        return await self.bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=reply_markup
        )