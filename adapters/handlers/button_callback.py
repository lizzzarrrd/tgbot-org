from aiogram import types
from adapters.send_message import MessageSender
from domain.all_buttons_types import ConfirmButton, MessagesToUser, EditEventButton
from domain.all_keyboards import EditEventKeyboard, TransformEventKeyboard

class ConfirmHandler:
    def __init__(self, sender: MessageSender):
        self.sender = sender

    async def handle(self, callback: types.CallbackQuery) -> None:
        pressed_button: ConfirmButton = ConfirmButton(callback.data)
        if pressed_button == ConfirmButton.YES:
            await self.sender.send_text(callback.message, MessagesToUser.WHERE_ADD_EVENT, reply_markup=EditEventKeyboard.build())
        elif pressed_button == ConfirmButton.NO:
            await self.sender.send_text(callback.message, MessagesToUser.WHAT_CHANGE, reply_markup=TransformEventKeyboard.build())
        elif pressed_button == ConfirmButton.REJECT:
            await self.sender.send_text(callback.message, MessagesToUser.REJECT)

        pressed_button: EditEventButton = EditEventButton(callback.data)
        if pressed_button == EditEventButton.EDIT_TO_YANDEX:
            #Polina_s_module_for_yandex_calendar()
            await self.sender.send_text(callback.message,MessagesToUser.ADDED_TO_YANDEX)
        elif pressed_button == EditEventButton.EDIT_TO_GOOGLE:
            #Polina_s_module_for_google_calendar()
            await self.sender.send_text(callback.message, MessagesToUser.ADDED_TO_GOOGLE)
        elif pressed_button == EditEventButton.MAKE_ICS:
            # file = Polina_s_module_for_making_ics_calendar()
            await self.sender.send_text(callback.message, MessagesToUser.TAKE_ICS)
        await callback.answer()


