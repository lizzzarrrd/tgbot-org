from __future__ import annotations

import asyncio
import time

from aiogram import types
from aiogram.fsm.context import FSMContext
from pathlib import Path
from sqlalchemy import select


from tg_bot.adapters import MessageSender
from tg_bot.domain import MessagesToUser, EditEventButton
from tg_bot.infra.init_db import async_session_factory

from core.config import settings

from parser_module.domain.models import Event

from calendar_actions.ics_generator import write_ics_for_project_event
from calendar_actions.google_calendar import (
    OAuthClient,
    GoogleAuthError,
    start_device_flow,
    poll_device_flow_token,
    refresh_access_token,
    build_google_event_payload,
    insert_event_to_google_calendar,
)

from tg_bot.domain.database.google_token import GoogleToken

class AddictionToCalendarHandler:
    def __init__(self, sender: MessageSender) -> None:
        self.sender: MessageSender = sender

    async def handle_for_calendar_addiction(
            self,
            callback: types.CallbackQuery,
            state: FSMContext,
            ) -> None:
        pressed_button: EditEventButton = EditEventButton(callback.data)
        if callback.message:
            await callback.message.edit_reply_markup(reply_markup=None)

        data = await state.get_data()
        event_dict = data.get("event")

        if not event_dict:
            await self.sender.send_text(
                callback.message,
                "Сообщение не найдено, отправьте еще раз",
            )
            await callback.answer()
            return

        event = Event.model_validate(event_dict)

        if pressed_button == EditEventButton.EDIT_TO_YANDEX:
            # Polina_s_module_for_yandex_calendar(parsed_event from Egor)
            await self.sender.send_text(callback.message,
                                        MessagesToUser.ADDED_TO_YANDEX)
        elif pressed_button == EditEventButton.EDIT_TO_GOOGLE:
            if not getattr(settings, "google_client_id", None):
                await self.sender.send_text(
                    callback.message,
                    "Google Calendar не настроен: отсутствует GOOGLE_CLIENT_ID в .env",
                )
                await callback.answer()
                return

            telegram_id = callback.from_user.id if callback.from_user else 0
            chat_id = callback.message.chat.id if callback.message else 0

            oauth = OAuthClient(
                client_id=settings.google_client_id,
                client_secret=getattr(settings, "google_client_secret", None),
            )

            async with async_session_factory() as session:
                result = await session.execute(
                    select(GoogleToken).where(GoogleToken.telegram_id == telegram_id)
                )
                token_row: GoogleToken | None = result.scalar_one_or_none()

            async def add_event_with_refresh(refresh_token: str) -> None:
                token_data = await asyncio.to_thread(refresh_access_token, oauth, refresh_token)
                access_token = token_data["access_token"]
                expires_in = int(token_data.get("expires_in", 3600))
                expires_at = int(time.time()) + expires_in

                payload = build_google_event_payload(event)
                await asyncio.to_thread(insert_event_to_google_calendar, access_token, payload)

                async with async_session_factory() as session:
                    result2 = await session.execute(
                        select(GoogleToken).where(GoogleToken.telegram_id == telegram_id)
                    )
                    row2: GoogleToken | None = result2.scalar_one_or_none()
                    if row2:
                        row2.access_token = access_token
                        row2.expires_at = expires_at
                        row2.token_type = token_data.get("token_type")
                        row2.scope = token_data.get("scope")
                        await session.commit()

            if token_row and token_row.refresh_token:
                try:
                    await add_event_with_refresh(token_row.refresh_token)
                    await self.sender.send_text(callback.message, MessagesToUser.ADDED_TO_GOOGLE)
                except GoogleAuthError as e:
                    await self.sender.send_text(
                        callback.message, f"Не получилось добавить в Google Calendar: {e}"
                    )
                await callback.answer()
                return

            try:
                device = await asyncio.to_thread(start_device_flow, oauth)
            except GoogleAuthError as e:
                await self.sender.send_text(callback.message, f"Не удалось начать авторизацию Google: {e}")
                await callback.answer()
                return

            user_code = device["user_code"]
            verification_url = device.get("verification_url") or device.get("verification_uri")
            device_code = device["device_code"]
            expires_in = int(device.get("expires_in", 600))
            interval = int(device.get("interval", 5))

            await self.sender.send_text(
                callback.message,
                "Чтобы добавить в Google Calendar, нужно один раз авторизоваться.\n\n"
                f"1) Открой: {verification_url}\n"
                f"2) Введи код: {user_code}\n\n"
                "Я подожду авторизацию и добавлю событие автоматически.",
            )

            async def background_wait_and_add() -> None:
                try:
                    token_data = await asyncio.to_thread(
                        poll_device_flow_token,
                        oauth,
                        device_code,
                        interval,
                        expires_in,
                    )

                    refresh_token = token_data.get("refresh_token") or ""
                    access_token = token_data["access_token"]
                    expires_at = int(time.time()) + int(token_data.get("expires_in", 3600))

                    async with async_session_factory() as session:
                        result3 = await session.execute(
                            select(GoogleToken).where(GoogleToken.telegram_id == telegram_id)
                        )
                        row3: GoogleToken | None = result3.scalar_one_or_none()

                        if row3 is None:
                            row3 = GoogleToken(
                                telegram_id=telegram_id,
                                refresh_token=refresh_token,
                                access_token=access_token,
                                expires_at=expires_at,
                                token_type=token_data.get("token_type"),
                                scope=token_data.get("scope"),
                            )
                            session.add(row3)
                        else:
                            if refresh_token:
                                row3.refresh_token = refresh_token
                            row3.access_token = access_token
                            row3.expires_at = expires_at
                            row3.token_type = token_data.get("token_type")
                            row3.scope = token_data.get("scope")

                        await session.commit()

                    payload = build_google_event_payload(event)
                    await asyncio.to_thread(
                        insert_event_to_google_calendar,
                        access_token,
                        payload)

                    await self.sender.send_text_to_chat(
                        chat_id,
                        MessagesToUser.ADDED_TO_GOOGLE)

                except GoogleAuthError as e:
                    await self.sender.send_text_to_chat(chat_id,
                                                        f"Google авторизация не удалась: {e}")
                except Exception as e:
                    await self.sender.send_text_to_chat(chat_id,
                                                        f"Ошибка при добавлении в Google Calendar: {e}")

            asyncio.create_task(background_wait_and_add())

            await callback.answer()
            return

        elif pressed_button == EditEventButton.MAKE_ICS:
            user_id = callback.from_user.id if callback.from_user else 0
            out_dir = Path("/data/ics") / str(user_id)
            out_path = out_dir / "event.ics"

            file_path = str(write_ics_for_project_event(event, out_path))
            await self.sender.send_file(
                callback.message,
                file_path=file_path,
                caption=MessagesToUser.TAKE_ICS,
            )
        await callback.answer()
