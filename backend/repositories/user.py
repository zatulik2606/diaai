from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.exceptions import AppError
from backend.models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        result = await self._session.execute(select(User).where(User.telegram_id == telegram_id))
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> User | None:
        normalized = username.lstrip("@").lower()
        result = await self._session.execute(
            select(User).where(User.telegram_username == normalized)
        )
        return result.scalar_one_or_none()

    async def list_diabetics(self) -> list[User]:
        result = await self._session.execute(
            select(User)
            .where(User.role == "diabetic", User.is_active.is_(True))
            .order_by(User.display_name.asc().nulls_last())
        )
        return list(result.scalars().all())

    async def require_by_telegram_id(self, telegram_id: int) -> User:
        user = await self.get_by_telegram_id(telegram_id)
        if user is None:
            raise AppError(
                code="NOT_FOUND",
                message="User not found",
                status_code=404,
            )
        return user

    async def require_doctor(self, telegram_id: int) -> User:
        user = await self.require_by_telegram_id(telegram_id)
        if user.role != "doctor":
            raise AppError(
                code="FORBIDDEN",
                message="Doctor role required",
                status_code=403,
            )
        return user

    async def get_or_create(self, telegram_id: int) -> User:
        user = await self.get_by_telegram_id(telegram_id)
        if user is not None:
            return user
        user = User(telegram_id=telegram_id)
        self._session.add(user)
        await self._session.flush()
        return user

    async def get_by_id(self, user_id) -> User | None:
        return await self._session.get(User, user_id)

    async def create_doctor(
        self,
        *,
        display_name: str,
        email: str | None = None,
        telegram_id: int | None = None,
    ) -> User:
        user = User(
            role="doctor",
            display_name=display_name,
            email=email,
            telegram_id=telegram_id,
        )
        self._session.add(user)
        await self._session.flush()
        return user
