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
| 04 | API-тесты сценариев | ✅ Done | [plan](tasks/task-04-api-tests/plan.md) · [summary](tasks/task-04-api-tests/summary.md) |
| 05 | Endpoint'ы и серверная логика | 🚧 Next | [plan](tasks/task-05-api-impl/plan.md) |

## Критерии завершения итерации

- [x] `make backend-run` → `/health` 200; `/docs` v1 paths (task-03)
- [x] contract tests: 17 тестов, auth/422/400/501 (task-04)
- [ ] `make backend-test` зелёный с impl 200/201 (task-05)
- [ ] endpoint'ы соответствуют [docs/api/](../../../../api/)
- [ ] события питания и инсулина в PostgreSQL; данные переживают перезапуск
- [ ] **без** миграции бота (→ iteration-3, task-07)

## Текущий статус

🚧 In Progress — task-05 api-impl

## Следующая итерация

[iteration-3-delivery](../iteration-3-delivery/plan.md) — задачи 06–08: docs, bot refactor, quality.

## Документы

- 📝 [Summary](summary.md) — task-03 ✅, task-04 ✅; итерация открыта до task-05
