# Итерация backend 2: Summary

> **Статус итерации:** 🚧 In Progress (task-04). Summary обновляется по закрытии task-05.

## Сделано

### Task-03: Каркас backend ✅

- Пакет [`backend/`](../../../../../backend/): FastAPI, lifespan, RequestIdMiddleware
- API v1: `/assistant/messages`, `/events/food`, `/events/insulin` — stub 501
- Auth Bearer → 401; ErrorBody; Pydantic schemas по openapi
- `Makefile` (`backend-*`), `pyproject.toml`, `.env.example`
- Tests: `test_health.py`, `test_auth.py` — `make backend-test` зелёный
- Документы: [backend-structure.md](../../../tech/backend-structure.md)
- Детали: [task-03 summary](tasks/task-03-scaffold/summary.md)

### Task-04, Task-05

- 📋 не начаты

## Решения

- Пакет `backend/` в корне репо; `diaai` в `src/`
- `create_app()` для тестов; GET `/health` вне `/api/v1`
- 400 для пустого text+image в assistant (до impl)

## Отклонения от плана

Нет.

## Проблемы

Нет.

## DoD итерации

| Критерий | Статус |
|----------|--------|
| `make backend-run`, `/docs` v1 | ✅ task-03 |
| `make backend-test` после impl | ⏳ task-05 |
| endpoint'ы + PostgreSQL | ⏳ task-05 |
| без миграции бота | ⏳ (iteration-3) |

| Кто | Статус |
|-----|--------|
| Агент | 🚧 task-03 ✅ |
| Пользователь | ✅ `/docs` проверен (task-03) |

## Следующий шаг

[Task-04](tasks/task-04-api-tests/plan.md) — contract tests A/B.
