# Task 02: Проектирование схемы данных

Опирается на [iteration-2/plan.md](../../plan.md) · [tasklist-database.md](../../../../../tasklist-database.md)

## Цель

Логическая + физическая модель PostgreSQL, ER-диаграмма, review по `postgresql-table-design`, черновик DDL для `002_*`.

## Что делаем

### 1. Логическая модель

- Сущности из [data-requirements.md](../../../../../../spec/data-requirements.md)
- Cardinality, nullable FK, каскады *(soft: RESTRICT на delete user)*
- Решения open questions — см. [iteration-2/plan.md](../../plan.md#решения-для-проектирования-из-open-questions-iter-1)

### 2. Физическая модель (`docs/spec/schema-er.md`)

| Таблица | Ключевые колонки | Индексы |
|---------|------------------|---------|
| `users` | id UUID PK, telegram_id BIGINT UNIQUE nullable, role, display_name, email, is_active, created_at TIMESTAMPTZ | ix_users_role |
| `photo_analyses` | id, user_id, request_id, food_event_id nullable, xe/bje/bju NUMERIC, confidence, object_type, created_at | ix_photo_analyses_user_id, request_id |
| `progress_snapshots` | id, user_id, period enum, period_start/end DATE, sums, trend, comment, created_at | ix_progress_snapshots_user_period |
| `recommendations` | id, user_id, request_id nullable, text, type, created_at | ix_recommendations_user_id |
| `consultations` | id, diabetic_id, doctor_id, format, scheduled_at, status, doctor_comment | ix_consultations_diabetic, doctor |

Существующие `dialogs`, `dialog_requests`, `food_events`, `insulin_events` — описать as-is + новые FK где нужно (`photo_analyses.food_event_id`).

### 3. Design review (`docs/spec/schema-review.md`)

Checklist [postgresql-table-design](../../../../../.agents/skills/postgresql-table-design/SKILL.md):

- PK UUID (opaque IDs, согласовано с MVP)
- FK columns indexed manually
- `TIMESTAMPTZ` для всех event times
- `NUMERIC` для xe/bje/dose
- NOT NULL где semantically required
- Таблица pass / warn / fix

### 4. Diff MVP → целевая

Секция в `schema-er.md` и обновление [data-model.md](../../../../../../data-model.md#sql-схема-mvp-task-05) → «SQL-схема целевая (iter 2)».

### 5. Черновик DDL

Appendix в `schema-er.md` или отдельная секция «Draft migration 002» — **не коммитить** `alembic/versions/002_*.py` в этой задаче.

## Затронутые файлы

| Файл | Действие |
|------|----------|
| `docs/spec/schema-er.md` | создать |
| `docs/spec/schema-review.md` | создать |
| `docs/spec/README.md` | добавить schema-* |
| `docs/data-model.md` | целевая схема, обновить gap → resolved |
| `docs/api/api-contract.md` | только если меняются persisted fields *(не ожидается)* |

## Согласование

- [api-contract.md](../../../../../../api/api-contract.md) v1 — без новых endpoint'ов
- [backend iter 4 plan](../../../backend/iteration-4-analytics/plan.md) — поля ProgressSnapshot, Recommendation
- Имена колонок API: `xe`, `bje`, `telegram_id` — [data-model.md](../../../../../../data-model.md#api-поля-v1)

## DoD

**Self-check:** ER + review + diff; FK indexes; open questions closed in schema-er.

**User-check:** schema-er читается; data-model согласован; review без orphan Fix.

## Skills

Обязательно: `postgresql-table-design` → `schema-review.md`.

## Make-команды

Не требуются.
