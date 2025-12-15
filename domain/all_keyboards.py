
from aiogram.utils.keyboard import InlineKeyboardBuilder
from domain.all_buttons_types import ConfirmButton, EditEventButton

class ConfirmKeyboard:
    @staticmethod
    def build():
        builder = InlineKeyboardBuilder()

        builder.button(
            text=ConfirmButton.YES.value,
            callback_data=ConfirmButton.YES.value,
        )
        builder.button(
            text=ConfirmButton.NO.value,
            callback_data=ConfirmButton.NO.value,
        )
        builder.button(
            text=ConfirmButton.REJECT.value,
            callback_data=ConfirmButton.REJECT.value,
        )

        builder.adjust(1)
        return builder.as_markup()

class EditEventKeyboard:
    @staticmethod
    def build():
        builder = InlineKeyboardBuilder()

        builder.button(
            text=EditEventButton.EDIT_DATE.value,
            callback_data=EditEventButton.EDIT_DATE.value,
        )
        builder.button(
            text=EditEventButton.EDIT_TIME.value,
            callback_data=EditEventButton.EDIT_TIME.value,
        )
        builder.button(
            text=EditEventButton.MAKE_ICS.value,
            callback_data=EditEventButton.MAKE_ICS.value,
        )
        builder.button(
            text=EditEventButton.SAVE_CALENDAR.value,
            callback_data=EditEventButton.SAVE_CALENDAR.value,
        )

        builder.adjust(1)
        return builder.as_markup()