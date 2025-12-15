from __future__ import annotations

from aiogram import types

from adapters.send_message import MessageSender
from domain.all_buttons_types import ConfirmButton

class ConfirmHandler:
    def __init__(self, sender: MessageSender):
        self.sender = sender

    async def handle(self, callback: types.CallbackQuery) -> None:
        if callback.data == ConfirmButton.YES:
            await self.sender.send_text(callback.message, "Ок, подтверждено")
        elif callback.data == ConfirmButton.NO:
            await self.sender.send_text(callback.message, "Отменено")

        # обязательно закрыть “часики” у кнопки
        await callback.answer()


