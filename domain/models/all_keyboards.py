from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)

from domain.models.buttons import (
    MainMenuButton,
    ConfirmButton,
    EditEventButton,
)


class MainMenuKeyboard:
    @staticmethod
    def build() -> ReplyKeyboardMarkup:
        kb = ReplyKeyboardMarkup(resize_keyboard=True)

        for button in MainMenuButton:
            kb.add(KeyboardButton(text=button.value))

        return kb


class ConfirmKeyboard:
    @staticmethod
    def build() -> InlineKeyboardMarkup:
        kb = InlineKeyboardMarkup()

        kb.add(
            InlineKeyboardButton(
                text="Да",
                callback_data=ConfirmButton.YES.value,
            )
        )
        kb.add(
            InlineKeyboardButton(
                text="Нет",
                callback_data=ConfirmButton.NO.value,
            )
        )

        return kb


class EditEventKeyboard:
    @staticmethod
    def build() -> InlineKeyboardMarkup:
        kb = InlineKeyboardMarkup()

        kb.add(
            InlineKeyboardButton(
                text="Изменить дату",
                callback_data=EditEventButton.EDIT_DATE.value,
            )
        )
        kb.add(
            InlineKeyboardButton(
                text="Изменить время",
                callback_data=EditEventButton.EDIT_TIME.value,
            )
        )
        kb.add(
            InlineKeyboardButton(
                text="Получить .ics",
                callback_data=EditEventButton.MAKE_ICS.value,
            )
        )
        kb.add(
            InlineKeyboardButton(
                text="Добавить в календарь",
                callback_data=EditEventButton.SAVE_CALENDAR.value,
            )
        )

        return kb