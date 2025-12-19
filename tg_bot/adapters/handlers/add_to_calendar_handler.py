from aiogram import types


from tg_bot.adapters import MessageSender
from tg_bot.domain import (MessagesToUser,
                    EditEventButton)


class AddictionToCalendarHandler:
    def __init__(self, sender: MessageSender) -> None:
        self.sender: MessageSender = sender

    async def handle_for_calendar_addiction(self,
                                            callback: types.CallbackQuery) -> None:
        pressed_button: EditEventButton = EditEventButton(callback.data)
        await callback.message.edit_reply_markup(reply_markup=None)
        if pressed_button == EditEventButton.EDIT_TO_YANDEX:
            # Polina_s_module_for_yandex_calendar(parsed_event from Egor)
            await self.sender.send_text(callback.message,
                                        MessagesToUser.ADDED_TO_YANDEX)
        elif pressed_button == EditEventButton.EDIT_TO_GOOGLE:
            # Polina_s_module_for_google_calendar(parsed_event from Egor)
            await self.sender.send_text(callback.message,
                                        MessagesToUser.ADDED_TO_GOOGLE)
        elif pressed_button == EditEventButton.MAKE_ICS:
            # file_path = Polina_s_module_for_making_ics_calendar(parsed_event from Egor)
            await self.sender.send_file(callback.message, file_path="",
                                        caption=MessagesToUser.TAKE_ICS)
        await callback.answer()
