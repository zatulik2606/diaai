# Итерация backend 2: Summary

> **Статус итерации:** ✅ Done (2026-06-13). Задачи 03–05 закрыты.

## Сделано

### Task-03: Каркас backend ✅

- Пакет [`backend/`](../../../../../backend/): FastAPI, `create_app`, lifespan, RequestIdMiddleware, auth Bearer
- API v1 stub 501; schemas; Makefile; `.env.example`
- Детали: [task-03 summary](tasks/task-03-scaffold/summary.md)

### Task-04: API-тесты ✅

- 17 contract-тестов: auth, validation, assistant, events (501 phase)
- `conftest.py`: AsyncClient, payload fixtures
- Детали: [task-04 summary](tasks/task-04-api-tests/summary.md)

### Task-05: Endpoint impl ✅

- PostgreSQL: `database.py`, 5 ORM, Alembic `001`, `docker-compose.yml` (порт **5433**)
- Services: `llm_service`, `assistant_service`, `events_service`; repositories
- Endpoint'ы: assistant **200**, events **201/200**; domain 403/404
- **21** тест (`make backend-test`); live integration (httpx → backend)
- [data-model.md](../../../../../data-model.md) — секция SQL-схема MVP
- Детали: [task-05 summary](tasks/task-05-api-impl/summary.md)

## Решения

- **TDD:** task-04 assert 501 → task-05 обновление на 200/201 без смены auth/422-тестов
- **Тесты:** sqlite in-memory + `dependency_overrides`; mock LLM
- **Dev PG:** host port 5433 (конфликт 5432 с другим compose)
- **ORM:** `DialogRequest` вместо `Request` (Starlette)
- **Env:** `BACKEND_SERVICE_TOKEN` в кавычках при `:`; один `OPENROUTER_API_KEY` без дублей
- **PhotoAnalysis:** вне scope; media в JSONB `dialog_requests`

## Отклонения от плана

- PostgreSQL на **5433**, не 5432 — зафиксировано в `docker-compose.yml` и config default
- User DoD task-04 («просмотр тестов») закрыт в рамках закрытия итерации

## Проблемы

- `.env`: дублирующий обрезанный `OPENROUTER_API_KEY` → 502 LLM (исправлено при интеграционной проверке)
- Docker daemon / занятый 5432 — решено портом 5433

## DoD итерации

| Критерий | Статус |
|----------|--------|
| `make backend-run`, `/docs` v1, auth | ✅ |
| contract + impl tests (21) | ✅ |
| endpoint'ы по `docs/api/` | ✅ |
| PostgreSQL + Alembic | ✅ |
| live: assistant + events | ✅ |
| миграция бота | → iteration-3, task-07 |

| Кто | Статус |
|-----|--------|
| Агент | ✅ `make backend-test`, `make backend-lint`, migrate, run |
| Пользователь | ✅ `/docs`, curl A/B, PG persistence |

## Артефакты

- Код: [`backend/`](../../../../../backend/), [`alembic/`](../../../../../alembic/), [`docker-compose.yml`](../../../../../docker-compose.yml)
- План: [iteration-2-core/plan.md](plan.md)

## Следующий шаг

[iteration-3-delivery](../iteration-3-delivery/plan.md) — task-06 ✅; task-07 (bot → API), task-08 (quality).
