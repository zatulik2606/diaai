from datetime import timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.request import DialogRequest
from backend.repositories.request import RequestRepository
from backend.repositories.user import UserRepository
from backend.schemas.web import HistoryMessage, PaginatedHistoryResponse


class WebChatService:
    def __init__(self, session: AsyncSession) -> None:
        self._users = UserRepository(session)
        self._requests = RequestRepository(session)

    def _expand_messages(self, requests: list[DialogRequest]) -> list[HistoryMessage]:
        messages: list[HistoryMessage] = []
        for req in requests:
            messages.append(
                HistoryMessage(
                    id=str(req.id),
                    role="user",
                    text=req.content or "",
                    created_at=req.created_at,
                )
            )
            messages.append(
                HistoryMessage(
                    id=f"{req.id}-reply",
                    role="assistant",
                    text=req.reply,
                    created_at=req.created_at + timedelta(seconds=1),
                )
            )
        return messages

    async def get_history(
        self,
        *,
        telegram_id: int,
        limit: int,
        offset: int,
    ) -> PaginatedHistoryResponse:
        user = await self._users.require_by_telegram_id(telegram_id)
        total_requests = await self._requests.count_for_user(user.id)
        total = total_requests * 2

        request_offset = offset // 2
        skip_leading = offset % 2
        requests_needed = (limit + skip_leading + 1) // 2

        requests, _ = await self._requests.list_for_user_history(
            user.id,
            limit=requests_needed,
            offset=request_offset,
        )
        messages = self._expand_messages(requests)
        page = messages[skip_leading : skip_leading + limit]

        return PaginatedHistoryResponse(items=page, total=total, limit=limit, offset=offset)
