from __future__ import annotations

import asyncio
import json
import time
from pathlib import Path

from aiogram import types
from aiogram.fsm.context import FSMContext
from sqlalchemy import select

from core.config import settings

from tg_bot.adapters.send_message import MessageSender

from tg_bot.domain import MessagesToUser
from tg_bot.domain import MessagesToUser, EditEventButton
from tg_bot.infra.init_db import async_session_factory
from parser_module.domain.models import Event

from calendar_actions.ics_generator import write_ics_for_project_event
from calendar_actions.google_calendar import (
    OAuthClient,
    GoogleAuthError,
    refresh_access_token,
    build_google_event_payload,
    insert_event_to_google_calendar,
)
from calendar_actions.google_oauth_web import (
    generate_pkce_pair,
    generate_state,
    build_authorization_url,
)

from tg_bot.domain.database.google_token import GoogleToken
from tg_bot.domain.database.google_oauth_state import GoogleOAuthState


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
                text=MessagesToUser.WRONG,
            )
            await callback.answer()
            return

        event = Event.model_validate(event_dict)

        if pressed_button == EditEventButton.EDIT_TO_YANDEX:
            await self.sender.send_text(callback.message, text=MessagesToUser.PLUG)
            await callback.answer()
            return

        if pressed_button == EditEventButton.EDIT_TO_GOOGLE:
            if not getattr(settings, "google_client_id", None) or not getattr(settings, "google_redirect_uri", None):
                await self.sender.send_text(callback.message, text=MessagesToUser.PLUG)
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

                async with async_session_factory() as session2:
                    result2 = await session2.execute(
                        select(GoogleToken).where(GoogleToken.telegram_id == telegram_id)
                    )
                    row2: GoogleToken | None = result2.scalar_one_or_none()
                    if row2:
                        row2.access_token = access_token
                        row2.expires_at = expires_at
                        row2.token_type = token_data.get("token_type")
                        row2.scope = token_data.get("scope")
                        await session2.commit()

            # Если refresh_token уже есть, то просто добавляем событие
            if token_row and token_row.refresh_token:
                try:
                    await add_event_with_refresh(token_row.refresh_token)
                    await self.sender.send_text(callback.message, MessagesToUser.ADDED_TO_GOOGLE)
                except GoogleAuthError as e:
                    await self.sender.send_text(callback.message, text=MessagesToUser.PLUG)
                await callback.answer()
                return

            # Иначе даём ссылку на авторизацию
            state_str = generate_state()
            code_verifier, code_challenge = generate_pkce_pair()
            scopes = ["https://www.googleapis.com/auth/calendar.events"]

            auth_url = build_authorization_url(
                client_id=settings.google_client_id,
                redirect_uri=settings.google_redirect_uri,
                scopes=scopes,
                state=state_str,
                code_challenge=code_challenge,
            )

            async with async_session_factory() as session3:
                session3.add(
                    GoogleOAuthState(
                        state=state_str,
                        telegram_id=telegram_id,
                        chat_id=chat_id,
                        code_verifier=code_verifier,
                        event_json=json.dumps(event_dict, ensure_ascii=False),
                    )
                )
                await session3.commit()

            await self.sender.send_text(
                callback.message, text=f"{MessagesToUser.PLUG} {auth_url}")
            await callback.answer()
            return

        if pressed_button == EditEventButton.MAKE_ICS:
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
            return

        await callback.answer()
