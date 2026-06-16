# Task 04: Лидерборд

Итерация: [iteration-4-leaderboard](../../plan.md) · [tasklist-frontend.md](../../../../../tasklist-frontend.md)

**Статус:** ✅ Done · [summary](summary.md)

---

## Цель

Реализовать `/leaderboard` для doctor и diabetic: backend DTO с продуктами и медалями топ-5 БЖЕ + UI (таблица / scatter / legend).

## Состав работ

### Backend

- [x] `LeaderboardProduct` + `BjeMedal` в `backend/schemas/web.py`
- [x] `FoodEventRepository.products_by_user()` — group by `description`, sum xe/bje
- [x] `WebLeaderboardService`: cohort top-5 BJE → `bje_medal`; убрать `medal` за rank
- [x] `require_leaderboard_viewer` — `doctor_telegram_id` или `patient_telegram_id`
- [x] `test_leaderboard_products`, `test_leaderboard_patient_access`

### Frontend

- [x] `web/lib/types/leaderboard.ts`, `leaderboard-utils.ts`
- [x] `fetchLeaderboard(telegramId, role)` в `backend-client.ts`
- [x] `components/leaderboard/*` — table, chips, scatter, tabs, `bje-top5-legend`
- [x] Emoji medals 🥇–5️⃣ на product chips
- [x] Подсветка строки пациента + «ваше место: #N»
- [x] `middleware` + `app-sidebar` — leaderboard для diabetic
- [x] `app/(app)/leaderboard/` — page + loading + error

## Затронутые файлы

| Область | Файлы |
|---------|-------|
| Backend | `deps.py`, `leaderboard.py`, `schemas/web.py`, `food_event.py`, `web_leaderboard_service.py`, `web_utils.py`, `test_web_api.py` |
| Frontend | `lib/*`, `components/leaderboard/*`, `components/ui/{tabs,progress,badge,tooltip}.tsx`, `middleware.ts`, `app-sidebar.tsx`, `app/(app)/leaderboard/*` |
| Docs | `frontend-contract.md`, `frontend-requirements.md`, `api-contract.md`, `openapi.yaml`, summaries |

## Проверка

```bash
make backend-test
make web-build
# doctor
curl -s "http://127.0.0.1:8000/api/v1/web/leaderboard?doctor_telegram_id=162684825" \
  -H "Authorization: Bearer 12345" | jq '.table[0].products[0]'
# patient
curl -s "http://127.0.0.1:8000/api/v1/web/leaderboard?patient_telegram_id=900000001" \
  -H "Authorization: Bearer 12345" | jq '.table | length'
# web: ivan_p / doctor_ivanov → /leaderboard
```

## Definition of Done

- [x] API `products[]` + `bje_medal` для топ-5 БЖЕ когорты
- [x] Patient и doctor доступ к leaderboard
- [x] UI: top-5 legend, emoji medals, highlight своей строки
- [x] Legacy `metrics`/`medal` удалены
