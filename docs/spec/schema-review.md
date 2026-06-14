# PostgreSQL design review

Схема: [schema-er.md](schema-er.md) · Skill: [postgresql-table-design](../../.agents/skills/postgresql-table-design/SKILL.md)

Дата review: database iter 2 (task 02).

---

## Итог

| Статус | Количество |
|--------|------------|
| Pass | 16 |
| Warn | 4 |
| Fix | 0 |

Схема готова к impl миграции `002_*` в database iter 5.

---

## Checklist

| # | Тема | Статус | Комментарий |
|---|------|--------|-------------|
| 1 | PRIMARY KEY на reference tables | **Pass** | UUID PK на всех 9 таблицах |
| 2 | PK UUID vs BIGINT IDENTITY | **Warn** | Skill предпочитает BIGINT IDENTITY; оставляем UUID для совместимости с `001` и opaque IDs в API |
| 3 | NOT NULL семантика | **Pass** | Обязательные поля NOT NULL; nullable FK (`request_id`, `food_event_id`) документированы |
| 4 | TIMESTAMPTZ для event time | **Pass** | `recorded_at`, `injected_at`, `scheduled_at`, `created_at`, `started_at` |
| 5 | NUMERIC для xe/bje/dose | **Pass** | `NUMERIC(10,2)`; confidence `NUMERIC(3,2)` |
| 6 | TEXT вмест of VARCHAR/CHAR | **Pass** | Все строки — TEXT + CHECK |
| 7 | TEXT + CHECK вместо PG ENUM | **Pass** | role, status, period, trend — evolving values |
| 8 | FK columns indexed | **Pass** | См. таблицу FK ниже |
| 9 | ON DELETE на FK | **Pass** | RESTRICT на user/parent; SET NULL на optional child FK |
| 10 | Partial indexes | **Pass** | nullable FK, partial UNIQUE telegram_id |
| 11 | Composite indexes для access paths | **Pass** | `(user_id, recorded_at DESC)`, `(user_id, period, period_start DESC)` |
| 12 | JSONB для semi-structured | **Pass** | `dialog_requests.media` — as-is |
| 13 | telegram_id UNIQUE + nullable | **Pass** | Partial UNIQUE `WHERE telegram_id IS NOT NULL` |
| 14 | UNIQUE на progress_snapshots | **Pass** | `(user_id, period, period_start)` — идемпотентный persist |
| 15 | consultations diabetic != doctor | **Pass** | CHECK constraint |
| 16 | snake_case identifiers | **Pass** | Все имена таблиц/колонок |
| 17 | Avoid TIMESTAMP without TZ | **Pass** | Нет `timestamp without time zone` |
| 18 | period_start <= period_end | **Pass** | CHECK на `progress_snapshots` |
| 19 | Сводка FK + ON DELETE | **Pass** | [schema-er.md §3.10](schema-er.md#310-сводка-fk-on-delete-и-ограничения-целостности) |
| 20 | FK ON DELETE на таблицах `001` | **Warn** | `food_events.request_id`, `insulin_events.food_event_id` — в `001` NO ACTION; целевое SET NULL — alter в iter 5 |
| 21 | `dialog_requests.media` JSON vs JSONB | **Warn** | `001` — тип JSON; миграция на JSONB опциональна в `002` |

---

## FK → индекс (обязательная проверка)

| Таблица | FK колонка | Индекс |
|---------|------------|--------|
| `dialogs` | `user_id` | `ix_dialogs_user_id` ✅ |
| `dialog_requests` | `dialog_id`, `user_id` | `ix_dialog_requests_dialog_id`, `ix_dialog_requests_user_id` ✅ |
| `food_events` | `user_id`, `request_id` | `ix_food_events_user_id`, `ix_food_events_request_id` ✅ |
| `insulin_events` | `user_id`, `food_event_id` | `ix_insulin_events_user_id`, `ix_insulin_events_food_event_id` ✅ |
| `photo_analyses` | `user_id`, `request_id`, `food_event_id` | все три ✅ |
| `progress_snapshots` | `user_id` | `ix_progress_snapshots_user_period` ✅ |
| `recommendations` | `user_id`, `request_id` | оба ✅ |
| `consultations` | `diabetic_id`, `doctor_id` | оба + composite ✅ |

---

## Warn (принятые отклонения)

| Тема | Решение | Defer |
|------|---------|-------|
| UUID PK вместо BIGINT IDENTITY | Сохранить UUID — единообразие с `001`, API opaque IDs | iter 5 при impl — без смены типа |
| `dialog_requests.media` JSON vs нормализация | Raw metadata в JSON/JSONB; структурированный анализ — `photo_analyses` | object storage URL — backlog |
| FK ON DELETE на `001`-таблицах | Целевое SET NULL для optional FK; alter constraint в iter 5 | iter 5 migration |
| JSON → JSONB для `media` | Опционально в `002` для GIN-индексации | backlog |

---

## Fix

_(нет незакрытых Fix)_

---

## Согласование

- Согласовано с [ADR-001](../adr/adr-001-database.md) — PostgreSQL, целевая схема § «Физическая схема» ✅
- [api-contract.md](../api/api-contract.md) v1 — persisted fields без изменений ✅
- [data-model.md](../data-model.md#postgresql-design-review) — домен + PG маппинг ✅
- [001_initial_schema.py](../../alembic/versions/001_initial_schema.py) — diff явный в [schema-er.md §5](schema-er.md#5-diff-mvp-001--целевая-схема) ✅
