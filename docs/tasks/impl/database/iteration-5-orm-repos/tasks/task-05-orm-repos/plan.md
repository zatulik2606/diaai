# Task 05: ORM, репозитории, backend

Опирается на [iteration-5/plan.md](../../plan.md) · [tasklist-database.md](../../../../../tasklist-database.md) § Итерация 5

**Статус:** ✅ Done · [summary](summary.md)

## Цель

Миграция `002_*`, models/repos, wiring services — полный data layer в PostgreSQL (9 таблиц).

## Затронутые файлы

| Область | Файлы |
|---------|--------|
| Миграция | `alembic/versions/002_full_data_layer.py` |
| Models | `backend/models/photo_analysis.py`, `progress_snapshot.py`, `recommendation.py`, `consultation.py`; `user.py`; `__init__.py`; `alembic/env.py` |
| Repos | `backend/repositories/photo_analysis.py`, `progress_snapshot.py`, `recommendation.py`, `consultation.py`; `user.py` |
| Services | `backend/services/assistant_service.py`, `progress_service.py`, `consultation_service.py` |
| Seed | `data/progress-import.v1.json`, `scripts/db/seed_from_progress.py`, `scripts/db/db_inspect.py` |
| Tests | `backend/tests/test_migrations.py`, `test_repositories_extended.py`, `test_assistant.py`, `conftest.py` |
| Docs | `docs/data-model.md`, `backend/README.md`, `docs/tech/database-access.md`, `data/README.md` |

## Шаги

1. **`002_full_data_layer.py`** — DDL по [schema-er §6](../../../../../../spec/schema-er.md#6-appendix-draft-migration-002)
2. **Models** — 4 новых + расширение User; register в `__init__.py` и `env.py`
3. **Repositories** — CRUD/list MVP для новых таблиц; `UserRepository.create_doctor`
4. **Services** — `assistant_service` → `photo_analyses` на photo/mixed; stubs `progress_service`, `consultation_service`
5. **Seed v2** — snapshots, consultations; `db_inspect` — 9 таблиц
6. **Tests** — metadata smoke, extended repos, photo persist assertion
7. **Docs + tasklist** — область 5/5

## Архитектура

```
HTTP handler → Service(session) → Repository(session) → get_db → PostgreSQL
```

Photo flow: `POST /assistant/messages` (photo|mixed) → `AssistantService` → `PhotoAnalysisRepository.create`.

Structured поля `photo_analyses` (`xe`, `bje`, …) — null на MVP; парсинг LLM → backend task 11.

## DoD

```bash
make db-reset && make db-inspect   # progress_snapshots:2, consultations:1
make test                          # green
make lint                          # green
uv run alembic downgrade -1 && uv run alembic upgrade head
```

## Вне scope

Analytics REST (backend 09–12), LLM parsing structured fields, web/bot changes, JSON Schema seed v2.

## Make-команды

`make db-reset`, `make backend-test`, `make test`, `make lint`, `uv run alembic downgrade -1`
