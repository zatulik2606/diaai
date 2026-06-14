# Итерация database 4: Summary

> **Статус:** ✅ Done

План: [plan.md](plan.md)

## Сделано

### Task-04: Инфраструктура, seed, команды ✅

- One-command окружение: `make db-reset` (down -v → up → migrate → seed)
- Seed: [`data/progress-import.v1.json`](../../../../data/progress-import.v1.json) + [`scripts/db/seed_from_progress.py`](../../../../scripts/db/seed_from_progress.py)
- Inspect: [`scripts/db/db_inspect.py`](../../../../scripts/db/db_inspect.py)
- Документация: [database-access.md](../../../../tech/database-access.md) § Локальное окружение и seed

| Артефакт | Путь |
|----------|------|
| Seed data | [data/progress-import.v1.json](../../../../data/progress-import.v1.json) |
| Seed script | [scripts/db/seed_from_progress.py](../../../../scripts/db/seed_from_progress.py) |
| Inspect | [scripts/db/db_inspect.py](../../../../scripts/db/db_inspect.py) |
| Make targets | [Makefile](../../../../Makefile) |

Детали: [task-04 summary](tasks/task-04-db-infra-seed/summary.md)

## Verification

| Команда | Результат |
|---------|-----------|
| `make db-reset && make db-inspect` | ✅ |
| повторный `make db-seed` | ✅ idempotent (+0) |
| `make backend-test` | ✅ 30 passed |
| `make lint` | ✅ |

## Следующий шаг

[Итерация 5 — ORM, репозитории, backend](../iteration-5-orm-repos/plan.md): миграция `002_*`, модели, repos.
