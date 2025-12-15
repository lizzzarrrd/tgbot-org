from __future__ import annotations
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def main_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("Создать событие"))
    kb.add(KeyboardButton("Мои события"))
    kb.add(KeyboardButton("Мои группы"))
    return kb


def confirm_buttons() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Да", callback_data="event_yes"))
    kb.add(InlineKeyboardButton("Нет", callback_data="event_no"))
    return kb


def edit_event_buttons() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Изменить дату", callback_data="edit_date"))
    kb.add(InlineKeyboardButton("Изменить время", callback_data="edit_time"))
    kb.add(InlineKeyboardButton("Получить .ics", callback_data="make_ics"))
    kb.add(InlineKeyboardButton("Добавить в календарь", callback_data="save_calendar"))
    return kb