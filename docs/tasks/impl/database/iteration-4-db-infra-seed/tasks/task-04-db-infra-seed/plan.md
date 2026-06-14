# Task 04: Инфраструктура БД, seed, команды

Опирается на [iteration-4/plan.md](../../plan.md) · [tasklist-database.md](../../../../../tasklist-database.md)

## Цель

One-command локальное окружение PostgreSQL + seed + inspect.

## Что делаем

1. `data/progress-import.v1.json` — users, food/insulin events; `progress_snapshots: []`
2. `scripts/db/seed_from_progress.py` — async, idempotent upsert по `id`
3. `scripts/db/db_inspect.py` — counts, sample без ПДн (`--verbose` опционально)
4. Makefile: `db-up`, `db-down`, `db-reset`, `db-migrate`, `db-seed`, `db-shell`, `db-inspect`
5. Docs: `database-access.md`, `README.md`, `backend/README.md`, `data/README.md`, `tasklist-database.md` § инфраструктура

## Затронутые файлы

| Файл | Действие |
|------|----------|
| `data/progress-import.v1.json` | создать |
| `data/README.md` | создать |
| `scripts/db/seed_from_progress.py` | создать |
| `scripts/db/db_inspect.py` | создать |
| `Makefile` | цели `db-*` |
| `docs/tech/database-access.md` | секция seed |
| `README.md`, `backend/README.md` | quick start |
| `.env.example` | комментарий `DATABASE_URL` |

## DoD

**Self-check:** `make db-reset && make db-inspect`; повторный `make db-seed` — counts unchanged; `make backend-test`; `make lint`.

**User-check:** все 7 `db-*` в README; `make db-shell` работает.

## Проверка руками

```bash
# Запуск / остановка
make db-up
make db-down

# Миграции
make db-up && make db-migrate
uv run alembic current   # 001 (head)

# Seed + inspect
make db-reset
make db-inspect          # users:2, food_events:10, insulin_events:5
make db-seed             # +0 rows
make db-shell            # SELECT count(*) FROM food_events;
```

## Make-команды

`make db-reset`, `make db-inspect`, `make db-seed`, `make backend-test`
