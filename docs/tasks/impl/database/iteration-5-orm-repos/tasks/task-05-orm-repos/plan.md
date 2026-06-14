# Task 05: ORM, репозитории, backend

Опирается на [iteration-5/plan.md](../../plan.md) · [tasklist-database.md](../../../../../tasklist-database.md)

## Цель

Миграция `002_*`, models/repos, wiring services — полный data layer в PostgreSQL.

## Что делаем

1. `alembic/versions/002_full_data_layer.py`
2. Models: photo_analysis, progress_snapshot, recommendation, consultation; extend User
3. Repositories для новых таблиц
4. `assistant_service` → photo_analysis persist; progress/consultation service stubs
5. Seed v2, db_inspect, tests, docs

## DoD

`make db-reset && make test`; `make lint` green.

## Make-команды

`make db-reset`, `make backend-test`, `make test`, `uv run alembic downgrade -1`
