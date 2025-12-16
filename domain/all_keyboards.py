
from aiogram.utils.keyboard import InlineKeyboardBuilder
from domain.all_buttons_types import ConfirmButton, EditEventButton, TransformEventButton

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

class TransformEventKeyboard:
    @staticmethod
    def build():
        builder = InlineKeyboardBuilder()

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

class EditEventKeyboard:
    @staticmethod
    def build():
        builder = InlineKeyboardBuilder()

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