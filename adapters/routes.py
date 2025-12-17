from aiogram import F, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from adapters import (MessageHandler, MessageSender, StartHandler, ConfirmHandler, ChangeEventHandler, AddictionToCalendarHandler)
from domain import ConfirmButton, EditEventButton, TransformEventButton
from infra.init_bot import bot, router


sender: MessageSender = MessageSender(bot)
start_handler: StartHandler = StartHandler(sender)
message_handler: MessageHandler = MessageHandler(sender)
confirm_handler: ConfirmHandler = ConfirmHandler(sender)
change_event_handler: ChangeEventHandler = ChangeEventHandler(sender)
addiction_to_calendar_handler: AddictionToCalendarHandler = AddictionToCalendarHandler(sender)


@router.message(CommandStart())
async def start_command(message: types.Message) -> None:
    await start_handler.handle(message)


@router.message()
async def all_messages(message: types.Message, state: FSMContext) -> None:
    await message_handler.handle(message, state)


@router.callback_query(
    F.data.in_(
        {
            ConfirmButton.YES,
            ConfirmButton.NO,
            ConfirmButton.REJECT,
        }
    )
)
async def confirm_callbacks(callback: types.CallbackQuery) -> None:
    await confirm_handler.handle_for_confirm(callback)


@router.callback_query(
    F.data.in_(
        {
            EditEventButton.EDIT_TO_YANDEX,
            EditEventButton.EDIT_TO_GOOGLE,
            EditEventButton.MAKE_ICS,
        }
    )
)
async def calendar_addiction_callbacks(
    callback: types.CallbackQuery,
) -> None:
    await addiction_to_calendar_handler.handle_for_calendar_addiction(callback)


@router.callback_query(
    F.data.in_(
        {
            TransformEventButton.TRANSORM_DATE,
            TransformEventButton.TRANSORM_TIME,
            TransformEventButton.TRANSORM_NAME,
            TransformEventButton.TRANSORM_DESCRIPTION,
        }
    )
)
async def calendar_addiction_callbacks(
    callback: types.CallbackQuery,
    state: FSMContext
) -> None:
    await change_event_handler.handle_for_event_changing_info(callback, state)