# Backend: сводка области

> **Статус:** delivery 01–08 ✅ · **iter 4 ✅** (tasks 09–12)

## Прогресс

| Итерация | Задачи | Статус | Документы |
|----------|--------|--------|-----------|
| 1 Основание | 01–02 | ✅ Done | [plan](iteration-1-foundation/plan.md) · [summary](iteration-1-foundation/summary.md) |
| 2 Сборка ядра | 03–05 | ✅ Done | [plan](iteration-2-core/plan.md) · [summary](iteration-2-core/summary.md) |
| 3 Поставка | 06–08 | ✅ Done | [plan](iteration-3-delivery/plan.md) · [summary](iteration-3-delivery/summary.md) |
| 4 Аналитика | 09–12 | ✅ Done | [plan](iteration-4-analytics/plan.md) · [summary](iteration-4-analytics/summary.md) |

## Текущее состояние

- [`backend/`](../../../backend/) — FastAPI, PostgreSQL, OpenRouter, web API
- [`src/diaai/`](../../../src/diaai/) — bot → backend API ✅
- [`web/`](../../../web/) — клиент web API ✅ (область frontend)
- `make test` — **109** passed (92 backend + 17 bot)
- Analytics REST `/api/v1/analytics/*` — contract ✅ + impl ✅ (tasks 09–12)

Онбординг: [backend/README.md](../../../backend/README.md) · архитектура: [architecture.md](../../../architecture.md)

## Следующий этап

Consultations UI (D5/D6) · production deploy — см. [plan.md](../../../plan.md)

## Документы

- [plan.md](plan.md) — сводный план области
- [tasklist-backend.md](../../tasklist-backend.md)
- [api-contract.md](../../../api/api-contract.md) — REST API v1
