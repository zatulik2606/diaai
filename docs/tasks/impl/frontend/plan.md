# Frontend: сводный план области

Опирается на [tasklist-frontend.md](../../tasklist-frontend.md) · [plan.md](../../../plan.md) · [vision.md](../../../vision.md)

## Цель области

Единый web-клиент (`web/`) для пациента с диабетом и доктора: Next.js App Router + shadcn/ui, тонкий клиент backend REST API.

## Прогресс

| Итерация | Задачи | Статус | Документы |
|----------|--------|--------|-----------|
| 0 UI-требования и API-контракты | 00 | ✅ Done | [plan](iteration-0-ui-contracts/plan.md) · [summary](iteration-0-ui-contracts/summary.md) |
| 1 API для frontend | 01 | ✅ Done | [plan](iteration-1-frontend-api/plan.md) · [summary](iteration-1-frontend-api/summary.md) |
| 2 Каркас frontend | 02 | ✅ Done | [plan](iteration-2-scaffold/plan.md) · [summary](iteration-2-scaffold/summary.md) |
| 3 | Панель пациента с диабетом | 03 | ✅ Done | [plan](iteration-3-patient-dashboard/plan.md) · [summary](iteration-3-patient-dashboard/summary.md) |
| 4 Лидерboard | 04 | 📋 Next | [plan](iteration-4-leaderboard/plan.md) · [summary](iteration-4-leaderboard/summary.md) · [task-04](iteration-4-leaderboard/tasks/task-04-leaderboard/plan.md) |
| 5 Чат с ассистентом | 05 | 📋 Planned | [plan](iteration-5-assistant-chat/plan.md) |
| 6 Чат в основной области | 06 | 📋 Planned | [plan](iteration-6-main-chat/plan.md) |
| 7 Ревью качества | 07 | 📋 Planned | [plan](iteration-7-quality-review/plan.md) |
| 8 Голосовой режим | 08 | 📋 Planned | [plan](iteration-8-voice-chat/plan.md) |
| 9 Text-to-SQL | 09 | 📋 Planned | [plan](iteration-9-text-to-sql/plan.md) |

**4 / 10** итераций завершено.

## Артефакты области

| Путь | Статус |
|------|--------|
| `docs/spec/frontend-requirements.md` | ✅ iter 0 |
| `docs/spec/frontend-design-system.md` | ✅ iter 0 |
| `docs/api/frontend-contract.md` | ✅ iter 0–3 (patient API); iter 4 target — leaderboard products |
| `docs/api/api-contract.md` | ✅ iter 0–1 (web impl) |
| `docs/api/api-contract-review.md` | ✅ iter 0 |
| `web/` Next.js app | ✅ iter 2–3; iter 4 — `/leaderboard` |

Сводка: [summary.md](summary.md) · iter 0: [iteration-0-ui-contracts/summary.md](iteration-0-ui-contracts/summary.md) · iter 1: [iteration-1-frontend-api/summary.md](iteration-1-frontend-api/summary.md) · iter 2: [iteration-2-scaffold/summary.md](iteration-2-scaffold/summary.md) · iter 3: [iteration-3-patient-dashboard/summary.md](iteration-3-patient-dashboard/summary.md) · **iter 4:** [iteration-4-leaderboard/plan.md](iteration-4-leaderboard/plan.md)
