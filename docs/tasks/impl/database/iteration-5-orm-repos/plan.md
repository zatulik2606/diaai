# Итерация database 5: ORM, репозитории, backend

Опирается на [tasklist-database.md](../../../tasklist-database.md) · [impl/database/plan.md](../plan.md) · [iteration-4 summary](../iteration-4-db-infra-seed/summary.md)

**Статус итерации:** ✅ Done · [summary](summary.md)

## Контекст

- **Tasklist:** итерация 5, задача 05
- **Зависимости (✅):** schema-er draft DDL, ADR-003, `make db-*` + seed (iter 4)
- **Разблокирует:** backend analytics 09–12

## Цель

Реализовать целевую схему (9 таблиц) в коде: миграция `002_*`, models, repos, wiring в services.

## Задачи

| # | Задача | Статус | Документы |
|---|--------|--------|-----------|
| 05 | ORM, репозитории, backend | ✅ Done | [plan](tasks/task-05-orm-repos/plan.md) · [summary](tasks/task-05-orm-repos/summary.md) |

## Шаги

1. `002_full_data_layer.py` по [schema-er §6](../../../../spec/schema-er.md#6-appendix-draft-migration-002)
2. Models + register
3. Repositories
4. Services: photo_analysis persist + progress/consultation stubs
5. Seed v2 + db_inspect
6. Tests + docs

## DoD

`make db-reset && make test` green; 9 таблиц; photo → `photo_analyses`.

## Вне scope

Analytics REST (backend 09–12), LLM parsing structured fields, web/bot changes.

## Следующий шаг

Backend iter 4 analytics API на готовых таблицах.
