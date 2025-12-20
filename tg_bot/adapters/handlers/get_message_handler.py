from __future__ import annotations

from aiogram import types
from aiogram.fsm.context import FSMContext

from tg_bot.adapters import MessageSender

from tg_bot.domain import ConfirmKeyboard
from tg_bot.domain import MessagesToUser
from tg_bot.domain import MessageProcessingStates
from parser_module.entrypoints import handle_message
from parser_module.entrypoints import handle_event_update
from tg_bot.use_cases import format_event

class MessageHandler:
    """
    Основная ручка: получает любое текстовое сообщение от пользователя.
    """

    def __init__(self, sender: MessageSender) -> None:
        self.sender: MessageSender = sender

    async def handle(self, message: types.Message, state: FSMContext) -> None:

        current_state = await state.get_state()

        if not current_state:
            parsed_event = handle_message(message)
            try:
                await state.update_data(event=parsed_event["data"])
            except:
                await self.sender.send_text(message, "Пошел нахуй")
                return

            if parsed_event["status"] == "success":
                await self.sender.send_text(
                    message,
                    f"{MessagesToUser.CONFIRM_BUTTON_MESSAGE} {format_event(parsed_event['data'])}",
                    reply_markup=ConfirmKeyboard.build(),
                )
            else:
                await self.sender.send_text(message, parsed_event.get("msg", "Ошибка"))
            return
        
        data = await state.get_data() 
        current_event = data.get("event")
        if not current_event:
            await state.clear()
            await self.sender.send_text(message, "Событие не найдено, отправь исходный текст заново.")
            return

        if current_state == MessageProcessingStates.EDITING_DATE_START.state:
            new_event_parsed_event = handle_event_update(current_event, "date_start", message.text)
            await self.sender.send_text(message,
                                        f"{MessagesToUser.CONFIRM_BUTTON_MESSAGE} {format_event(new_event_parsed_event['data'])}",
                reply_markup=ConfirmKeyboard.build(),)

        elif current_state == MessageProcessingStates.EDITING_DATE_END.state:
            new_event_parsed_event = handle_event_update(current_event, "date_end", message.text)
            await self.sender.send_text(message,
                                        f"{MessagesToUser.CONFIRM_BUTTON_MESSAGE} {format_event(new_event_parsed_event['data'])}",
                reply_markup=ConfirmKeyboard.build(),)

        elif current_state == MessageProcessingStates.EDITING_NAME.state:
            # отправить в парсер заново переделать поле события и получить новое событие
            new_event_parsed_event = handle_event_update(current_event, "name", message.text)
            await self.sender.send_text(message,
                                        f"{MessagesToUser.CONFIRM_BUTTON_MESSAGE} {format_event(new_event_parsed_event['data'])}",
                reply_markup=ConfirmKeyboard.build(),)
        elif current_state == MessageProcessingStates.EDITING_DESCRIPTION.state:
            # отправить в парсер заново переделать поле события и получить новое событие
            new_event_parsed_event = handle_event_update(current_event, "description", message.text)
            await self.sender.send_text(message,
                                        f"{MessagesToUser.CONFIRM_BUTTON_MESSAGE} {format_event(new_event_parsed_event['data'])}",
                reply_markup=ConfirmKeyboard.build(),)
        elif current_state == MessageProcessingStates.EDITING_LOCATION.state:
            # отправить в парсер заново переделать поле события и получить новое событие
            new_event_parsed_event = handle_event_update(current_event, "location", message.text)
            await self.sender.send_text(message,
                                        f"{MessagesToUser.CONFIRM_BUTTON_MESSAGE} {format_event(new_event_parsed_event['data'])}",
                reply_markup=ConfirmKeyboard.build(),)
        # await state.clear()
        await state.set_state(None)


