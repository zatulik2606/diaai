# Итерация database 4: Summary

> **Статус:** ✅ Done

План: [plan.md](plan.md)

## Сделано

### Task-04: Инфраструктура, seed, команды ✅

- One-command окружение: `make db-reset` (down -v → up → migrate → seed)
- Seed: [`data/progress-import.v1.json`](../../../../data/progress-import.v1.json) — 2 users, 10 food_events, 5 insulin_events
- [`scripts/db/seed_from_progress.py`](../../../../scripts/db/seed_from_progress.py) — async, pydantic, `ON CONFLICT DO NOTHING` по `id`
- [`scripts/db/db_inspect.py`](../../../../scripts/db/db_inspect.py) — counts + sample без ПДн
- Makefile: 7 целей `db-*` (`db-up`, `db-down`, `db-reset`, `db-migrate`, `db-seed`, `db-shell`, `db-inspect`)
- Docs: [database-access.md](../../../../tech/database-access.md), [README.md](../../../../README.md), [backend/README.md](../../../../backend/README.md), [data/README.md](../../../../data/README.md), [tasklist-database.md](../../../tasklist-database.md) § инфраструктура
- План итерации: [plan.md](plan.md)
- Детали: [task-04 summary](tasks/task-04-db-infra-seed/summary.md)

| Артефакт | Путь |
|----------|------|
| Seed data | [data/progress-import.v1.json](../../../../data/progress-import.v1.json) |
| Seed script | [scripts/db/seed_from_progress.py](../../../../scripts/db/seed_from_progress.py) |
| Inspect | [scripts/db/db_inspect.py](../../../../scripts/db/db_inspect.py) |
| Make targets | [Makefile](../../../../Makefile) |
| Guide (seed) | [database-access.md](../../../../tech/database-access.md) |

## Ценность

- Локальная seeded БД за одну команду — onboarding и ручное E2E без ручного compose/migrate/insert
- Idempotent seed — безопасный повторный прогон в CI и при разработке
- `make db-inspect` — быстрая проверка данных без вывода ПДн
- Связка bootstrap (Backend iter 2) + операции (database iter 4) задокументирована в tasklist

## Решения

| Тема | Решение |
|------|---------|
| Seed idempotency | фиксированные UUID в JSON + `INSERT ... ON CONFLICT (id) DO NOTHING` |
| Валидация import | pydantic-модели в seed-скрипте (без JSON Schema / jsonschema) |
| Inspect script | `db_inspect.py` — избежать shadowing stdlib `inspect` |
| Wait PG | loop `pg_isready` в `db-up` (не `docker compose wait`) |
| `progress_snapshots` | пустой массив в v1; seed таблиц — iter 5 |
| Env | новых переменных нет; `.env.example` в **корне** репо (не `backend/`) |
| Lint | `scripts/` добавлен в `make lint` / `make format` |

## Отклонения от плана

| План | Факт | Причина |
|------|------|---------|
| `scripts/db/inspect.py` | `scripts/db/db_inspect.py` | Shadowing stdlib `inspect` |
| `docker compose wait` | loop `pg_isready` | wait зависал бесконечно |
| JSON Schema | не создан | pydantic без новой зависимости |
| `docker-compose.yml` | без изменений | healthcheck уже был достаточен |

## Проблемы

| Проблема | Решение |
|----------|---------|
| `inspect.py` ломал import asyncio/sqlalchemy | переименован в `db_inspect.py` |
| `docker compose wait postgres` не завершался | заменён на `pg_isready` loop (max 15s) |

## DoD итерации

| Кто | Статус | Критерии |
|-----|--------|----------|
| Self-check (агент) | ✅ | `db-reset` + `db-inspect` green; seed idempotent; migrate на чистой БД; `backend-test` 30 passed; `lint` green |
| User-check | 📋 | чеклист в [task-04 summary](tasks/task-04-db-infra-seed/summary.md) |

## Make-команды

| Команда | Результат |
|---------|-----------|
| `make db-up` / `make db-down` | ✅ lifecycle PG |
| `make db-reset && make db-inspect` | ✅ users:2, food:10, insulin:5 |
| `make db-seed` (повторно) | ✅ +0 rows |
| `make backend-migrate` / `make db-migrate` | ✅ revision 001 |
| `make backend-test` | ✅ 30 passed |
| `make lint` | ✅ |

## Следующий шаг

[Итерация 5 — ORM, репозитории, backend](../iteration-5-orm-repos/plan.md): миграция `002_*`, модели, repos, E2E с seed.
