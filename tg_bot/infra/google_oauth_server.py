from __future__ import annotations

import asyncio
import json
import time
from typing import Optional

from aiohttp import web
from sqlalchemy import select, delete

from core.config import settings
from tg_bot.infra.init_db import async_session_factory
from tg_bot.infra.init_bot import bot

from tg_bot.domain import MessagesToUser

from calendar_actions.google_calendar import (
    OAuthClient as RefreshOAuthClient,
    refresh_access_token,
    build_google_event_payload,
    insert_event_to_google_calendar,
)
from calendar_actions.google_oauth_web import exchange_code_for_tokens

from tg_bot.domain.database.google_token import GoogleToken
from tg_bot.domain.database.google_oauth_state import GoogleOAuthState
from parser_module.domain.models import Event


async def _handle_google_callback(request: web.Request) -> web.Response:
    """GET /google/callback?code=...&state=..."""

    code = request.query.get("code")
    state = request.query.get("state")
    error = request.query.get("error")

    if error:
        return web.Response(text=f"Google OAuth error: {error}", status=400)

    if not code or not state:
        return web.Response(text="Missing code/state", status=400)

    async with async_session_factory() as session:
        res = await session.execute(
            select(GoogleOAuthState).where(GoogleOAuthState.state == state)
        )
        pending: Optional[GoogleOAuthState] = res.scalar_one_or_none()

        if pending is None:
            return web.Response(text="Unknown or expired state", status=400)

        ttl_seconds = 2 * 60 * 60
        if int(time.time()) - int(pending.created_at) > ttl_seconds:
            await session.delete(pending)
            await session.commit()
            return web.Response(text="State expired. Please try again.", status=400)

        try:
            token_data = await asyncio.to_thread(
                exchange_code_for_tokens,
                client_id=settings.google_client_id,
                client_secret=getattr(settings, "google_client_secret", None),
                redirect_uri=settings.google_redirect_uri,
                code=code,
                code_verifier=pending.code_verifier,
            )
        except Exception as e:
            return web.Response(text=f"Token exchange failed: {e}", status=500)

        refresh_token = token_data.get("refresh_token") or ""
        access_token = token_data.get("access_token")
        expires_in = int(token_data.get("expires_in", 3600))
        expires_at = int(time.time()) + expires_in

        res2 = await session.execute(
            select(GoogleToken).where(GoogleToken.telegram_id == pending.telegram_id)
        )
        row: Optional[GoogleToken] = res2.scalar_one_or_none()
        if row is None:
            row = GoogleToken(
                telegram_id=pending.telegram_id,
                refresh_token=refresh_token,
                access_token=access_token,
                expires_at=expires_at,
                token_type=token_data.get("token_type"),
                scope=token_data.get("scope"),
            )
            session.add(row)
        else:
            if refresh_token:
                row.refresh_token = refresh_token
            row.access_token = access_token
            row.expires_at = expires_at
            row.token_type = token_data.get("token_type")
            row.scope = token_data.get("scope")

        await session.delete(pending)
        await session.commit()

    try:
        if not access_token:
            if not refresh_token:
                raise RuntimeError("No access_token/refresh_token")

            oauth = RefreshOAuthClient(
                client_id=settings.google_client_id,
                client_secret=getattr(settings, "google_client_secret", None),
            )
            refreshed = await asyncio.to_thread(refresh_access_token, oauth, refresh_token)
            access_token = refreshed["access_token"]

        event = Event.model_validate(json.loads(pending.event_json))
        payload = build_google_event_payload(event)
        await asyncio.to_thread(insert_event_to_google_calendar, access_token, payload)

        await bot.send_message(pending.chat_id, text=MessagesToUser.ADDED_TO_GOOGLE_CAL)
    except Exception as e:
        try:
            await bot.send_message(pending.chat_id, text=MessagesToUser.WRONG)
        except Exception:
            pass

    return web.Response(
        text="Авторизация завершена. Можно закрыть эту вкладку и вернуться в Telegram.",
        content_type="text/plain",
    )


async def _handle_health(request: web.Request) -> web.Response:
    return web.Response(text="ok")


async def start_google_oauth_server() -> web.AppRunner:
    """Запускает aiohttp сервер"""

    app = web.Application()
    app.router.add_get("/health", _handle_health)
    app.router.add_get("/google/callback", _handle_google_callback)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host=settings.oauth_listen_host, port=settings.oauth_listen_port)
    await site.start()
    return runner


async def cleanup_oauth_states_task() -> None:
    """Периодически чистит старые state-записи, чтобы база не разрасталась"""
    ttl_seconds = 2 * 60 * 60
    while True:
        try:
            threshold = int(time.time()) - ttl_seconds
            async with async_session_factory() as session:
                await session.execute(
                    delete(GoogleOAuthState).where(GoogleOAuthState.created_at < threshold)
                )
                await session.commit()
        except Exception:
            pass

        await asyncio.sleep(15 * 60)
