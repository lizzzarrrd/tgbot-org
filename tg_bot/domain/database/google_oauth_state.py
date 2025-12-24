from __future__ import annotations

import time

from sqlalchemy import BigInteger, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class GoogleOAuthState(Base):
    """Храним временное состояние OAuth до прихода callback.

    state — случайная строка, которую мы передаём в Google authorize
    code_verifier — для PKCE (нужно на шаге обмена code -> token)
    event_json — событие, которое нужно добавить в календарь после авторизации
    """

    __tablename__ = "google_oauth_states"

    id: Mapped[int] = mapped_column(primary_key=True)
    state: Mapped[str] = mapped_column(String, unique=True, index=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, index=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, index=True)

    code_verifier: Mapped[str] = mapped_column(String, nullable=False)
    event_json: Mapped[str] = mapped_column(Text, nullable=False)

    created_at: Mapped[int] = mapped_column(Integer, default=lambda: int(time.time()))
