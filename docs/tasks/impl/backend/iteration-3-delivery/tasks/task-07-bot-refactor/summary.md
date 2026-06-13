# Task 07: Summary — Рефакторинг бота → API

## Сделано

- **`src/diaai/backend_client.py`** — `httpx.AsyncClient`, Bearer, `X-Request-Id`, `send_assistant_message`, маппинг ошибок 401/502/503/400/422.
- **`handlers.py`** — text/photo через backend; `/start` без сброса RAM (история в PG).
- **`main.py`, `bot.py`, `config.py`** — wiring `BackendClient`; env: `BACKEND_URL`, `BACKEND_SERVICE_TOKEN`; без `LlmClient`/`SessionStore`/`Prompt` в prod.
- **`.env.example`, `README.md`** — bot требует backend; quick start в два шага.
- **`docs/vision.md`, `docs/integrations.md`, `docs/tasks/tasklist-bot.md`** — bot → backend ✅.

## Legacy

- `llm_client.py`, `session_store.py`, `prompt.py` — не используются prod-путём; файлы сохранены.

## Тесты (python-testing-patterns)

- `tests/test_backend_client.py` — async unit-тесты с `httpx.MockTransport`: 200, auth headers, photo payload, 401/502/503/422, connect error, empty reply.
- `tests/test_config.py` — `Config.from_env` с `monkeypatch` (изоляция от `.env`).
- `make test` — backend (21) + bot (15) = **36 passed**.

## Отклонения от плана

- `/start` не сбрасывает диалог в PG (нет DELETE endpoint) — по плану, post-MVP.
- ~~Unit-тесты бота не добавляли~~ — добавлены unit-тесты клиента и config (без Telegram e2e).

## Проверки

| Критерий | Статус |
|----------|--------|
| `make lint` | ✅ |
| `make test` (36) | ✅ |
| `make backend-test` | ✅ 21 passed |
| prod-путь без `llm_client` | ✅ |

## Следующий шаг

Task-08 — structured logging, quality gate.
