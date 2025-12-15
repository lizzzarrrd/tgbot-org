from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)

from aiogram.utils.keyboard import InlineKeyboardBuilder
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
    def build():
        builder = InlineKeyboardBuilder()

        builder.button(
            text="Да",
            callback_data=ConfirmButton.YES.value,
        )
        builder.button(
            text="Нет",
            callback_data=ConfirmButton.NO.value,
        )

        builder.adjust(2)
        return builder.as_markup()

class EditEventKeyboard:
    @staticmethod
    def build():
        builder = InlineKeyboardBuilder()

        builder.button(
            text="Изменить дату",
            callback_data=EditEventButton.EDIT_DATE.value,
        )
        builder.button(
            text="Изменить время",
            callback_data=EditEventButton.EDIT_TIME.value,
        )
        builder.button(
            text="Получить .ics",
            callback_data=EditEventButton.MAKE_ICS.value,
        )
        builder.button(
            text="Добавить в календарь",
            callback_data=EditEventButton.SAVE_CALENDAR.value,
        )

        builder.adjust(1)
        return builder.as_markup()