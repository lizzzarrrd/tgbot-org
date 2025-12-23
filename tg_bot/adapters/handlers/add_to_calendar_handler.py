from aiogram import types
from aiogram.fsm.context import FSMContext
from pathlib import Path

from tg_bot.adapters import MessageSender
from tg_bot.domain import (MessagesToUser,
                    EditEventButton)

from parser_module.domain.models import Event
from calendar_actions.ics_generator import write_ics_for_project_event


class AddictionToCalendarHandler:
    def __init__(self, sender: MessageSender) -> None:
        self.sender: MessageSender = sender

    async def handle_for_calendar_addiction(
            self,
            callback: types.CallbackQuery,
            state: FSMContext,
            ) -> None:
        pressed_button: EditEventButton = EditEventButton(callback.data)
        await callback.message.edit_reply_markup(reply_markup=None)

        data = await state.get_data()
        event_dict = data.get("event")

        if not event_dict:
            await self.sender.send_text(
                callback.message,
                "Сообщение не найдено, отправьте еще раз",
            )
            await callback.answer()
            return

        event = Event.model_validate(event_dict)

        if pressed_button == EditEventButton.EDIT_TO_YANDEX:
            # Polina_s_module_for_yandex_calendar(parsed_event from Egor)
            await self.sender.send_text(callback.message,
                                        MessagesToUser.ADDED_TO_YANDEX)
        elif pressed_button == EditEventButton.EDIT_TO_GOOGLE:
            # Polina_s_module_for_google_calendar(parsed_event from Egor)
            await self.sender.send_text(callback.message,
                                        MessagesToUser.ADDED_TO_GOOGLE)
        elif pressed_button == EditEventButton.MAKE_ICS:
            user_id = callback.from_user.id if callback.from_user else 0
            out_dir = Path("/data/ics") / str(user_id)
            out_path = out_dir / "event.ics"

            file_path = str(write_ics_for_project_event(event, out_path))
            await self.sender.send_file(
                callback.message,
                file_path=file_path,
                caption=MessagesToUser.TAKE_ICS,
            )
        await callback.answer()
