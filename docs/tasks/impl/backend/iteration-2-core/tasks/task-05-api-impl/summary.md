# Task 05: Summary

## Сделано

- **Database:** `database.py`, 5 ORM, Alembic `001`, `docker-compose.yml` (PG **5433**), `make backend-migrate`
- **Repositories + services:** A/B, OpenRouter, ownership 403/404
- **Tests:** 21 passed; sqlite + mock LLM
- **Live:** assistant 200, events 201 (httpx client integration)

## Решения

- PG host port 5433 (конфликт с 5432)
- `DialogRequest` — имя ORM-модели
- `.env`: один `OPENROUTER_API_KEY`; `BACKEND_SERVICE_TOKEN` в кавычках при `:`

## DoD

| Кто | Статус |
|-----|--------|
| Агент | ✅ |
| Пользователь | ✅ curl + PG |

## Следующий шаг

Task-06 — README, OpenAPI sync.
