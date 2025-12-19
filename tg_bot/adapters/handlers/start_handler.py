from __future__ import annotations
from aiogram import types
from tg_bot.adapters import MessageSender
from tg_bot.domain import MessagesToUser
from tg_bot.use_cases import BdInteractor


class StartHandler:
    """
    Обработчик команды /start.
    Отвечает за первичную регистрацию пользователя в боте.
    """

    def __init__(self, sender: MessageSender, db_interactor: BdInteractor) -> None:
        self.sender: MessageSender = sender
        self.interactor_with_db: BdInteractor = db_interactor

    async def handle(self, message: types.Message) -> None:
        await self.sender.send_text(message, text=MessagesToUser.HI_MESSAGE)
        telegram_id = message.from_user.id
        await self.interactor_with_db.get_or_create(telegram_id)
        await self.sender.send_text(message, text=f"все норм получилось, ты зареган по id {telegram_id}, давай теперь засылай событие")


