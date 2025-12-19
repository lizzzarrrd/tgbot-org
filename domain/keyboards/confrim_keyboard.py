
from aiogram.utils.keyboard import InlineKeyboardBuilder

from domain import ConfirmButton

class ConfirmKeyboard:
    @staticmethod
    def build():
        builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

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