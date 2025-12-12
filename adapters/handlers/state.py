from __future__ import annotations
from typing import Optional


class RegistrationState:
    """
    Проверяет регистрацию пользователя.
    """

    def __init__(self, user_repo):
        self.user_repo = user_repo

    async def is_registered(self, tg_id: int) -> bool:
        user = await self.user_repo.get_by_tg_id(tg_id)
        return user is not None

    async def ensure_registered(self, tg_id: int) -> None:
        if not await self.is_registered(tg_id):
            raise PermissionError("Пользователь не зарегистрирован")

    async def register(
        self,
        tg_id: int,
        username: Optional[str],
        first_name: Optional[str],
        last_name: Optional[str],
        registered_at
    ):
        await self.user_repo.create_or_update_user(
            tg_id=tg_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            registered_at=registered_at
        )