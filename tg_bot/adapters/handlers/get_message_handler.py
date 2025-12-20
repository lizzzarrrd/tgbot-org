from __future__ import annotations

from aiogram import types
from aiogram.fsm.context import FSMContext

from tg_bot.adapters import MessageSender

from tg_bot.domain import ConfirmKeyboard
from tg_bot.domain import MessagesToUser
from tg_bot.domain import MessageProcessingStates
from parser_module.entrypoints import handle_message

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
            await self.sender.send_text(
                message,
                f"{MessagesToUser.CONFIRM_BUTTON_MESSAGE} {parsed_event}",
                reply_markup=ConfirmKeyboard.build(),
            )

        elif current_state == MessageProcessingStates.EDITING_DATE.state:
            # отправить в парсер заново переделать поле события и получить новое событие
            new_event_parsed_event = "PARSED FROM EGOR CHANGED DATE"
            await self.sender.send_text(message,
                                        f"{MessagesToUser.CONFIRM_BUTTON_MESSAGE} {new_event_parsed_event}",
                reply_markup=ConfirmKeyboard.build(),)
        elif current_state == MessageProcessingStates.EDITING_TIME.state:
            # отправить в парсер заново переделать поле события и получить новое событие
            new_event_parsed_event = "PARSED FROM EGOR CHANGED TIME"
            await self.sender.send_text(message,
                                        f"{MessagesToUser.CONFIRM_BUTTON_MESSAGE} {new_event_parsed_event}",
                reply_markup=ConfirmKeyboard.build(),)
        elif current_state == MessageProcessingStates.EDITING_NAME.state:
            # отправить в парсер заново переделать поле события и получить новое событие
            new_event_parsed_event = "PARSED FROM EGOR CHANGED NAME"
            await self.sender.send_text(message,
                                        f"{MessagesToUser.CONFIRM_BUTTON_MESSAGE} {new_event_parsed_event}",
                reply_markup=ConfirmKeyboard.build(),)
        elif current_state == MessageProcessingStates.EDITING_DESCRIPTION.state:
            # отправить в парсер заново переделать поле события и получить новое событие
            new_event_parsed_event = "PARSED FROM EGOR CHANGED DESCRIPTION"
            await self.sender.send_text(message,
                                        f"{MessagesToUser.CONFIRM_BUTTON_MESSAGE} {new_event_parsed_event}",
                reply_markup=ConfirmKeyboard.build(),)
        await state.clear()


