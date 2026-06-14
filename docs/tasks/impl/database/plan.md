# Database: сводный план области

Опирается на [tasklist-database.md](../../tasklist-database.md) · [plan.md](../../../plan.md) · [data-model.md](../../../data-model.md)

## Цель области

Довести PostgreSQL от MVP-схемы (`001_initial_schema`) до полноценного слоя данных для аналитики (plan iter 4) и web (plan iter 5).

## Прогресс

| Итерация | Задачи | Статус | Документы |
|----------|--------|--------|-----------|
| 1 Сценарии и требования | 01 | ✅ Done | [plan](iteration-1-user-scenarios/plan.md) · [summary](iteration-1-user-scenarios/summary.md) |
| 2 Проектирование схемы | 02 | ✅ Done | [plan](iteration-2-schema-design/plan.md) · [summary](iteration-2-schema-design/summary.md) |
| 3 ADR и практика | 03 | ✅ Done | [plan](iteration-3-data-access-adr/plan.md) · [summary](iteration-3-data-access-adr/summary.md) |
| 4 Инфра и seed | 04 | ✅ Done | [plan](iteration-4-db-infra-seed/plan.md) · [summary](iteration-4-db-infra-seed/summary.md) |
| 5 ORM и backend | 05 | 📋 Next | [plan](iteration-5-orm-repos/plan.md) |

**4 / 5** итераций завершено → итерация 5 — next.

## Зависимости

- Backend MVP ✅ — [iteration-2-core summary](../backend/iteration-2-core/summary.md)
- Целевая схема ✅ — [schema-er.md](../../../spec/schema-er.md) (iter 2)
- Data access ADR ✅ — [adr-003-data-access-layer.md](../../../adr/adr-003-data-access-layer.md) (iter 3)
- Seed + `make db-*` ✅ — [iteration-4 summary](iteration-4-db-infra-seed/summary.md) (iter 4)
- Аналитика API — [tasklist-backend](../../tasklist-backend.md) 09–12 (после iter 5)
- Web — [tasklist-web.md](../../tasklist-web.md)

## Артефакты области

| Путь | Назначение | Статус |
|------|------------|--------|
| `docs/spec/` | сценарии, schema-er, schema-review | iter 1–2 ✅ |
| `docs/data-model.md` | домен + целевая SQL | ✅ |
| `docs/adr/adr-003-data-access-layer.md` | data access | iter 3 ✅ |
| `docs/tech/database-access.md` | практический guide | iter 3–4 ✅ |
| `scripts/db/*`, `make db-*` | seed, inspect | iter 4 ✅ |
| `alembic/versions/002_*` | целевая схема в коде | iter 5 |

## Следующий шаг

[Итерация 5 — ORM, репозитории, backend](iteration-5-orm-repos/plan.md): миграция `002_*`, модели, repos, E2E с seed.

Сводка: [summary.md](summary.md)
