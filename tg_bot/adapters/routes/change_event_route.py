from aiogram import types, F
from aiogram.fsm.context import FSMContext
from .base_route import BaseRoute
from tg_bot.adapters import MessageSender, ChangeEventHandler
from tg_bot.domain import TransformEventButton
from tg_bot.infra.init_bot import bot


class ChangeEventCallbacksRoute(BaseRoute):
    
    def __init__(self, router):
        self.sender = MessageSender(bot)
        self.change_event_handler = ChangeEventHandler(self.sender)
        super().__init__(router)
    
    def register_handlers(self):
        @self.router.callback_query(
            F.data.in_(
                {
                    TransformEventButton.TRANSORM_DATE_START,
                    TransformEventButton.TRANSORM_DATE_END,
                    TransformEventButton.TRANSORM_NAME,
                    TransformEventButton.TRANSORM_DESCRIPTION,
                    TransformEventButton.TRANSORM_LOCATION
                }
            )
        )
        async def change_event_callbacks(
            callback: types.CallbackQuery,
            state: FSMContext
        ) -> None:
            await self.change_event_handler.handle_for_event_changing_info(callback, state)