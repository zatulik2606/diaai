# Database: сводка области

> **Статус:** 🚧 In Progress (**4 / 5** итераций)

Сводный план: [plan.md](plan.md)

## Прогресс

| Итерация | Задачи | Статус | Документы |
|----------|--------|--------|-----------|
| 1 Сценарии и требования | 01 | ✅ Done | [plan](iteration-1-user-scenarios/plan.md) · [summary](iteration-1-user-scenarios/summary.md) |
| 2 Проектирование схемы | 02 | ✅ Done | [plan](iteration-2-schema-design/plan.md) · [summary](iteration-2-schema-design/summary.md) |
| 3 ADR и практика | 03 | ✅ Done | [plan](iteration-3-data-access-adr/plan.md) · [summary](iteration-3-data-access-adr/summary.md) |
| 4 Инфра и seed | 04 | ✅ Done | [plan](iteration-4-db-infra-seed/plan.md) · [summary](iteration-4-db-infra-seed/summary.md) |
| 5 ORM и backend | 05 | 📋 Next | [plan](iteration-5-orm-repos/plan.md) |

## Итерация 4 (закрыта)

| Критерий | Результат |
|----------|-----------|
| `make db-reset` | one-command PG + migrate 001 + seed |
| Seed data | users:2, food_events:10, insulin_events:5 |
| Seed idempotent | повторный `make db-seed` → +0 rows |
| Inspect | `make db-inspect` — counts без ПДн |
| Docs | `db-*` в README, backend README, database-access |
| Verification | `make backend-test` 30 passed · `make lint` green |

Self-check ✅ · User-check 📋 — [iteration-4 summary](iteration-4-db-infra-seed/summary.md)

## Итерации 1–3 (кратко)

- **1:** сценарии D1–D7, Doc1–Doc4 → [docs/spec/](../../../spec/)
- **2:** целевая схема 9 таблиц → [schema-er.md](../../../spec/schema-er.md)
- **3:** ADR-003 + [database-access.md](../../../tech/database-access.md)

## Следующий шаг

[Итерация 5 — ORM и backend](iteration-5-orm-repos/plan.md): `002_*`, models, repos.
