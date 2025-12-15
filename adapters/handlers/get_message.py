from __future__ import annotations
from aiogram import types
from adapters.send_message import MessageSender
from domain.all_keyboards import MainMenuKeyboard,ConfirmKeyboard

class MessageHandler:
    """
    Основная ручка: получает любое текстовое сообщение от пользователя.
    """

    def __init__(self, sender: MessageSender):
        self.sender = sender

    async def (self, message: types.Message) -> None:

        await message.answer(
            "Главное меню",
            reply_markup=MainMenuKeyboard.build(),
        )

        await message.answer(
            "Подтвердить?",
            reply_markup=ConfirmKeyboard.build(),
        )


