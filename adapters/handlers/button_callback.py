from aiogram import types
from ..send_message import MessageSender
from domain import (ConfirmButton, MessagesToUser,
                    EditEventButton, EditEventKeyboard, TransformEventButton, TransformEventKeyboard)


class ConfirmHandler:
    def __init__(self, sender: MessageSender) -> None:
        self.sender: MessageSender = sender

    async def handle_for_confirm(self, callback: types.CallbackQuery) -> None:
        pressed_button: ConfirmButton = ConfirmButton(callback.data)
        if pressed_button == ConfirmButton.YES:
            await self.sender.send_text(callback.message, MessagesToUser.WHERE_ADD_EVENT, reply_markup=EditEventKeyboard.build())
        elif pressed_button == ConfirmButton.NO:
            await self.sender.send_text(callback.message, MessagesToUser.WHAT_CHANGE, reply_markup=TransformEventKeyboard.build())
        elif pressed_button == ConfirmButton.REJECT:
            await self.sender.send_text(callback.message, MessagesToUser.REJECT)





class AddictionToCalendarHandler:
    def __init__(self, sender: MessageSender) -> None:
        self.sender: MessageSender = sender

    async def handle_for_calendar_addiction(self,
                                            callback: types.CallbackQuery) -> None:
        pressed_button: EditEventButton = EditEventButton(callback.data)
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
            await self.sender.send_file(callback.message, file_path,
                                        MessagesToUser.TAKE_ICS)
        await callback.answer()


class ChangeEventHandler:
    def __init__(self, sender: MessageSender) -> None:
        self.sender: MessageSender = sender

    async def handle_for_event_changing_info(self,
                                             callback: types.CallbackQuery) -> None:
        pressed_button: TransformEventButton = TransformEventButton(
            callback.data)
        if pressed_button == TransformEventButton.TRANSORM_DATE:
            # отправить в парсер заново переделать поле события и получить новое событие
            new_event_parsed_event = "PARSED FROM EGOR CHANGED DATE"
            await self.sender.send_text(callback.message,
                                        f"{MessagesToUser.CONFIRM_BUTTON_MESSAGE} {new_event_parsed_event}")
        elif pressed_button == TransformEventButton.TRANSORM_TIME:
            # отправить в парсер заново переделать поле события и получить новое событие
            new_event_parsed_event = "PARSED FROM EGOR CHANGED TIME"
            await self.sender.send_text(callback.message,
                                        f"{MessagesToUser.CONFIRM_BUTTON_MESSAGE} {new_event_parsed_event}")
        elif pressed_button == TransformEventButton.TRANSORM_NAME:
            # отправить в парсер заново переделать поле события и получить новое событие
            new_event_parsed_event = "PARSED FROM EGOR CHANGED NAME"
            await self.sender.send_text(callback.message,
                                        f"{MessagesToUser.CONFIRM_BUTTON_MESSAGE} {new_event_parsed_event}")
        elif pressed_button == TransformEventButton.TRANSORM_DESCRIPTION:
            # отправить в парсер заново переделать поле события и получить новое событие
            new_event_parsed_event = "PARSED FROM EGOR CHANGED DESCRIPTION"
            await self.sender.send_text(callback.message,
                                        f"{MessagesToUser.CONFIRM_BUTTON_MESSAGE} {new_event_parsed_event}")
        await callback.answer()