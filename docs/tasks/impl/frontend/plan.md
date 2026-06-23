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
| 4 Лидерboard | 04 | ✅ Done | [plan](iteration-4-leaderboard/plan.md) · [summary](iteration-4-leaderboard/summary.md) |
| 5 Чат с ассистентом | 05 | ✅ Done | [plan](iteration-5-assistant-chat/plan.md) · [summary](iteration-5-assistant-chat/summary.md) |
| 6 Чат в основной области | 06 | ✅ Done | [plan](iteration-6-main-chat/plan.md) · [summary](iteration-6-main-chat/summary.md) |
| 7 Ревью качества | 07 | ✅ Done | [plan](iteration-7-quality-review/plan.md) · [summary](iteration-7-quality-review/summary.md) |
| 8 Голосовой режим | 08 | ✅ Done | [plan](iteration-8-voice-chat/plan.md) · [summary](iteration-8-voice-chat/summary.md) |
| 9 Text-to-SQL | 09 | ✅ Done | [plan](iteration-9-text-to-sql/plan.md) · [summary](iteration-9-text-to-sql/summary.md) |

**10 / 10** итераций завершено. Область frontend закрыта ✅.

## Артефакты области

| Путь | Статус |
|------|--------|
| `docs/spec/frontend-requirements.md` | ✅ iter 0 |
| `docs/spec/frontend-design-system.md` | ✅ iter 0 |
| `docs/api/frontend-contract.md` | ✅ iter 0–5 (assistant BFF) |
| `docs/api/api-contract.md` | ✅ iter 0–4 (web impl) |
| `docs/api/api-contract-review.md` | ✅ iter 0 |
| `web/` Next.js app | ✅ iter 2–9 (`/dashboard`, `/leaderboard`, `/chat`, FAB, voice, data query) |

Сводка: [summary.md](summary.md) · … · iter 8: [iteration-8-voice-chat/summary.md](iteration-8-voice-chat/summary.md) · iter 9: [iteration-9-text-to-sql/summary.md](iteration-9-text-to-sql/summary.md)
