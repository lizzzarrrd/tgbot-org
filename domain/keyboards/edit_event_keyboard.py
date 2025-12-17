from aiogram.utils.keyboard import InlineKeyboardBuilder

from ..buttons import EditEventButton

class EditEventKeyboard:
    @staticmethod
    def build():
        builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

        builder.button(
            text=EditEventButton.EDIT_TO_YANDEX.value,
            callback_data=EditEventButton.EDIT_TO_YANDEX.value,
        )
        builder.button(
            text=EditEventButton.EDIT_TO_GOOGLE.value,
            callback_data=EditEventButton.EDIT_TO_GOOGLE.value,
        )
        builder.button(
            text=EditEventButton.MAKE_ICS.value,
            callback_data=EditEventButton.MAKE_ICS.value,
        )
        builder.adjust(1)
        return builder.as_markup()