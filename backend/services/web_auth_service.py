from sqlalchemy.ext.asyncio import AsyncSession

from backend.exceptions import AppError
from backend.repositories.user import UserRepository
from backend.schemas.web import AuthResolveResponse


class WebAuthService:
    def __init__(self, session: AsyncSession) -> None:
        self._users = UserRepository(session)

    async def resolve_username(self, username: str) -> AuthResolveResponse:
        normalized = username.strip()
        if not normalized:
            raise AppError(
                code="NOT_FOUND",
                message="User not found",
                status_code=404,
            )
        user = await self._users.get_by_username(normalized)
        if user is None:
            raise AppError(
                code="NOT_FOUND",
                message="User not found",
                status_code=404,
            )
        return AuthResolveResponse(
            user_id=user.id,
            telegram_id=user.telegram_id,
            role=user.role,
            display_name=user.display_name,
        )
