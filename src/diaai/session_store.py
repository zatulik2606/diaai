from __future__ import annotations

from collections import defaultdict
from typing import Any

type Message = dict[str, Any]


class SessionStore:
    def __init__(self, max_history_pairs: int) -> None:
        self._max_messages = max_history_pairs * 2
        self._store: defaultdict[int, list[Message]] = defaultdict(list)

    def get_history(self, chat_id: int) -> list[Message]:
        return list(self._store[chat_id])

    def add_message(self, chat_id: int, role: str, content: Any) -> None:
        self._store[chat_id].append({"role": role, "content": content})
        if len(self._store[chat_id]) > self._max_messages:
            self._store[chat_id] = self._store[chat_id][-self._max_messages :]

    def clear(self, chat_id: int) -> None:
        self._store.pop(chat_id, None)
