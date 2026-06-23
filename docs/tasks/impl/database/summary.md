# Database: сводка области

> **Статус:** ✅ Done (**5 / 5** итераций) · **актуально:** `make test` — **84**, миграции `001`–`003`

Сводный план: [plan.md](plan.md)

## Прогресс

| Итерация | Задачи | Статус | Summary |
|----------|--------|--------|---------|
| 1 Сценарии | 01 | ✅ | [summary](iteration-1-user-scenarios/summary.md) |
| 2 Схема | 02 | ✅ | [summary](iteration-2-schema-design/summary.md) |
| 3 ADR | 03 | ✅ | [summary](iteration-3-data-access-adr/summary.md) |
| 4 Инфра и seed | 04 | ✅ | [summary](iteration-4-db-infra-seed/summary.md) |
| 5 ORM и backend | 05 | ✅ | [summary](iteration-5-orm-repos/summary.md) |

## Итерация 5 (закрыта)

| Критерий | Результат |
|----------|-----------|
| `002_full_data_layer` | 9 таблиц |
| `make db-reset && make test` | 52 passed *(на момент закрытия iter 5; сейчас 84)* |
| photo → `photo_analyses` | ✅ |
| Persistence PG | ✅ после restart backend |
| Область database | **5/5** ✅ |

## Область завершена

Data layer готов для [backend analytics 09–12](../tasklist-backend.md) и [frontend](../tasklist-frontend.md).

**Ключевые артефакты:** миграции `001`–`003`, ORM/repos, `make db-*`, seed, [schema-er.md](../../spec/schema-er.md), ADR-003.
