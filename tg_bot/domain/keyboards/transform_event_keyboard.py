from aiogram.utils.keyboard import InlineKeyboardBuilder

from tg_bot.domain import TransformEventButton


class TransformEventKeyboard:
    @staticmethod
    def build():
        builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
        builder.button(
            text=TransformEventButton.TRANSORM_DATE.value,
            callback_data=TransformEventButton.TRANSORM_DATE.value,
        )
        builder.button(
            text=TransformEventButton.TRANSORM_TIME.value,
            callback_data=TransformEventButton.TRANSORM_TIME.value,
        )
        builder.button(
            text=TransformEventButton.TRANSORM_NAME.value,
            callback_data=TransformEventButton.TRANSORM_NAME.value,
        )
        builder.button(
            text=TransformEventButton.TRANSORM_DESCRIPTION.value,
            callback_data=TransformEventButton.TRANSORM_DESCRIPTION.value,
        )

        builder.adjust(1)
        return builder.as_markup()