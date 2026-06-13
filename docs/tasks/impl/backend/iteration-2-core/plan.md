# Итерация backend 2: Сборка ядра

Опирается на [plan.md](../../../../plan.md#итерация-2--backend-ядро-и-бд) · [tasklist-backend.md](../../../tasklist-backend.md) · [iteration-1-foundation](../iteration-1-foundation/plan.md)

## Цель

Реализовать backend по контрактам итерации 1: каркас, contract-тесты, API + PostgreSQL.

## Ценность

Работающее ядро: endpoint'ы A/B, данные в PostgreSQL, готовность к поставке (iteration-3).

## Предусловия

- ✅ [Итерация backend 1](../iteration-1-foundation/summary.md) — ADR-002, `docs/api/`

## Задачи

| # | Задача | Статус | Документы |
|---|--------|--------|-----------|
| 03 | Каркас backend + API-скелет | ✅ Done | [plan](tasks/task-03-scaffold/plan.md) · [summary](tasks/task-03-scaffold/summary.md) |
| 04 | API-тесты сценариев | 📋 Planned | [plan](tasks/task-04-api-tests/plan.md) |
| 05 | Endpoint'ы и серверная логика | 📋 Planned | [plan](tasks/task-05-api-impl/plan.md) |

## Критерии завершения итерации

- [x] `make backend-run` → `/health` 200; `/docs` v1 paths (task-03)
- [ ] `make backend-test` зелёный после task-05
- [ ] endpoint'ы соответствуют [docs/api/](../../../../api/)
- [ ] события питания и инсулина в PostgreSQL; данные переживают перезапуск
- [ ] **без** миграции бота (→ iteration-3, task-07)

## Текущий статус

🚧 In Progress — task-04 api-tests

## Следующая итерация

[iteration-3-delivery](../iteration-3-delivery/plan.md) — задачи 06–08: docs, bot refactor, quality.

## Документы

- 📝 [Summary](summary.md) — task-03 ✅; итерация открыта до task-05
