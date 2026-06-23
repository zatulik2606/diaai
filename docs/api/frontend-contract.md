# Frontend API Contract (v1)

REST-расширения backend для web-клиента. Machine-readable: [openapi.yaml](openapi.yaml) tag `web`.

Опирается на [api-contract.md](api-contract.md) · [conventions.md](conventions.md) · [frontend-requirements.md](../spec/frontend-requirements.md) · [data-model.md](../data-model.md)

**Статус:** контракт iter 0 ✅ · doctor API iter 1 ✅ · patient dashboard iter 3 ✅.

---

## Обзор

| Параметр | Значение |
|----------|----------|
| Базовый URL (local) | `http://127.0.0.1:8000` |
| Префикс web endpoint'ов | `/api/v1/web/` |
| Формат | JSON, `Content-Type: application/json` |
| Auth | `Authorization: Bearer <BACKEND_SERVICE_TOKEN>` (BFF → backend) |
| Пользователь web | `telegram_id` / `doctor_telegram_id` / `patient_telegram_id` в query или body |

**Версионирование:** non-breaking additions в `/api/v1/` per [conventions.md](conventions.md). Bot endpoint'ы v1 не меняются.

**Переиспользование v1 (без изменений):**

| Method | Path | Зона UI | Сценарий |
|--------|------|---------|----------|
| POST | `/api/v1/assistant/messages` | 3 — FAB chat | D2 — отправка сообщения |

---

## Сводная таблица endpoint'ов

| # | Method | Path | Query / Body | Response (root) | HTTP OK |
|---|--------|------|--------------|-----------------|---------|
| 1 | POST | `/api/v1/web/auth/resolve` | body: `username` | `user_id`, `telegram_id`, `role`, `display_name` | 200 |
| 2 | GET | `/api/v1/web/doctor/dashboard/summary` | `doctor_telegram_id`, `period_days?` | `period_days`, `kpis[]` | 200 |
| 3 | GET | `/api/v1/web/doctor/dashboard/activity` | `doctor_telegram_id`, `days?` | `days`, `series[]` | 200 |
| 4 | GET | `/api/v1/web/doctor/dashboard/questions` | `doctor_telegram_id`, `limit?`, `offset?` | `items[]`, `total`, `limit`, `offset` | 200 |
| 5 | GET | `/api/v1/web/doctor/dashboard/submissions` | `doctor_telegram_id`, `limit?`, `offset?` | `items[]`, `total`, `limit`, `offset` | 200 |
| 6 | GET | `/api/v1/web/doctor/dashboard/progress-matrix` | `doctor_telegram_id`, `period?`, `columns?` | `period`, `columns[]`, `rows[]` | 200 |
| 7 | GET | `/api/v1/web/leaderboard` | `doctor_telegram_id`, `period?`, `metric?`, `metric_x?`, `metric_y?` | `period`, `metric`, `table[]`, `scatter[]` | 200 |
| 8 | GET | `/api/v1/web/assistant/history` | `telegram_id`, `limit?`, `offset?` | `items[]`, `total`, `limit`, `offset` | 200 |
| 9 | POST | `/api/v1/assistant/messages` | body: `telegram_id`, `text?`, `image_base64?` | `dialog_id`, `request_id`, `reply` | 200 |
| 10 | GET | `/api/v1/web/patient/dashboard/summary` | `patient_telegram_id`, `period_days?` | `period_days`, `kpis[]` | 200 |
| 11 | GET | `/api/v1/web/patient/dashboard/activity` | `patient_telegram_id`, `days?` | `days`, `series[]` | 200 |
| 12 | GET | `/api/v1/web/patient/dashboard/questions` | `patient_telegram_id`, `limit?`, `offset?` | `items[]`, `total`, `limit`, `offset` | 200 |
| 13 | GET | `/api/v1/web/patient/dashboard/submissions` | `patient_telegram_id`, `limit?`, `offset?` | `items[]`, `total`, `limit`, `offset` | 200 |
| 14 | GET | `/api/v1/web/patient/dashboard/progress-matrix` | `patient_telegram_id`, `period?` | `period`, `columns[]`, `rows[]` (metric rows) | 200 |

---

## Cross-cutting

### Заголовки

