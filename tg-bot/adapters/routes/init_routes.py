from aiogram import Router
from .base_route import BaseRoute
from .start_route import StartRoute
from .message_route import MessageRoute
from .confirm_route import ConfirmCallbacksRoute
from .add_to_cal_route import CalendarAddictionCallbacksRoute
from .change_event_route import ChangeEventCallbacksRoute

class InitRoute(BaseRoute):
    
    def setup_routes(router: Router) -> None:
        command_routes = StartRoute(router)
        message_routes = MessageRoute(router)
        confirm_callbacks = ConfirmCallbacksRoute(router)
        calendar_addiction_callbacks = CalendarAddictionCallbacksRoute(router)
        change_event_callbacks = ChangeEventCallbacksRoute(router)
        
        return {
            "commands": command_routes,
            "messages": message_routes,
            "confirm": confirm_callbacks,
            "calendar_addiction": calendar_addiction_callbacks,
            "change_event": change_event_callbacks,
        }
