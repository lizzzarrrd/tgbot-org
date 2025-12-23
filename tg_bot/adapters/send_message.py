from __future__ import annotations
from aiogram import Bot
from typing import Optional, Union
from aiogram.types import Message, ReplyKeyboardMarkup, InlineKeyboardMarkup, InputFile, FSInputFile

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
        """
        Отправка просто сообщения пользователю на входящее сообщения
        """
        await message.answer(text, reply_markup=reply_markup)

    async def send_text_to_chat(self, chat_id: int, text: str) -> None:
        """
        Отправка сообщения в чат независимо ни от чего
        """
        await self.bot.send_message(chat_id, text)

    async def send_file(
            self,
            message: Message,
            file_path: str,
            caption: Optional[str] = None,
    ) -> None:
        """
        Отправка файла пользователю,
        используется другая функция answer_document, Aiogram v3: FSInputFile.
        """
        try:
            input_file = FSInputFile(file_path)
        except Exception:
            input_file = InputFile(file_path)

        await message.answer_document(input_file, caption=caption)