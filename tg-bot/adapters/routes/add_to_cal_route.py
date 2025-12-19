from aiogram import types, F
from .base_route import BaseRoute
from adapters import MessageSender, AddictionToCalendarHandler
from domain import EditEventButton
from infra.init_bot import bot

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
        ) -> None:
            await self.addiction_handler.handle_for_calendar_addiction(callback)