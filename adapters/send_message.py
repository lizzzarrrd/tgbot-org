from __future__ import annotations
from aiogram import Bot
from aiogram.types import Message
from typing import Optional, Union
from aiogram.types import Message, ReplyKeyboardMarkup, InlineKeyboardMarkup

Markup = Union[ReplyKeyboardMarkup, InlineKeyboardMarkup]

class MessageSender:
    """
    Унифицированный интерфейс отправки сообщений пользователю.
    Отправляет сообщение в чат.
    """

    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def send_text(
            self,
            message: Message,
            text: str,
            reply_markup: Optional[Markup] = None,
    ) -> None:
        await message.answer(text, reply_markup=reply_markup)