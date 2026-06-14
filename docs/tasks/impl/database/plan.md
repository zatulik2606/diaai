# Database: сводный план области

Опирается на [tasklist-database.md](../../tasklist-database.md) · [plan.md](../../../plan.md) · [data-model.md](../../../data-model.md)

## Цель области

Довести PostgreSQL от MVP-схемы (`001_initial_schema`) до полноценного слоя данных для аналитики (plan iter 4) и web (plan iter 5).

## Прогресс

| Итерация | Задачи | Статус | Документы |
|----------|--------|--------|-----------|
| 1 Сценарии и требования | 01 | ✅ Done | [plan](iteration-1-user-scenarios/plan.md) · [summary](iteration-1-user-scenarios/summary.md) |
| 2 Проектирование схемы | 02 | 📋 Next | [plan](iteration-2-schema-design/plan.md) · [summary](iteration-2-schema-design/summary.md) |
| 3 ADR и практика | 03 | 📋 Planned | [plan](iteration-3-data-access-adr/plan.md) |
| 4 Инфра и seed | 04 | 📋 Planned | [plan](iteration-4-db-infra-seed/plan.md) |
| 5 ORM и backend | 05 | 📋 Planned | [plan](iteration-5-orm-repos/plan.md) |

**1 / 5** итераций завершено → итерация 2 — next.

## Зависимости

- Backend MVP ✅ — [iteration-2-core summary](../backend/iteration-2-core/summary.md)
- Аналитика API — [tasklist-backend](../../tasklist-backend.md) 09–12 (после итераций 2, 5)
- Web — [tasklist-web.md](../../tasklist-web.md) (после итерации 1 для сценариев)

## Артефакты области

| Путь | Назначение |
|------|------------|
| `docs/spec/` | продуктовые сценарии и требования к данным |
| `docs/data-model.md` | доменная и SQL-модель |
| `docs/adr/adr-003-*` | data access (итерация 3) |
| `alembic/versions/002_*` | целевая схема (итерация 5) |

## Следующий шаг

[Итерация 2 — проектирование схемы](iteration-2-schema-design/plan.md): ER, physical model, `postgresql-table-design` review.
