# Backend: сводка области

> **Статус:** ✅ Done (задачи 01–08). **Следующее:** итерация 4 (аналитика, задачи 09–12).

## Прогресс

| Итерация | Задачи | Статус | Документы |
|----------|--------|--------|-----------|
| 1 Основание | 01–02 | ✅ Done | [plan](iteration-1-foundation/plan.md) · [summary](iteration-1-foundation/summary.md) |
| 2 Сборка ядра | 03–05 | ✅ Done | [plan](iteration-2-core/plan.md) · [summary](iteration-2-core/summary.md) |
| 3 Поставка | 06–08 | ✅ Done | [plan](iteration-3-delivery/plan.md) · [summary](iteration-3-delivery/summary.md) |
| 4 Аналитика | 09–12 | 📋 Planned | [plan](iteration-4-analytics/plan.md) · [summary](iteration-4-analytics/summary.md) |

## Итерация 3 (закрыта)

| Критерий | Статус |
|----------|--------|
| Docs + docker onboarding | ✅ task-06 |
| OpenAPI sync | ✅ task-06 |
| Bot → backend, история в PG | ✅ task-07 |
| Unit-тесты bot (`tests/`, 15) | ✅ task-07 |
| Logging / quality gate | ✅ task-08 |
| Post-audit: token, async LLM, image limits | ✅ task-08 |

Подробнее: [iteration-3-delivery/summary.md](iteration-3-delivery/summary.md)

## Текущее состояние

- [`backend/`](../../../backend/) — FastAPI, PostgreSQL, OpenRouter
- [`src/diaai/`](../../../src/diaai/) — bot → backend API ✅
- `make test` — **45** passed (30 backend + 15 bot)
- Онбординг: [backend/README.md](../../../backend/README.md)

## Следующий этап

[Итерация 4 — Аналитика](iteration-4-analytics/plan.md) · [plan.md](../../../plan.md#итерация-4--аналитика-и-динамика-состояния)

## Документы

- [plan.md](plan.md) — сводный план области
- [tasklist-backend.md](../../tasklist-backend.md)
- [api-contract.md](../../../api/api-contract.md) — REST API v1
