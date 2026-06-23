# Text-to-SQL: сценарии и golden questions

Опирается на [adr-004-text-to-sql.md](../adr/adr-004-text-to-sql.md) · [text-to-sql-architecture.md](text-to-sql-architecture.md) · [tasklist-frontend.md](../tasks/tasklist-frontend.md) iter 9

---

## Endpoint

`POST /api/v1/web/analytics/query`

| Параметр | Значение |
|----------|----------|
| Auth | Bearer `BACKEND_SERVICE_TOKEN` (BFF) |
| Query | `patient_telegram_id` (diabetic) или `doctor_telegram_id` (doctor) |
| Body | `{ "question": "..." }` |

---

## Golden questions (seed)

Seed users: `@ivan_p` (patient), `@doctor_ivanov` (doctor) — `make db-reset`.

| # | Роль | Вопрос | Ожидание |
|---|------|--------|----------|
| 1 | diabetic | «Сколько ХЕ я съел за последние 7 дней?» | `SUM(food_events.xe)` за 7 дней, scoped `user_id` пациента |
| 2 | doctor | «Сколько ХЕ за неделю у Иван П.?» | sum по `display_name` / patient |
| 3 | doctor | «Топ-3 пациента по ХЕ за 30 дней» | `GROUP BY user`, `ORDER BY sum DESC LIMIT 3` |

---

## Негативные кейсы

| Вопрос / SQL | Ожидание |
|--------------|----------|
| Пустой `question` | 422 |
| «Удали все события» (LLM → DELETE) | SqlGuard reject → 422 |
| `SELECT * FROM pg_catalog.pg_tables` | SqlGuard reject → 422 |
| Diabetic SQL без filter `user_id` | scope reject → 403 |

---

## UI

- Patient: блок «Вопрос по данным» на `/dashboard`
- Doctor: тот же блок на `/leaderboard`
- Ответ: текст + таблица; при `chart_hint=bar|line` — recharts

---

## Out of scope

- Write SQL, bot voice/text analytics, streaming
