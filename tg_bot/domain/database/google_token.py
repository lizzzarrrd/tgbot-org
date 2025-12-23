from __future__ import annotations

from sqlalchemy import BigInteger, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class GoogleToken(Base):
    __tablename__ = "google_tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)

    refresh_token: Mapped[str] = mapped_column(String, nullable=False)

    access_token: Mapped[str | None] = mapped_column(String, nullable=True)
    token_type: Mapped[str | None] = mapped_column(String, nullable=True)
    scope: Mapped[str | None] = mapped_column(String, nullable=True)

    expires_at: Mapped[int | None] = mapped_column(Integer, nullable=True)
