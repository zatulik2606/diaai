# Требования к данным

Опирается на [user-scenarios.md](user-scenarios.md) · [data-model.md](../data-model.md) · [api-contract.md](../api/api-contract.md)

Матрица read/write по сценариям. **API v1 bot** — без изменений. Web dashboard и chat — `/api/v1/web/*` ✅. Новые endpoint'ы D3–D4 (analytics REST) — [tasklist-backend](../tasks/tasklist-backend.md) 09–12; consultations UI — post-MVP ([tasklist-frontend](../tasks/tasklist-frontend.md) закрыт, D5/D6 вне scope).

---

## Пациент с диабетом

| ID | Экран / действие | Read (сущности · поля) | Write | Канал | MVP data |
|----|------------------|------------------------|-------|-------|----------|
| D1 | Лента дня | **FoodEvent** · description, xe, bje, proteins/fats/carbs, source, recorded_at; **InsulinEvent** · dose, injected_at, food_event_id, comment | FoodEvent, InsulinEvent *(опц. link request_id)* | both | yes |
| D2 | Чат / история | **Dialog** · channel, status; **Request** · type, content, reply, created_at; **User** · telegram_id | Dialog *(get-or-create)*, Request | both | yes |
| D3 | Dashboard периода | **ProgressSnapshot** · period, date range, sums xe/bje/insulin, trend, comment; агрегаты из FoodEvent, InsulinEvent | ProgressSnapshot *(persist или on-the-fly — iter 2)* | web, API | yes *(new table)* |
| D4 | Рекомендации | **Recommendation** · text, type, created_at; опц. связь Request / период | Recommendation | web, API | yes *(new table)* |
| D5 | Запись к доктору | **User** (doctor) · id, display_name; **Consultation** · slot, format, status | Consultation · scheduled | web | yes *(new table)* |
| D6 | История консультаций | **Consultation** · doctor, datetime, format, status, doctor_comment | Consultation · cancel *(post-MVP)* | web | yes |
| D7 | Деталь анализа фото | **PhotoAnalysis** · xe, bje, proteins/fats/carbs, confidence, comment; **Request** · media; опц. **FoodEvent** | PhotoAnalysis; опц. FoodEvent | both | yes *(new or media JSON — iter 2)* |

---

## Доктор

| ID | Экран / действие | Read | Write | Канал | MVP data |
|----|------------------|------|-------|-------|----------|
| Doc1 | Список пациентов | **User** · role=diabetic, display_name, last_activity; **Consultation** · upcoming filter | — | web | yes *(User fields)* |
| Doc2 | Dashboard пациента | **ProgressSnapshot**, FoodEvent, InsulinEvent по user_id пациента | — | web | yes |
| Doc3 | Карточка консультации | **Consultation** · diabetic, doctor, datetime, format, status | Consultation · status, doctor_comment | web | yes |
| Doc4 | Заметка | **Consultation** · doctor_comment | Consultation · doctor_comment | web | yes |

---

## Матрица сценарий → сущность

| Сущность | Сценарии |
|----------|----------|
| User | D1–D7, Doc1–Doc4 |
| Dialog | D2, D7 |
| Request (Запрос) | D2, D7, D1 *(optional request_id)* |
| FoodEvent | D1, D7 |
| InsulinEvent | D1 |
| PhotoAnalysis | D2, D7 |
| ProgressSnapshot | D3, Doc2 |
| Recommendation | D4 |
| Consultation | D5, D6, Doc1, Doc3, Doc4 |

---

## MVP data scope

### Must have — уже в PostgreSQL (`001_initial_schema`)

| Сущность | Таблица | Покрывает |
|----------|---------|-----------|
| User | `users` | D1–D2, частично Doc1 |
| Dialog | `dialogs` | D2 |
| Request | `dialog_requests` | D2, D7 *(reply + media JSON)* |
| FoodEvent | `food_events` | D1 |
| InsulinEvent | `insulin_events` | D1 |

### Добавлено в PostgreSQL (`002_full_data_layer` + `003_telegram_username`) ✅

| Сущность | Таблица | Сценарии | REST / UI |
|----------|---------|----------|-----------|
| ProgressSnapshot | `progress_snapshots` | D3, Doc2 | web dashboard ✅ · `/api/v1/analytics/*` ✅ |
| Recommendation | `recommendations` | D4 | iter 4 ✅ |
| PhotoAnalysis | `photo_analyses` | D2, D7 | assistant persist ✅ |
| Consultation | `consultations` | D5, D6, Doc3, Doc4 | seed ✅ · UI post-MVP 📋 |
| User.display_name, doctor | `users` | Doc1, web auth | seed + `/web/auth/resolve` ✅ |

### Остаётся (post-MVP / backend iter 4)

| Тема | Сценарии | Статус |
|------|----------|--------|
| Analytics REST (signals, recommendations API) | D3, D4 | backend iter 4 ✅ |
| Consultations UI + workflow | D5, D6, Doc2–Doc4 | post-MVP 📋 |
| Web photo upload в chat | D7 | post-MVP 📋 |

### Backlog (post-MVP data layer)

| Тема | Сценарии |
|------|----------|
| Web-auth (sessions, JWT) | все web |
| Doctor onboarding / привязка пациент | Doc1 |
| Object storage для фото (URL вместо base64) | D2, D7 |
| Отмена консультации пациентом | D6 |
| Прогноз (Forecast) | post iter 4 |

---

## Согласование с API v1

| Сценарий | Endpoint (существующий) |
|----------|-------------------------|
| D2, D7 (бот) | `POST /api/v1/assistant/messages` |
| D1 (бот) | `POST /api/v1/events/food`, `POST /api/v1/events/insulin`, `GET /api/v1/events/food` |

D3 dashboard — `/api/v1/web/patient|doctor/dashboard/*` ✅. D4, signals — **только требования к данным**; REST — [tasklist-backend](../tasks/tasklist-backend.md) 09–12. D5–D6, Doc* — post-MVP.

---

## Open questions (для итерации 2)

| Вопрос | Решение (iter 2) |
|--------|------------------|
| PhotoAnalysis | Таблица `photo_analyses` + FK — [schema-er.md](schema-er.md) |
| ProgressSnapshot | Persist в `progress_snapshots` |
| Doctor User | `users.role` + nullable `telegram_id` |
| Patient–doctor link | Через `consultations` |

---

## Связанные документы

- [user-scenarios.md](user-scenarios.md)
- [data-model.md](../data-model.md) — gap analysis
- [tasklist-database.md](../tasks/tasklist-database.md)
