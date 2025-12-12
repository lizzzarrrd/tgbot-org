from __future__ import annotations
from aiogram import types
from datetime import datetime
from .state  import RegistrationState
from .send_message import MessageSender


class StartHandler:
    """
    Обработчик команды /start.
    Отвечает за первичную регистрацию пользователя в боте.
    """

    def __init__(self, registration_state: RegistrationState, sender: MessageSender):
        self.registration_state = registration_state
        self.sender = sender

    async def handle(self, message: types.Message) -> None:
        tg_user = message.from_user
        if tg_user is None:
            return

        await self.registration_state.register(
            tg_id=tg_user.id,
            username=tg_user.username,
            first_name=tg_user.first_name,
            last_name=tg_user.last_name,
            registered_at=datetime.utcnow()
        )

        await self.sender.send_text(
            chat_id=message.chat.id,
            text="Привет! Ты успешно зарегистрирован!"
        )