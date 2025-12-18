from sqlalchemy import BigInteger, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    # username: Mapped[str | None] = mapped_column(String(64))
    # created_at: Mapped[DateTime] = mapped_column(
    #     DateTime(timezone=True),
    #     server_default=func.now(),
    # )