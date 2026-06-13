# Task 05: Endpoint'ы и серверная логика

Опирается на [ADR-002](../../../../../../adr/adr-002-backend-stack.md) · [data-model.md](../../../../../../data-model.md) · [task-04-api-tests/plan.md](../task-04-api-tests/plan.md)

Skills: [fastapi-templates](.agents/skills/fastapi-templates/SKILL.md) — lifespan, get_db, repository/service layers

## Цель

Реализовать endpoint'ы A/B по контрактам: LLM, PostgreSQL, идентификация по `telegram_id`.

## Архитектура (ADR-002 + fastapi-templates)

```
backend/
├── main.py              # lifespan: DB connect/disconnect
├── config.py
├── api/v1/              # handlers → services
├── schemas/
├── services/            # assistant_service, events_service, llm_service
├── repositories/        # user, dialog, request, food_event, insulin_event
└── models/              # SQLAlchemy ORM
alembic/                 # migrations
```

## Состав работ

### 1. Database (lifespan + DI)

- `database.py`: async engine, `AsyncSessionLocal`, `get_db` dependency
- lifespan в `main.py`: connect on startup, dispose on shutdown
- Alembic: начальная миграция по [data-model.md](../../../../../../data-model.md) и [adr-001](../../../../../../adr/adr-001-database.md)

### 2. ORM models + repositories

- User (telegram_id), Dialog, Request, FoodEvent, InsulinEvent
- тонкие repositories — CRUD без лишних абстракций

### 3. Сценарий A — `POST /assistant/messages`

- get-or-create user/dialog по `telegram_id`
- загрузка истории (env `LLM_MAX_HISTORY`)
- `llm_service` → OpenRouter (openai client)
- сохранение Request + reply
- ошибки: 400/502/503 по [conventions.md](../../../../../../api/conventions.md)

### 4. Сценарий B — events

- POST `/events/food`, `/events/insulin` → 201
- GET `/events/food` (optional MVP) — list by telegram_id, from/to
- 403/404 для чужих `request_id` / `food_event_id`

### 5. Замена stub 501 на реализацию

- все contract tests из task-04 зелёные

### 6. Документы

- актуализировать [data-model.md](../../../../../../data-model.md), [integrations.md](../../../../../../integrations.md)

## Затронутые файлы

- `backend/services/`, `backend/repositories/`, `backend/models/`
- `backend/api/v1/assistant.py`, `events.py`
- `alembic/versions/`, `.env.example`
- `docs/data-model.md`, `docs/integrations.md`

## DoD

| Кто | Критерий |
|-----|----------|
| Агент | `make backend-test` зелёный; данные переживают перезапуск PG |
| Пользователь | curl — сценарии A и B; запись в БД |

## Следующий шаг

[iteration-3-delivery](../../iteration-3-delivery/plan.md) — task-06 docs.
