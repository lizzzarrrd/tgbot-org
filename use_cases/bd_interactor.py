from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from domain import User


class BdInteractor:
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        """Проверка, есть ли пользователь в БД"""
        result = await self.session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()

    async def create(self, telegram_id: int) -> User:
        """Создание нового пользователя"""
        user = User(
            telegram_id=telegram_id,
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_or_create(self, telegram_id: int) -> User:
        user = await self.get_by_telegram_id(telegram_id)
        if user:
            return user
        return await self.create(telegram_id)
