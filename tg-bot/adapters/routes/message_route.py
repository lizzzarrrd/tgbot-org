from aiogram import types
from aiogram.fsm.context import FSMContext
from .base_route import BaseRoute
from adapters import MessageSender, MessageHandler
from infra.init_bot import bot


class MessageRoute(BaseRoute):
    
    def __init__(self, router):
        self.sender = MessageSender(bot)
        self.message_handler = MessageHandler(self.sender)
        super().__init__(router)
    
    def register_handlers(self):
        @self.router.message()
        async def all_messages(message: types.Message, state: FSMContext) -> None:
            await self.message_handler.handle(message, state)