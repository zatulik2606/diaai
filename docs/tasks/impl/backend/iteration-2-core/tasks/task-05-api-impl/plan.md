# Task 05: Endpoint'ы и серверная логика

Опирается на [task-04-api-tests/plan.md](../task-04-api-tests/plan.md) · [ADR-002](../../../../../../adr/adr-002-backend-stack.md) · [data-model.md](../../../../../../data-model.md)

Skills: [fastapi-templates](.agents/skills/fastapi-templates/SKILL.md) — lifespan, get_db, repository/service layers

## Цель

Реализовать endpoint'ы A/B по контрактам: LLM, PostgreSQL, идентификация по `telegram_id`.

## Архитектура

```
backend/
├── main.py              # lifespan: DB connect/dispose
├── config.py
├── database.py          # async engine, get_db
├── api/v1/              # handlers → services
├── schemas/
├── services/            # assistant_service, events_service, llm_service
├── repositories/
└── models/              # SQLAlchemy ORM
alembic/                 # migrations (корень репо)
```

## Фазы реализации

### 1. Database + ORM + миграция

- `database.py`: `AsyncSessionLocal`, `get_db` → 503 без БД
- Модели: User, Dialog, DialogRequest, FoodEvent, InsulinEvent
- Alembic `001_initial_schema`
- `docker-compose.yml` — PostgreSQL (host port **5433**)
- Makefile: `backend-migrate`

### 2. Repositories

- get-or-create user/dialog; CRUD events/requests
- ownership: `request_id`, `food_event_id`

### 3. LLM service

- OpenRouter через openai-клиент; промпт `prompts/system.txt`
- 502 `LLM_UNAVAILABLE` при ошибках

### 4. Сценарий A — `POST /assistant/messages`

- Response 200: `dialog_id`, `request_id`, `reply`
- media в JSONB (PhotoAnalysis — post-MVP)

### 5. Сценарий B — events

| Endpoint | Код | Domain |
|----------|-----|--------|
| POST `/events/food` | 201 | 403/404 `request_id` |
| POST `/events/insulin` | 201 | 403/404 `food_event_id` |
| GET `/events/food` | 200 | 422 invalid `from`/`to` |

### 6. Тесты (обновление task-04)

| Файл | Изменение |
|------|-----------|
| `test_assistant.py` | 501→200 + mock LLM |
| `test_events.py` | 501→201/200 |
| `test_events_domain.py` | 403/404 |

## Затронутые файлы

- `backend/services/`, `repositories/`, `models/`, `database.py`
- `backend/api/v1/assistant.py`, `events.py`
- `alembic/versions/`, `docker-compose.yml`, `.env.example`, `pyproject.toml`
- `docs/data-model.md` — секция SQL-схема MVP

## DoD

| Кто | Критерий | Статус |
|-----|----------|--------|
| Агент | `make backend-test` + lint; ≥20 тестов | ✅ 21 |
| Агент | `alembic upgrade head`, `make backend-run` | ✅ |
| Пользователь | curl A/B; данные в PG после перезапуска | ✅ проверено |

## Вне scope

- Bot → API (task-07)
- PhotoAnalysis таблица, object storage
- CORS, web auth

## Следующий шаг

[iteration-3-delivery](../../iteration-3-delivery/plan.md) — task-06 docs.
