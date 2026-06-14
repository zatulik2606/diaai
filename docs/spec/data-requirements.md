# Требования к данным

Опирается на [user-scenarios.md](user-scenarios.md) · [data-model.md](../data-model.md) · [api-contract.md](../api/api-contract.md)

Матрица read/write по сценариям. **API v1 не меняется** в рамках database iter 1 — новые endpoint'ы для D3–D7 и Doc* — scope [tasklist-backend](../tasks/tasklist-backend.md) 09–12 и [tasklist-web](../tasks/tasklist-web.md).

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

### Must add — до plan iter 4–5

| Сущность | Сценарии | Приоритет | Примечание |
|----------|----------|-----------|------------|
| ProgressSnapshot | D3, Doc2 | P1 | backend iter 4 |
| Recommendation | D4 | P1 | backend iter 4 |
| PhotoAnalysis | D2, D7 | P1 | open: таблица vs `dialog_requests.media` — iter 2 |
| Consultation | D5, D6, Doc3, Doc4 | P2 | web iter 5 |
| User.display_name, doctor users | Doc1, web | P2 | расширение `users` |

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

D3–D6, Doc* — **только требования к данным**; REST — [tasklist-backend](../tasks/tasklist-backend.md) 09–12.

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
