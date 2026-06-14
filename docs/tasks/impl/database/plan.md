# Database: сводный план области

Опирается на [tasklist-database.md](../../tasklist-database.md) · [plan.md](../../../plan.md) · [data-model.md](../../../data-model.md)

## Цель области

Довести PostgreSQL от MVP-схемы (`001_initial_schema`) до полноценного слоя данных для аналитики и web.

## Прогресс

| Итерация | Задачи | Статус | Документы |
|----------|--------|--------|-----------|
| 1 Сценарии и требования | 01 | ✅ Done | [plan](iteration-1-user-scenarios/plan.md) · [summary](iteration-1-user-scenarios/summary.md) |
| 2 Проектирование схемы | 02 | ✅ Done | [plan](iteration-2-schema-design/plan.md) · [summary](iteration-2-schema-design/summary.md) |
| 3 ADR и практика | 03 | ✅ Done | [plan](iteration-3-data-access-adr/plan.md) · [summary](iteration-3-data-access-adr/summary.md) |
| 4 Инфра и seed | 04 | ✅ Done | [plan](iteration-4-db-infra-seed/plan.md) · [summary](iteration-4-db-infra-seed/summary.md) |
| 5 ORM и backend | 05 | ✅ Done | [plan](iteration-5-orm-repos/plan.md) · [summary](iteration-5-orm-repos/summary.md) |

**5 / 5** итераций завершено.

## Артефакты области

| Путь | Статус |
|------|--------|
| `docs/spec/` | ✅ |
| `docs/adr/adr-003-data-access-layer.md` | ✅ |
| `scripts/db/*`, `make db-*` | ✅ |
| `alembic/versions/002_full_data_layer.py` | ✅ |

Сводка: [summary.md](summary.md)
