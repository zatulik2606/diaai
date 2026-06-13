# Итерация backend 2: Summary

> **Статус итерации:** 🚧 In Progress (task-05). Summary обновляется по закрытии task-05.

## Сделано

### Task-03: Каркас backend ✅

- Пакет [`backend/`](../../../../../backend/): FastAPI, lifespan, RequestIdMiddleware
- API v1 stub 501; auth; schemas; Makefile; `.env.example`
- Детали: [task-03 summary](tasks/task-03-scaffold/summary.md)

### Task-04: API-тесты ✅

- 17 contract-тестов: auth (4), validation (5), assistant (4), events (3), health (1)
- Happy-path assert 501; error paths финальные (401/422/400)
- Проверка: `make backend-test`, coverage backend ~99%
- Детали: [task-04 summary](tasks/task-04-api-tests/summary.md)

### Task-05

- 🚧 Next — endpoint impl + PostgreSQL

## Решения

- Stub-тесты зелёные на 501; TDD handoff в task-05
- 403/404 — только с БД (task-05)
- pytest-cov — ad-hoc (`uv run --with pytest-cov`); в dev-зависимости — task-08

## Отклонения от плана

Нет.

## DoD итерации

| Критерий | Статус |
|----------|--------|
| `make backend-run`, `/docs` v1 | ✅ task-03 |
| contract tests (17) | ✅ task-04 |
| impl A/B + PostgreSQL | ⏳ task-05 |
| `make backend-test` с 200/201 | ⏳ task-05 |

## Следующий шаг

[Task-05](tasks/task-05-api-impl/plan.md) — impl A/B + PostgreSQL; обновить happy-path assertions.
