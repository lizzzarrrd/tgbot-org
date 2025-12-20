from aiogram.utils.keyboard import InlineKeyboardBuilder

from tg_bot.domain import TransformEventButton


class TransformEventKeyboard:
    @staticmethod
    def build():
        builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
        builder.button(
            text=TransformEventButton.TRANSORM_DATE_START.value,
            callback_data=TransformEventButton.TRANSORM_DATE_START.value,
        )
        builder.button(
            text=TransformEventButton.TRANSORM_DATE_END.value,
            callback_data=TransformEventButton.TRANSORM_DATE_END.value,
        )
        builder.button(
            text=TransformEventButton.TRANSORM_NAME.value,
            callback_data=TransformEventButton.TRANSORM_NAME.value,
        )
        builder.button(
            text=TransformEventButton.TRANSORM_DESCRIPTION.value,
            callback_data=TransformEventButton.TRANSORM_DESCRIPTION.value,
        )
        builder.button(
            text=TransformEventButton.TRANSORM_LOCATION.value,
            callback_data=TransformEventButton.TRANSORM_LOCATION.value,
        )

        builder.adjust(1)
        return builder.as_markup()