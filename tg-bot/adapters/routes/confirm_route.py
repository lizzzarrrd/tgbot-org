from aiogram import types, F
from .base_route import BaseRoute
from adapters import MessageSender, ConfirmHandler
from domain import ConfirmButton
from infra.init_bot import bot


class ConfirmCallbacksRoute(BaseRoute):
    
    def __init__(self, router):
        self.sender = MessageSender(bot)
        self.confirm_handler = ConfirmHandler(self.sender)
        super().__init__(router)
    
    def register_handlers(self):
        @self.router.callback_query(
            F.data.in_(
                {
                    ConfirmButton.YES,
                    ConfirmButton.NO,
                    ConfirmButton.REJECT,
                }
            )
        )
        async def confirm_callbacks(callback: types.CallbackQuery) -> None:
            await self.confirm_handler.handle_for_confirm(callback)