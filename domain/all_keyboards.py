from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from domain.all_buttons_types import MainMenuButton, ConfirmButton, EditEventButton


class MainMenuKeyboard:
    @staticmethod
    def build() -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text=MainMenuButton.CREATE_EVENT.value)],
                [KeyboardButton(text=MainMenuButton.MY_EVENTS.value)],
                [KeyboardButton(text=MainMenuButton.MY_GROUPS.value)],
            ],
            resize_keyboard=True,
        )


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