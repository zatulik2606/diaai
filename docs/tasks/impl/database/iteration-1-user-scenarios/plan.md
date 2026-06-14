# Итерация database 1: Сценарии и требования к данным

Опирается на [tasklist-database.md](../../../tasklist-database.md) · [impl/database/plan.md](../plan.md)

## Цель

Зафиксировать продуктовые сценарии пациента с диабетом и доктора и вывести минимальный набор сущностей, полей и связей для web и аналитики — без DDL.

## Ценность

- Единый продуктовый язык для web (iter 5) и analytics API (iter 4)
- Явный gap-list относительно `001_initial_schema`
- Вход для итерации 2 (ER и physical schema)

## Задачи

| # | Задача | Статус | Документы |
|---|--------|--------|-----------|
| 01 | Сценарии и требования к данным | ✅ Done | [plan](tasks/task-01-user-scenarios/plan.md) · [summary](tasks/task-01-user-scenarios/summary.md) |

## Артефакты

- `docs/spec/user-scenarios.md`
- `docs/spec/data-requirements.md`
- `docs/spec/README.md`
- обновления: `docs/data-model.md`, `docs/vision.md`

## Definition of Done

**Self-check:** 7+4 сценария; read/write матрица; gap-list; согласовано с api-contract v1.

**User-check:** понятны экраны пациента с диабетом/доктора; видно какие таблицы понадобятся; покрыты plan iter 4–5.

## Вне scope

DDL, ER, миграции, код — итерации 2–5.
