# Task 04: Лидерборд — Summary

> **Статус:** ✅ Done

Итерация: [iteration-4-leaderboard](../../plan.md) · [plan](plan.md)

---

## Сделано

### Backend

- `BjeMedal`, `LeaderboardProduct` в `backend/schemas/web.py`
- `FoodEventRepository.products_by_user()` — group by `trim(description)`, top-20 по xe
- `bje_medal_for_rank()` + cohort top-5 BJE в `WebLeaderboardService`
- `require_leaderboard_viewer` — doctor или patient query param
- Удалены `metrics` / `medal` из response
- `test_leaderboard_products`, `test_leaderboard_patient_access`

### Frontend

- `leaderboard.ts`, `leaderboard-utils.ts`, `fetchLeaderboard(id, role)`
- shadcn: `tabs`, `progress`, `badge`, `tooltip`
- `bje-top5-legend.tsx` — блок топ-5 БЖЕ когорты
- `product-chip.tsx` — emoji продуктов + 🥇–5️⃣
- `leaderboard-table.tsx` — highlight `currentUserId`, метка «(вы)»
- `leaderboard-scatter.tsx`, `leaderboard-tabs.tsx`
- `middleware` — diabetic может открыть `/leaderboard`
- `app-sidebar` — Leaderboard для doctor + diabetic
- `app/(app)/leaderboard/` — RSC + loading + error

### Docs

- `frontend-contract.md`, `frontend-requirements.md` — patient auth + роли
- `openapi.yaml`, `api-contract.md` — без legacy leaderboard fields

## Отклонения от плана

| Отклонение | Причина |
|------------|---------|
| Лидерборд для пациента | запрос пользователя |
| Top-5 legend + emoji medals | UX: медали не были видны |
| Period/metric selectors — 30d / xe | MVP backlog |

## Проверки

| Команда | Результат |
|---------|-----------|
| `make backend-test` | ✅ 53 passed |
| `make web-lint && make web-build` | ✅ |
| API doctor + patient | ✅ |
| UI doctor_ivanov / ivan_p | ✅ |

## Skills review

| Skill | Verdict |
|-------|---------|
| shadcn | ✅ Tabs, Table, Progress, Badge, Tooltip |
| vercel-react-best-practices | ✅ RSC fetch, client chart/tabs only |
| nextjs-app-router-patterns | ✅ loading/error, role-based fetch |
