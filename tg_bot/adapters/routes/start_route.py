from .base_route import BaseRoute


from aiogram import types
from aiogram.filters import CommandStart
from tg_bot.infra.init_db import async_session_factory

from tg_bot.adapters import (MessageSender, StartHandler)
from tg_bot.infra.init_bot import bot
from tg_bot.use_cases import BdInteractor


sender: MessageSender = MessageSender(bot)


class StartRoute(BaseRoute):
        
    def __init__(self, router):
        self.sender = MessageSender(bot)
        self.router = router
        super().__init__(router)
    
    def register_handlers(self):
        @self.router.message(CommandStart())
        async def start_command(message: types.Message) -> None:
            # await self.start_handler.handle(message)
            async with async_session_factory() as session:
                db_interactor = BdInteractor(session)
                start_handler = StartHandler(
                    sender=self.sender,
                    db_interactor=db_interactor,
                )
                await start_handler.handle(message)