# Итерация backend 2: Сборка ядра

Опирается на [tasklist-backend.md](../../../tasklist-backend.md) · [iteration-1-foundation](../iteration-1-foundation/plan.md) · [ADR-002](../../../../../adr/adr-002-backend-stack.md)

Skills: [fastapi-templates](.agents/skills/fastapi-templates/SKILL.md) · [python-testing-patterns](.agents/skills/python-testing-patterns/SKILL.md)

## Цель

Реализовать backend по контрактам итерации 1: каркас FastAPI, contract-тесты, endpoint'ы A/B + PostgreSQL + OpenRouter.

## Статус

✅ Done — task-03, 04, 05.

## Ценность

- Рабочее API v1: assistant + events
- Персистентность в PostgreSQL; история диалогов
- TDD: contract tests → impl (501 → 200/201)
- Готовность к поставке (iteration-3)

## Архитектура

```mermaid
flowchart TB
    subgraph api [api/v1]
        assistant["assistant.py"]
        events["events.py"]
    end
    subgraph services [services]
        asst_svc["assistant_service"]
        evt_svc["events_service"]
        llm["llm_service"]
    end
    subgraph data [persistence]
        repos["repositories/"]
        db["database.py get_db"]
        pg["PostgreSQL"]
    end
    assistant --> asst_svc
    events --> evt_svc
    asst_svc --> llm
    asst_svc --> repos
    evt_svc --> repos
    repos --> db
    db --> pg
```

**Сценарий A:** `telegram_id` → User → Dialog → история Request → OpenRouter → 200.

**Сценарий B:** POST food/insulin → 201; GET food; 403/404 по FK ownership.

## Стратегия БД и тестов

| Среда | Подключение | Назначение |
|-------|-------------|------------|
| Runtime / dev | `DATABASE_URL=postgresql+asyncpg://diaai:diaai@localhost:5433/diaai` | PG через docker-compose (порт **5433** — 5432 часто занят) |
| pytest | `sqlite+aiosqlite:///:memory:` + `dependency_overrides[get_db]` | CI без Docker |

## Задачи итерации

| # | Задача | Статус | Документы |
|---|--------|--------|-----------|
| 03 | Каркас backend + API-скелет | ✅ Done | [plan](tasks/task-03-scaffold/plan.md) · [summary](tasks/task-03-scaffold/summary.md) |
| 04 | API-тесты сценариев | ✅ Done | [plan](tasks/task-04-api-tests/plan.md) · [summary](tasks/task-04-api-tests/summary.md) |
| 05 | Endpoint'ы и серверная логика | ✅ Done | [plan](tasks/task-05-api-impl/plan.md) · [summary](tasks/task-05-api-impl/summary.md) |

### Task-05 (кратко)

| Слой | Артефакты |
|------|-----------|
| DB | `database.py`, 5 ORM-моделей, Alembic `001`, `docker-compose.yml` |
| Repos | user, dialog, request, food_event, insulin_event |
| Services | `llm_service`, `assistant_service`, `events_service` |
| Tests | 21 (mock LLM, sqlite, domain 403/404) |

## Критерии завершения итерации

- [x] `make backend-run` → `/health` 200; `/docs` v1
- [x] contract + impl tests — **21 passed**
- [x] endpoint'ы по [docs/api/](../../../../../api/)
- [x] PostgreSQL (Alembic + docker-compose, порт 5433)
- [x] live: assistant 200, events 201 (OpenRouter + auth)
- [x] **без** миграции бота (→ iteration-3, task-07)

## Dev quick start

```bash
docker compose up -d
make backend-migrate
make backend-run   # http://127.0.0.1:8000/docs
make backend-test
```

Env: `BACKEND_SERVICE_TOKEN`, `DATABASE_URL`, `OPENROUTER_API_KEY`, `LLM_MODEL` — см. `.env.example`.

## Следующая итерация

[iteration-3-delivery](../iteration-3-delivery/plan.md) — задачи 06–08.

## Документы

- 📝 [Summary](summary.md) — ✅ итерация закрыта
