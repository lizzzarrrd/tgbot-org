from aiogram import types
from aiogram.filters import CommandStart
from .base_route import BaseRoute
from adapters import MessageSender, StartHandler
from infra.init_bot import bot


class StartRoute(BaseRoute):
        
    def __init__(self, router):
        self.sender = MessageSender(bot)
        self.start_handler = StartHandler(self.sender)
        super().__init__(router)
    
    def register_handlers(self):
        @self.router.message(CommandStart())
        async def start_command(message: types.Message) -> None:
            await self.start_handler.handle(message)