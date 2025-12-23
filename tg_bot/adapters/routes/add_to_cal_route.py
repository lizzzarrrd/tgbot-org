from aiogram import types, F
from aiogram.fsm.context import FSMContext

from .base_route import BaseRoute
from tg_bot.adapters import MessageSender, AddictionToCalendarHandler
from tg_bot.domain import EditEventButton
from tg_bot.infra.init_bot import bot

class CalendarAddictionCallbacksRoute(BaseRoute):
    
    def __init__(self, router):
        self.sender = MessageSender(bot)
        self.addiction_handler = AddictionToCalendarHandler(self.sender)
        super().__init__(router)
    
    def register_handlers(self):
        @self.router.callback_query(
            F.data.in_(
                {
                    EditEventButton.EDIT_TO_YANDEX,
                    EditEventButton.EDIT_TO_GOOGLE,
                    EditEventButton.MAKE_ICS,
                }
            )
        )
        async def calendar_addiction_callbacks(
            callback: types.CallbackQuery,
            state: FSMContext,
        ) -> None:
            await self.addiction_handler.handle_for_calendar_addiction(callback, state)