Как в [api-contract.md](api-contract.md#cross-cutting): `Authorization`, `Content-Type`, опционально `X-Request-Id`.

### Ошибки

Единый `ErrorBody` для 4xx/5xx (кроме 422):

```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "User not found",
    "details": {}
  }
}
```

| HTTP | code | Когда |
|------|------|-------|
| 401 | `UNAUTHORIZED` | неверный Bearer |
| 403 | `FORBIDDEN` | role mismatch (non-doctor on doctor endpoints) |
| 404 | `NOT_FOUND` | username / user not found |
| 422 | — | FastAPI validation `detail[]` |
| 503 | `SERVICE_UNAVAILABLE` | DB unavailable |

### Pagination

List endpoint'ы: `limit` (default 20, max 100), `offset` (default 0).

Response wrapper:

```json
{
  "items": [],
  "total": 42,
  "limit": 20,
  "offset": 0
}
```

---

## Auth

### POST `/api/v1/web/auth/resolve`

Резолв Telegram username → пользователь. Вызывается из Next.js BFF.

| | |
|---|---|
| **Method** | `POST` |
| **Path** | `/api/v1/web/auth/resolve` |
| **Auth** | `Authorization: Bearer` |
| **Content-Type** | `application/json` |

**Request body:**

| Поле | Тип | Обяз. | Описание |
|------|-----|-------|----------|
| `username` | string | да | без `@`, lowercase |

```json
{ "username": "doctor_ivanov" }
```

**Response 200 — структура:**

| Поле | Тип | Описание |
|------|-----|----------|
| `user_id` | uuid | `users.id` |
| `telegram_id` | int64 | `users.telegram_id` |
| `role` | enum | `diabetic` \| `doctor` |
| `display_name` | string | `users.display_name` |

```json
{
  "user_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "telegram_id": 162684825,
  "role": "doctor",
  "display_name": "Александр Кожин"
}
```

**Errors:** 401, 404 `NOT_FOUND`, 422, 503

**MVP lookup (iter 1):** seed-map или `display_name` ILIKE; опционально `telegram_username` после миграции `003`.

---

## Doctor dashboard

Все endpoint'ы требуют `doctor_telegram_id` query param — идентификатор залогиненного доктора.

### GET `/api/v1/web/doctor/dashboard/summary`

4 KPI с дельтой к предыдущему окну. **Зона 1.**

| | |
|---|---|
| **Method** | `GET` |
| **Path** | `/api/v1/web/doctor/dashboard/summary` |
| **Auth** | `Authorization: Bearer` |

**Query parameters:**

| Param | Тип | Обяз. | Default | Описание |
|-------|-----|-------|---------|----------|
| `doctor_telegram_id` | int64 | да | — | Telegram ID доктора |
| `period_days` | integer | нет | 7 | длина текущего окна (дней) |

**Response 200 — структура:**

| Поле | Тип | Описание |
|------|-----|----------|
| `period_days` | integer | echo query |
| `kpis` | array | ровно 4 элемента |
| `kpis[].id` | string | `active_patients` \| `total_xe` \| `questions_count` \| `food_events_count` |
| `kpis[].label` | string | UI label |
| `kpis[].value` | number | текущее значение |
| `kpis[].delta` | number | разница с prev window |
| `kpis[].delta_pct` | number | % change |
| `kpis[].trend` | enum | `up` \| `down` \| `flat` |

**Errors:** 401, 403 (non-doctor), 422, 503

**Response 200:**

```json
{
  "period_days": 7,
  "kpis": [
    {
      "id": "active_patients",
      "label": "Активные пациенты",
      "value": 12,
      "delta": 2,
      "delta_pct": 20.0,
      "trend": "up"
    },
    {
      "id": "total_xe",
      "label": "Сумма ХЕ",
      "value": 156.5,
      "delta": -12.3,
      "delta_pct": -7.3,
      "trend": "down"
    },
    {
      "id": "questions_count",
      "label": "Вопросов",
      "value": 34,
      "delta": 5,
      "delta_pct": 17.2,
      "trend": "up"
    },
    {
      "id": "food_events_count",
      "label": "Событий питания",
      "value": 89,
      "delta": 0,
      "delta_pct": 0.0,
      "trend": "flat"
    }
  ]
}
```

| KPI id | PG sources |
|--------|------------|
| `active_patients` | distinct `users.id` where `role=diabetic` with activity in window |
| `total_xe` | `SUM(food_events.xe)` |
| `questions_count` | `COUNT(dialog_requests)` where `type=text` |
| `food_events_count` | `COUNT(food_events)` |

`trend`: `up` if delta > 0, `down` if delta < 0, else `flat`.

---

### GET `/api/v1/web/doctor/dashboard/activity`

Time series активности по дням. **Зона 1.**

| | |
|---|---|
| **Method** | `GET` |
| **Path** | `/api/v1/web/doctor/dashboard/activity` |
| **Auth** | `Authorization: Bearer` |

**Query parameters:**

| Param | Тип | Обяз. | Default | Описание |
|-------|-----|-------|---------|----------|
| `doctor_telegram_id` | int64 | да | — | Telegram ID доктора |
| `days` | integer | нет | 14 | число календарных дней |

**Response 200 — структура:**

| Поле | Тип | Описание |
|------|-----|----------|
| `days` | integer | echo query |
| `series` | array | length = `days` |
| `series[].date` | date | `YYYY-MM-DD` UTC |
| `series[].requests_count` | integer | ≥ 0 |
| `series[].food_events_count` | integer | ≥ 0 |

**Errors:** 401, 403, 422, 503

**Response 200:**

```json
{
  "days": 14,
  "series": [
    {
      "date": "2026-05-25",
      "requests_count": 5,
      "food_events_count": 12
    },
    {
      "date": "2026-05-26",
      "requests_count": 3,
      "food_events_count": 8
    }
  ]
}
```

| Поле | PG |
|------|-----|
| `date` | calendar day UTC |
| `requests_count` | `dialog_requests` grouped by `DATE(created_at)` |
| `food_events_count` | `food_events` grouped by `DATE(recorded_at)` |

---

### GET `/api/v1/web/doctor/dashboard/questions`

Лента вопросов пациентов. **Зона 1.**

| | |
|---|---|
| **Method** | `GET` |
| **Path** | `/api/v1/web/doctor/dashboard/questions` |
| **Auth** | `Authorization: Bearer` |

**Query parameters:**

| Param | Тип | Обяз. | Default | Описание |
|-------|-----|-------|---------|----------|
| `doctor_telegram_id` | int64 | да | — | Telegram ID доктора |
| `limit` | integer | нет | 20 | max 100 |
| `offset` | integer | нет | 0 | pagination |

**Response 200 — структура:**

| Поле | Тип | Описание |
|------|-----|----------|
| `items` | array | sorted by `created_at` desc |
| `items[].id` | uuid | `dialog_requests.id` |
| `items[].patient.user_id` | uuid | |
| `items[].patient.display_name` | string | |
| `items[].patient.telegram_id` | int64 | optional |
| `items[].content` | string | вопрос |
| `items[].reply` | string | ответ ассистента |
| `items[].created_at` | datetime | ISO 8601 UTC |
| `total` | integer | всего записей |
| `limit` | integer | echo |
| `offset` | integer | echo |

**Errors:** 401, 403, 422, 503

**Response 200:**

```json
{
  "items": [
    {
      "id": "req-uuid-1",
      "patient": {
        "user_id": "patient-uuid",
        "display_name": "Иван П.",
        "telegram_id": 123456789
      },
      "content": "Сколько ХЕ в борще?",
      "reply": "Примерно 1.5–2 ХЕ на порцию 250 мл...",
      "created_at": "2026-06-07T10:30:00Z"
    }
  ],
  "total": 34,
  "limit": 20,
  "offset": 0
}
```

| Поле | PG |
|------|-----|
| `id` | `dialog_requests.id` |
| `patient.*` | join `users` on `dialog_requests.user_id` |
| `content` | `dialog_requests.content` |
| `reply` | `dialog_requests.reply` |
| `created_at` | `dialog_requests.created_at` |

Filter: `dialog_requests.type` in (`text`, `mixed`).

---

### GET `/api/v1/web/doctor/dashboard/submissions`

Лента фиксаций (food + photo). **Зона 1.**

| | |
|---|---|
| **Method** | `GET` |
| **Path** | `/api/v1/web/doctor/dashboard/submissions` |
| **Auth** | `Authorization: Bearer` |

**Query parameters:**

| Param | Тип | Обяз. | Default | Описание |
|-------|-----|-------|---------|----------|
| `doctor_telegram_id` | int64 | да | — | Telegram ID доктора |
| `limit` | integer | нет | 20 | max 100 |
| `offset` | integer | нет | 0 | pagination |

**Response 200 — структура:**

| Поле | Тип | Описание |
|------|-----|----------|
| `items` | array | mixed food + photo, by `recorded_at` desc |
| `items[].id` | uuid | |
| `items[].type` | enum | `food_event` \| `photo_analysis` |
| `items[].patient` | object | `user_id`, `display_name` |
| `items[].title` | string | описание / «Photo analysis» |
| `items[].xe` | number | |
| `items[].bje` | number | |
| `items[].confidence` | number \| null | только photo |
| `items[].recorded_at` | datetime | ISO 8601 UTC |
| `items[].detail_url` | string | frontend route |
| `total`, `limit`, `offset` | integer | pagination |

**Errors:** 401, 403, 422, 503

**Response 200:**

```json
{
  "items": [
    {
      "id": "food-uuid-1",
      "type": "food_event",
      "patient": {
        "user_id": "patient-uuid",
        "display_name": "Иван П."
      },
      "title": "Овсянка с ягодами",
      "xe": 2.5,
      "bje": 1.0,
      "recorded_at": "2026-06-07T08:15:00Z",
      "detail_url": "/patients/patient-uuid/events/food-uuid-1"
    },
    {
      "id": "photo-uuid-1",
      "type": "photo_analysis",
      "patient": {
        "user_id": "patient-uuid-2",
        "display_name": "Мария С."
      },
      "title": "Photo analysis",
      "xe": 3.0,
      "bje": 0.5,
      "confidence": 0.87,
      "recorded_at": "2026-06-06T19:00:00Z",
      "detail_url": "/patients/patient-uuid-2/photos/photo-uuid-1"
    }
  ],
  "total": 15,
  "limit": 20,
  "offset": 0
}
```

| type | PG |
|------|-----|
| `food_event` | `food_events` |
| `photo_analysis` | `photo_analyses` (+ join `users`) |

`detail_url` — frontend route (не backend path); iter 3 использует для navigation.

---

### GET `/api/v1/web/doctor/dashboard/progress-matrix`

Матрица пациенты × периоды. **Зона 4.**

| | |
|---|---|
| **Method** | `GET` |
| **Path** | `/api/v1/web/doctor/dashboard/progress-matrix` |
| **Auth** | `Authorization: Bearer` |

**Query parameters:**

| Param | Тип | Обяз. | Default | Описание |
|-------|-----|-------|---------|----------|
| `doctor_telegram_id` | int64 | да | — | Telegram ID доктора |
| `period` | string | нет | `week` | `week` \| `month` |
| `columns` | string | нет | `period` | `period` \| `metric` |

**Response 200 — структура:**

| Поле | Тип | Описание |
|------|-----|----------|
| `period` | string | echo |
| `columns` | array | `{ id, label }` |
| `rows` | array | по пациентам |
| `rows[].patient` | object | `user_id`, `display_name` |
| `rows[].cells` | array | |
| `rows[].cells[].column_id` | string | matches `columns[].id` |
| `rows[].cells[].score` | number | 0–100 |
| `rows[].cells[].completion_pct` | number | 0–100 |
| `rows[].cells[].snapshot_date` | datetime \| null | hover tooltip |
| `rows[].cells[].metrics` | object | `xe`, `bje`, `insulin_dose` |

**Errors:** 401, 403, 422, 503

**Response 200:**

```json
{
  "period": "week",
  "columns": [
    { "id": "2026-W22", "label": "W22" },
    { "id": "2026-W23", "label": "W23" }
  ],
  "rows": [
    {
      "patient": {
        "user_id": "patient-uuid",
        "display_name": "Иван П."
      },
      "cells": [
        {
          "column_id": "2026-W22",
          "score": 72,
          "completion_pct": 72,
          "snapshot_date": "2026-05-31T23:59:59Z",
          "metrics": { "xe": 45.0, "bje": 12.0, "insulin_dose": 28.5 }
        },
        {
          "column_id": "2026-W23",
          "score": 85,
          "completion_pct": 85,
          "snapshot_date": "2026-06-07T23:59:59Z",
          "metrics": { "xe": 52.0, "bje": 14.0, "insulin_dose": 30.0 }
        }
      ]
    }
  ]
}
```

| Поле | PG |
|------|-----|
| `score` / `completion_pct` | `progress_snapshots` or computed |
| `snapshot_date` | `progress_snapshots.period_end` |
| `metrics` | `progress_snapshots` sums |

---

## Leaderboard

### GET `/api/v1/web/leaderboard`

Рейтинг + scatter. **Зона 2.** Таблица: rank, progress, продукты с ХЕ и медалями топ-5 по БЖЕ.

| | |
|---|---|
| **Method** | `GET` |
| **Path** | `/api/v1/web/leaderboard` |
| **Auth** | `Authorization: Bearer` |

**Query parameters:**

| Param | Тип | Обяз. | Default | Описание |
|-------|-----|-------|---------|----------|
| `doctor_telegram_id` | int64 | один из двух | — | Telegram ID доктора |
| `patient_telegram_id` | int64 | один из двух | — | Telegram ID пациента (тот же рейтинг когорты) |
| `period` | string | нет | `30d` | `7d`, `30d`, `90d` |
| `metric` | string | нет | `xe` | sort key для table (рейтинг пациентов) |
| `metric_x` | string | нет | `xe` | ось X scatter |
| `metric_y` | string | нет | `insulin_dose` | ось Y scatter |

`metric`, `metric_x`, `metric_y` ∈ `xe`, `bje`, `insulin_dose`, `activity_score`.

**Response 200 — структура:**

| Поле | Тип | Описание |
|------|-----|----------|
| `period` | string | echo |
| `metric` | string | echo |
| `table` | array | sorted by rank |
| `table[].rank` | integer | ≥ 1 |
| `table[].patient` | object | `user_id`, `display_name` |
| `table[].progress_pct` | number | 0–100 |
| `table[].products` | array | продукты пациента за период |
| `table[].products[].name` | string | название (из `food_events.description`, агрегат) |
| `table[].products[].xe` | number | сумма ХЕ по продукту за период |
| `table[].products[].bje` | number | сумма БЖЕ по продукту за период |
| `table[].products[].bje_medal` | string \| null | `gold` \| `silver` \| `bronze` \| `fourth` \| `fifth` — если продукт в топ-5 когорты по БЖЕ |
| `scatter` | array | |
| `scatter[].patient_id` | uuid | |
| `scatter[].display_name` | string | |
| `scatter[].x` | number | |
| `scatter[].y` | number | |

**Errors:** 401, 403, 422, 503

**Response 200:**

```json
{
  "period": "30d",
  "metric": "xe",
  "table": [
    {
      "rank": 1,
      "patient": {
        "user_id": "uuid-1",
        "display_name": "Мария С."
      },
      "progress_pct": 92,
      "products": [
        {
          "name": "Овсянка",
          "xe": 24.5,
          "bje": 18.0,
          "bje_medal": "gold"
        },
        {
          "name": "Яблоко",
          "xe": 8.0,
          "bje": 2.5,
          "bje_medal": null
        }
      ]
    },
    {
      "rank": 2,
      "patient": {
        "user_id": "uuid-2",
        "display_name": "Иван П."
      },
      "progress_pct": 78,
      "products": [
        {
          "name": "Овсянка",
          "xe": 12.0,
          "bje": 9.0,
          "bje_medal": "gold"
        },
        {
          "name": "Творог",
          "xe": 6.5,
          "bje": 14.0,
          "bje_medal": "silver"
        }
      ]
  ],
  "scatter": [
    {
      "patient_id": "uuid-1",
      "display_name": "Мария С.",
      "x": 120.5,
      "y": 45.0
    }
  ]
}
```

| Поле | PG |
|------|-----|
| `rank` | computed order by `metric` |
| `progress_pct` | vs period goal from `progress_snapshots` |
| `products.*` | `food_events` grouped by `description` per `user_id` in window |
| `bje_medal` | топ-5 продуктов когорты по сумме `bje` за период → `gold`…`fifth` |
| `scatter.*` | same cohort, axes from `metric_x`, `metric_y` |

---

## Analytics query (Text-to-SQL, iter 9)

### POST `/api/v1/web/analytics/query`

Ad-hoc вопрос по данным БД. **Patient dashboard + doctor leaderboard.**

| | |
|---|---|
| **Method** | `POST` |
| **Path** | `/api/v1/web/analytics/query` |
| **Auth** | `Authorization: Bearer` |

**Query:** `patient_telegram_id` (diabetic) **или** `doctor_telegram_id` (doctor) — как leaderboard.

**Request:**

```json
{ "question": "Сколько ХЕ я съел за последние 7 дней?" }
```

**Response 200:**

```json
{
  "answer": "Результат: 42.5.",
  "columns": ["total_xe"],
  "rows": [[42.5]],
  "chart_hint": "scalar"
}
```

| `chart_hint` | UI |
|--------------|-----|
| `scalar` | текст ответа |
| `bar` | bar chart + таблица |
| `line` | line chart (future) |
| `table` | таблица |

**BFF:** `POST /api/analytics/query` (session cookie) → proxy выше.

Guardrails: [adr-004-text-to-sql.md](../adr/adr-004-text-to-sql.md) · scenarios: [text-to-sql-scenarios.md](../spec/text-to-sql-scenarios.md) · architecture: [text-to-sql-architecture.md](../spec/text-to-sql-architecture.md)

---

## Assistant history (FAB chat)

### GET `/api/v1/web/assistant/history`

История чата для FAB. **Зона 3.**

| | |
|---|---|
| **Method** | `GET` |
| **Path** | `/api/v1/web/assistant/history` |
| **Auth** | `Authorization: Bearer` |

**Query parameters:**

| Param | Тип | Обяз. | Default | Описание |
|-------|-----|-------|---------|----------|
| `telegram_id` | int64 | да | — | пользователь сессии |
| `limit` | integer | нет | 50 | max 100 |
| `offset` | integer | нет | 0 | pagination |

**Response 200 — структура:**

| Поле | Тип | Описание |
|------|-----|----------|
| `items` | array | chronological |
| `items[].id` | string | message id |
| `items[].role` | enum | `user` \| `assistant` |
| `items[].text` | string | content or reply |
| `items[].created_at` | datetime | ISO 8601 UTC |
| `total`, `limit`, `offset` | integer | pagination |

**Errors:** 401, 404 (user), 422, 503

**Response 200 (example):**

```json
{
  "items": [
    {
      "id": "req-uuid-1",
      "role": "user",
      "text": "Сколько ХЕ в яблоке?",
      "created_at": "2026-06-07T09:00:00Z"
    },
    {
      "id": "req-uuid-1-reply",
      "role": "assistant",
      "text": "Среднее яблоко ~15–20 г углеводов...",
      "created_at": "2026-06-07T09:00:05Z"
    }
  ],
  "total": 10,
  "limit": 50,
  "offset": 0
}
```

| Поле | PG |
|------|-----|
| user message | `dialog_requests.content` |
| assistant message | `dialog_requests.reply` |
| `created_at` | `dialog_requests.created_at` |

---

### POST `/api/v1/assistant/messages`

Отправка сообщения в чат. **Зона 3.** Полная спецификация — [api-contract.md](api-contract.md#post-apiv1assistantmessages).

| | |
|---|---|
| **Method** | `POST` |
| **Path** | `/api/v1/assistant/messages` |
| **Auth** | `Authorization: Bearer` |
| **Content-Type** | `application/json` |

**Request body (web MVP — текст):**

| Поле | Тип | Обяз. | Описание |
|------|-----|-------|----------|
| `telegram_id` | int64 | да | из web-сессии |
| `text` | string | да* | min 1 символ (*web MVP без фото) |
| `image_base64` | string | нет | iter 5+ |

```json
{
  "telegram_id": 123456789,
  "text": "Сколько ХЕ в яблоке?"
}
```

**Response 200 — структура:**

| Поле | Тип | Описание |
|------|-----|----------|
| `dialog_id` | uuid | активный диалог |
| `request_id` | uuid | сохранённый запрос |
| `reply` | string | ответ LLM |

```json
{
  "dialog_id": "550e8400-e29b-41d4-a716-446655440000",
  "request_id": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
  "reply": "Среднее яблоко ~15–20 г углеводов..."
}
```

**Errors:** 401, 400, 422, 404, 502, 503

---

## Patient dashboard (iter 3)

Все endpoint'ы требуют `patient_telegram_id` query param — залогиненный пациент с `role=diabetic`.

### GET `/api/v1/web/patient/dashboard/summary`

KPI ids: `total_xe`, `questions_count`, `food_events_count`, `insulin_total`.

```json
{
  "period_days": 7,
  "kpis": [
    {
      "id": "total_xe",
      "label": "Сумма ХЕ",
      "value": 12.5,
      "delta": 2.0,
      "delta_pct": 19.0,
      "trend": "up"
    }
  ]
}
```

**Errors:** 401, 403 (non-diabetic), 404, 422, 503

### GET `/api/v1/web/patient/dashboard/activity`

Тот же формат, что doctor activity: `{ "days": 14, "series": [{ "date", "requests_count", "food_events_count" }] }`.

### GET `/api/v1/web/patient/dashboard/questions`

Items без поля `patient`: `{ "id", "content", "reply", "created_at" }`.

### GET `/api/v1/web/patient/dashboard/submissions`

Items без поля `patient`: `{ "id", "type", "title", "xe", "bje", "confidence", "recorded_at", "detail_url" }`.

### GET `/api/v1/web/patient/dashboard/progress-matrix`

Rows = метрики (`xe`, `bje`, `insulin`), columns = периоды:

```json
{
  "period": "week",
  "columns": [{ "id": "2026-W22", "label": "W22" }],
  "rows": [
    {
      "metric_id": "xe",
      "label": "ХЕ",
      "cells": [{ "column_id": "2026-W22", "value": 72.0, "completion_pct": 85.0, "snapshot_date": "..." }]
    }
  ]
}
```

---

## Smoke examples (iter 1)

```bash
# Auth resolve
curl -s -X POST http://127.0.0.1:8000/api/v1/web/auth/resolve \
  -H "Authorization: Bearer $BACKEND_SERVICE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"username":"doctor_ivanov"}'

# Dashboard summary
curl -s "http://127.0.0.1:8000/api/v1/web/doctor/dashboard/summary?doctor_telegram_id=162684825" \
  -H "Authorization: Bearer $BACKEND_SERVICE_TOKEN"

# Leaderboard
curl -s "http://127.0.0.1:8000/api/v1/web/leaderboard?doctor_telegram_id=162684825&period=30d" \
  -H "Authorization: Bearer $BACKEND_SERVICE_TOKEN"

# Chat history
curl -s "http://127.0.0.1:8000/api/v1/web/assistant/history?telegram_id=123456789&limit=20" \
  -H "Authorization: Bearer $BACKEND_SERVICE_TOKEN"

# Chat send
curl -s -X POST http://127.0.0.1:8000/api/v1/assistant/messages \
  -H "Authorization: Bearer $BACKEND_SERVICE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"telegram_id":123456789,"text":"Сколько ХЕ в яблоке?"}'

# Patient dashboard (iter 3)
curl -s "http://127.0.0.1:8000/api/v1/web/patient/dashboard/summary?patient_telegram_id=900000001" \
  -H "Authorization: Bearer $BACKEND_SERVICE_TOKEN"
```

---

## Согласование

### UI зона → endpoint

| Зона | UI | Endpoint'ы |
|------|-----|------------|
| 1 | Dashboard (KPI, chart, questions, submissions) | `GET …/summary`, `…/activity`, `…/questions`, `…/submissions` |
| 2 | Leaderboard | `GET …/leaderboard` |
| 3 | FAB chat | `GET …/assistant/history`, `POST /api/v1/assistant/messages` |
| 4 | Progress matrix | `GET …/progress-matrix` |
| auth | Login | `POST …/auth/resolve` |

| Документ | Связь |
|----------|-------|
| [api-contract.md](api-contract.md) | bot v1 unchanged; cross-link here |
| [tasklist-backend.md](../tasks/tasklist-backend.md) iter 4 | analytics naming aligned (`xe`, `bje`) |
| [frontend-requirements.md](../spec/frontend-requirements.md) | UI blocks → endpoints |

---

## Out of scope (контракт)

- Web JWT / session endpoint'ы на backend (session — client/BFF iter 2)
- CRUD consultations Doc3–Doc4
- File upload для chat photo (iter 5+)
