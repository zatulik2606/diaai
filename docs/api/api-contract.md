# API-контракт diaai (v1)

Описание REST API backend для MVP. Machine-readable: [openapi.yaml](openapi.yaml) (tags: `system`, `assistant`, `media`, `events`, `analytics`, `web`). Соглашения и коды ошибок: [conventions.md](conventions.md).

**Статус:** bot endpoint'ы ✅ (backend iter 2–3) · web `/api/v1/web/*` ✅ (frontend iter 1) · analytics `/api/v1/analytics/*` 📋 contract (backend iter 4, task 09 ✅ → impl 10–11).

**Клиенты:**

| Клиент | Endpoint'ы | Статус |
|--------|------------|--------|
| Telegram-бот | `/api/v1/assistant/*`, `/api/v1/events/*`, `/api/v1/analytics/*` | ✅ assistant/events · 📋 analytics (iter 4) |
| Web (Next.js) | `/api/v1/web/*` + reuse `POST /assistant/messages` | ✅ [frontend-contract.md](frontend-contract.md) |

Продуктовые требования web UI — [frontend-requirements.md](../spec/frontend-requirements.md).

---

## Обзор

| Параметр | Значение |
|----------|----------|
| Базовый URL (local) | `http://127.0.0.1:8000` |
| Версия API | `/api/v1/` |
| Формат | JSON, `Content-Type: application/json` |
| Auth | `Authorization: Bearer <BACKEND_SERVICE_TOKEN>` |
| Пользователь (bot) | `telegram_id` — Telegram `chat.id` в теле POST или query GET |
| Пользователь (web) | `doctor_telegram_id` / `telegram_id` в query; `username` в body auth; BFF держит Bearer |

**Сценарии (bot):**

| ID | Назначение | Endpoint'ы |
|----|------------|------------|
| A | Вопрос ассистенту (текст / фото → LLM) | `POST /api/v1/assistant/messages` |
| B | Фиксация питания и инсулина | `POST /api/v1/events/food`, `POST /api/v1/events/insulin`, `GET /api/v1/events/food` |
| C | Динамика и рекомендации (D3, D4) | `GET /api/v1/analytics/progress`, `signals`, `recommendations` |

**Сценарии (web)** — см. [frontend-requirements.md](../spec/frontend-requirements.md):

| Зона | Сценарии | Endpoint'ы |
|------|----------|------------|
| 1 Dashboard доктора | Doc1, Doc2 | `GET /api/v1/web/doctor/dashboard/*` |
| 2 Лидерboard | D3 | `GET /api/v1/web/leaderboard` |
| 3 FAB-чат | D2 | `GET /api/v1/web/assistant/history`, `POST /api/v1/assistant/messages` |
| 4 Матрица прогресса | Doc2, D3 | `GET /api/v1/web/doctor/dashboard/progress-matrix` |
| Auth (login) | — | `POST /api/v1/web/auth/resolve` |

**Вне scope v1:** JWT/web-session на backend, CRUD консультаций Doc3–Doc4.

**Analytics vs web:** dashboard KPI — `/api/v1/web/*` ✅; unified bot API — `/api/v1/analytics/*` 📋 impl (контракт task 09). Text-to-SQL — `/api/v1/web/analytics/query` (doctor, отдельный контур).

**Web:** детальные контракты, JSON-примеры и PG mapping — [frontend-contract.md](frontend-contract.md).

---

## Карта endpoint'ов

### System и bot (реализовано ✅)

| Method | Path | Auth | Success | Описание |
|--------|------|------|---------|----------|
| GET | `/health` | нет | 200 | Health check + версия приложения |
| POST | `/api/v1/assistant/messages` | Bearer | 200 | Сценарий A / D2 — вопрос ассистенту |
| POST | `/api/v1/media/transcribe` | Bearer | 200 | STT: voice → text (bot, web fallback) |
| POST | `/api/v1/events/food` | Bearer | 201 | Создать событие питания |
| GET | `/api/v1/events/food` | Bearer | 200 | Список событий питания (optional MVP) |
| POST | `/api/v1/events/insulin` | Bearer | 201 | Создать событие инсулина |

### Web (`/api/v1/web/*`) — ✅ impl

| Method | Path | Auth | Success | Зона | Описание |
|--------|------|------|---------|------|----------|
| POST | `/api/v1/web/auth/resolve` | Bearer | 200 | auth | username → user |
| GET | `/api/v1/web/doctor/dashboard/summary` | Bearer | 200 | 1 | 4 KPI + delta |
| GET | `/api/v1/web/doctor/dashboard/activity` | Bearer | 200 | 1 | активность по дням |
| GET | `/api/v1/web/doctor/dashboard/questions` | Bearer | 200 | 1 | лента вопросов |
| GET | `/api/v1/web/doctor/dashboard/submissions` | Bearer | 200 | 1 | food + photo events |
| GET | `/api/v1/web/doctor/dashboard/progress-matrix` | Bearer | 200 | 4 | матрица пациенты × периоды |
| GET | `/api/v1/web/leaderboard` | Bearer | 200 | 2 | таблица + scatter |
| POST | `/api/v1/web/analytics/query` | Bearer | 200 | 2 | NL → read-only SQL (Text-to-SQL) |
| GET | `/api/v1/web/assistant/history` | Bearer | 200 | 3 | история чата |
| GET | `/api/v1/web/patient/dashboard/summary` | Bearer | 200 | 1 | patient KPI + delta |
| GET | `/api/v1/web/patient/dashboard/activity` | Bearer | 200 | 1 | активность пациента |
| GET | `/api/v1/web/patient/dashboard/questions` | Bearer | 200 | 1 | вопросы пациента |
| GET | `/api/v1/web/patient/dashboard/submissions` | Bearer | 200 | 1 | фиксации пациента |
| GET | `/api/v1/web/patient/dashboard/progress-matrix` | Bearer | 200 | 4 | метрики × периоды |

Doctor dashboard/leaderboard: query `doctor_telegram_id`. Patient dashboard: query `patient_telegram_id`. Списки: `limit` (default 20, max 100), `offset` (default 0), ответ `{ items, total, limit, offset }`.

Полные параметры и структуры ответов — [frontend-contract.md](frontend-contract.md).

### Analytics (`/api/v1/analytics/*`) — 📋 contract ✅, impl task 10–11

| Method | Path | Auth | Success | Сценарий | Описание |
|--------|------|------|---------|----------|----------|
| GET | `/api/v1/analytics/progress` | Bearer | 200 | D3 / C | снимок прогресса за day/week/month |
| GET | `/api/v1/analytics/signals` | Bearer | 200 | D3 / C | rule-based сигналы изменений |
| GET | `/api/v1/analytics/recommendations` | Bearer | 200 | D4 / C | справочные рекомендации (paginated) |

Query: `telegram_id` (обязательный). Role: `diabetic` only → иначе 403. Детали JSON — [scenarios/analytics-progress.md](scenarios/analytics-progress.md) · [scenarios/analytics-signals-recommendations.md](scenarios/analytics-signals-recommendations.md).

Runtime Swagger: `make backend-run` → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs). Сверка с yaml: `make backend-openapi-export`.

---

## Cross-cutting

### Заголовки

| Заголовок | Обязательный | Описание |
|-----------|--------------|----------|
| `Authorization` | да (кроме `/health`) | `Bearer <token>` — значение env `BACKEND_SERVICE_TOKEN` |
| `Content-Type` | да для POST | `application/json` |
| `X-Request-Id` | нет | UUID трассировки; backend echo в логах |

### Именование и типы

- JSON-поля: `snake_case`
- UUID: строка RFC 4122
- Время: ISO 8601 UTC (`2026-06-07T12:00:00Z`)
- Домен: `xe` — хлебные единицы (ХЕ), `bje` — белково-жировые единицы (БЖЕ)

### Формат ошибок

**4xx/5xx (кроме 422):** единое тело `ErrorBody`:

```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Краткое описание для клиента",
    "details": {}
  }
}
```

**422 (валидация Pydantic):** стандартный FastAPI `detail` (массив объектов с `loc`, `msg`, `type`). Клиенты обрабатывают оба формата.

Полная таблица кодов — [conventions.md](conventions.md#http-коды-ошибок).

**Web-specific:** doctor endpoint'ы → **403** `FORBIDDEN` при role mismatch; auth resolve → **404** `NOT_FOUND` если username не найден.

### Pagination (web)

List endpoint'ы web (`questions`, `submissions`, `assistant/history`):

| Query | Default | Max | Описание |
|-------|---------|-----|----------|
| `limit` | 20 | 100 | размер страницы |
| `offset` | 0 | — | смещение |

Обёртка ответа: `items[]`, `total`, `limit`, `offset`. Bot `GET /events/food` — голый array (backlog без изменений).

---

## GET /health

Проверка готовности backend. Auth не требуется.

**Response 200:**

```json
{
  "status": "ok",
  "version": "1.0.0"
}
```

---

## POST /api/v1/assistant/messages

Сценарий A (bot) / D2 (web FAB): текстовый вопрос или фото → OpenRouter → ответ ассистента. Сохраняет **Запрос** в активном **Диалоге**.

**Web:** BFF передаёт `telegram_id` из сессии; на MVP FAB — только `text` (фото iter 5+). История — `GET /api/v1/web/assistant/history`.

### Request

**Текст:**

```json
{
  "telegram_id": 123456789,
  "text": "Сколько ХЕ в борще с хлебом?"
}
```

**Фото (с опциональной подписью):**

```json
{
  "telegram_id": 123456789,
  "text": "Оцени состав и ориентировочные ХЕ по фото.",
  "image_base64": "<base64>",
  "image_media_type": "image/jpeg"
}
```

| Поле | Тип | Обязательный | Описание |
|------|-----|--------------|----------|
| `telegram_id` | integer | да | Telegram `chat.id` |
| `text` | string | условно | min 1 символ, если передан |
| `image_base64` | string | условно | Base64 изображения; см. правила ниже |
| `image_media_type` | string | нет | По умолчанию `image/jpeg` |

**Правила контента:**

- Обязателен **либо** непустой `text`, **либо** `image_base64` (можно оба).
- Оба отсутствуют / пусты → **400** `BAD_REQUEST`.
- `image_base64`: валидный base64; decoded size ≤ **5 MB**. Префиксы data-URL (`data:image/...;base64,`, `image/webp;base64,` и т.п.) **снимаются автоматически** на backend.
- Невалидный base64 или превышение лимита → **422**.

### Response 200

```json
{
  "dialog_id": "550e8400-e29b-41d4-a716-446655440000",
  "request_id": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
  "reply": "Ориентировочно 3–4 ХЕ…"
}
```

| Поле | Тип | Описание |
|------|-----|----------|
| `dialog_id` | uuid | Активный диалог (`channel=telegram`) |
| `request_id` | uuid | Сохранённый запрос |
| `reply` | string | Ответ LLM (без назначения доз инсулина) |

### Ошибки

| HTTP | Когда |
|------|-------|
| 401 | Нет/неверный Bearer token или `telegram_id` |
| 400 | Нет текста и фото |
| 422 | Невалидные типы, base64, лимит изображения |
| 404 | Диалог не найден |
| 502 | OpenRouter недоступен / таймаут |
| 503 | PostgreSQL недоступна |

Детали поведения: [scenarios/assistant-question.md](scenarios/assistant-question.md).

---

## POST /api/v1/events/food

Сценарий B: структурированная запись приёма пищи.

### Request

```json
{
  "telegram_id": 123456789,
  "description": "борщ и кусок хлеба",
  "xe": 3.5,
  "bje": 1.0,
  "proteins": null,
  "fats": null,
  "carbs": null,
  "source": "text",
  "request_id": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
  "comment": "оценка по описанию"
}
```

| Поле | Тип | Обязательный | Описание |
|------|-----|--------------|----------|
| `telegram_id` | integer | да | Владелец события |
| `description` | string | да | Что съедено, min 1 символ |
| `xe` | number | да | ХЕ, ≥ 0 |
| `bje` | number | да | БЖЕ, ≥ 0 |
| `proteins` | number \| null | нет | Белки, г |
| `fats` | number \| null | нет | Жиры, г |
| `carbs` | number \| null | нет | Углеводы, г |
| `source` | enum | да | `text`, `photo_dish`, `photo_product` |
| `request_id` | uuid | нет | Связь с запросом сценария A |
| `comment` | string | нет | Пояснение |

### Response 201

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "recorded_at": "2026-06-07T12:00:00Z"
}
```

### Ошибки

| HTTP | Когда |
|------|-------|
| 401 | Нет/неверный token или `telegram_id` |
| 403 | `request_id` принадлежит другому пользователю |
| 404 | `request_id` не найден |
| 422 | Отрицательные `xe`/`bje`, неверный `source`, невалидный UUID |
| 503 | PostgreSQL недоступна |

---

## POST /api/v1/events/insulin

Фиксация введённого инсулина (не назначение дозы).

### Request

```json
{
  "telegram_id": 123456789,
  "dose": 4.0,
  "food_event_id": "550e8400-e29b-41d4-a716-446655440001",
  "injected_at": "2026-06-07T11:55:00Z",
  "comment": "перед обедом"
}
```

| Поле | Тип | Обязательный | Описание |
|------|-----|--------------|----------|
| `telegram_id` | integer | да | Владелец события |
| `dose` | number | да | Доза в единицах, **> 0** |
| `food_event_id` | uuid | нет | Связанный приём пищи |
| `injected_at` | datetime ISO 8601 | нет | По умолчанию — now UTC |
| `comment` | string | нет | Контекст |

### Response 201

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440002",
  "recorded_at": "2026-06-07T11:55:00Z"
}
```

### Ошибки

| HTTP | Когда |
|------|-------|
| 401 | Нет/неверный token или `telegram_id` |
| 403 | `food_event_id` принадлежит другому пользователю |
| 404 | `food_event_id` не найден |
| 422 | `dose` ≤ 0, невалидный UUID/datetime |
| 503 | PostgreSQL недоступна |

---

## GET /api/v1/events/food

Список событий питания пользователя (optional MVP).

```
GET /api/v1/events/food?telegram_id=123456789&from=2026-06-01T00:00:00Z&to=2026-06-07T23:59:59Z
```

| Query | Обязательный | Описание |
|-------|--------------|----------|
| `telegram_id` | да | Владелец событий |
| `from` | нет | Начало периода, ISO 8601 |
| `to` | нет | Конец периода, ISO 8601 |

**Response 200:** массив объектов `FoodEvent` (поля создания + `id`, `recorded_at`).

**Backlog:** pagination (`page`/`page_size` или cursor); сейчас — голый array без limit.

### Ошибки

| HTTP | Когда |
|------|-------|
| 401 | Нет/неверный token или `telegram_id` |
| 422 | Невалидный формат `from`/`to` |
| 503 | PostgreSQL недоступна |

Детали сценария B: [scenarios/event-record.md](scenarios/event-record.md).

---

## Web client — `/api/v1/web/*`

Контракт зафиксирован в frontend iter 0; реализация — [frontend iter 1](../tasks/tasklist-frontend.md). Детали — [frontend-contract.md](frontend-contract.md).

### Auth (MVP)

| Шаг | Действие |
|-----|----------|
| 1 | Web: форма Telegram `@username` |
| 2 | Next.js BFF → `POST /api/v1/web/auth/resolve` с Bearer |
| 3 | Response: `user_id`, `telegram_id`, `role`, `display_name` |
| 4 | Сессия на клиенте (cookie/localStorage, iter 2) |

Demo doctor (seed): `username=doctor_ivanov`, `telegram_id=162684825`, `role=doctor`.

`BACKEND_SERVICE_TOKEN` **не** попадает в браузер.

### POST `/api/v1/web/auth/resolve`

| | |
|---|---|
| Body | `{ "username": "doctor_ivanov" }` — string, без `@`, lowercase |
| Response 200 | `user_id` (uuid), `telegram_id` (int64), `role` (`diabetic`\|`doctor`), `display_name` |
| Errors | 401, 404, 422, 503 |

### GET `/api/v1/web/doctor/dashboard/summary`

| Query | Обяз. | Default | Описание |
|-------|-------|---------|----------|
| `doctor_telegram_id` | да | — | Telegram ID доктора |
| `period_days` | нет | 7 | окно KPI |

Response 200: `{ period_days, kpis[] }` — 4 KPI (`active_patients`, `total_xe`, `questions_count`, `food_events_count`); каждый: `id`, `label`, `value`, `delta`, `delta_pct`, `trend` (`up`\|`down`\|`flat`).

### GET `/api/v1/web/doctor/dashboard/activity`

| Query | Обяз. | Default |
|-------|-------|---------|
| `doctor_telegram_id` | да | — |
| `days` | нет | 14 |

Response 200: `{ days, series[] }` — `series[].date`, `requests_count`, `food_events_count`.

### GET `/api/v1/web/doctor/dashboard/questions`

Query: `doctor_telegram_id`, `limit?`, `offset?`.

Response 200: paginated `{ items[], total, limit, offset }`; item: `id`, `patient`, `content`, `reply`, `created_at`.

### GET `/api/v1/web/doctor/dashboard/submissions`

Query: `doctor_telegram_id`, `limit?`, `offset?`.

Response 200: paginated; item: `id`, `type` (`food_event`\|`photo_analysis`), `patient`, `title`, `xe`, `bje`, `confidence?`, `recorded_at`, `detail_url`.

### GET `/api/v1/web/doctor/dashboard/progress-matrix`

| Query | Default | Значения |
|-------|---------|----------|
| `doctor_telegram_id` | — | required |
| `period` | `week` | `week`, `month` |
| `columns` | `period` | `period`, `metric` |

Response 200: `{ period, columns[{ id, label }], rows[{ patient, cells[] }] }`; cell: `column_id`, `score`, `completion_pct`, `snapshot_date`, `metrics`.

### GET `/api/v1/web/leaderboard`

Query: `doctor_telegram_id`, `period?` (`30d`), `metric?`, `metric_x?`, `metric_y?` — метрики: `xe`, `bje`, `insulin_dose`, `activity_score`.

Response 200: `{ period, metric, table[], scatter[] }`; table row: `rank`, `patient`, `progress_pct`, `products[]` (`name`, `xe`, `bje`, `bje_medal?`); scatter point: `patient_id`, `display_name`, `x`, `y`.

### GET `/api/v1/web/assistant/history`

Query: `telegram_id`, `limit?` (50), `offset?`.

Response 200: paginated; item: `id`, `role` (`user`\|`assistant`), `text`, `created_at`.

---

## Маппинг bot → API

| Bot | API |
|-----|-----|
| `message.chat.id` | `telegram_id` |
| `message.text` | `text` |
| `message.caption` или дефолт | `text` при фото |
| bytes из `download_file` → base64 | `image_base64` |
| env `BACKEND_SERVICE_TOKEN` | заголовок `Authorization` |

### Web → API

| Web | API |
|-----|-----|
| Login `@username` | `POST /api/v1/web/auth/resolve` body `username` |
| Session `telegram_id` | query `doctor_telegram_id` / `telegram_id` |
| Next.js Route Handler | Bearer `BACKEND_SERVICE_TOKEN` (server-only) |
| FAB send | `POST /api/v1/assistant/messages` |
| FAB history | `GET /api/v1/web/assistant/history` |
| Voice (web/bot) | `POST /api/v1/media/transcribe` → assistant |
| Analytics NL (doctor) | `POST /api/v1/web/analytics/query` |

---

## MVP-ограничения и backlog

| Тема | v1 bot | v1 web | Backlog |
|------|--------|--------|---------|
| `POST /assistant/messages` → 200 | ✅ | ✅ (FAB) | 201 + `Location` |
| Pagination GET food | голый array | — | cursor для bot |
| Pagination web lists | — | `limit`/`offset` | cursor |
| Rate limiting | нет | нет | 429 + `Retry-After` |
| Idempotency keys | нет | нет | `Idempotency-Key` для POST events |
| Единый формат 422 | dual | dual | маппинг post-MVP |
| `telegram_id` в query | bot GET food | web doctor/history | header v2 |
| `image_base64` > 5 MB | 422 | 422 | 413 `PAYLOAD_TOO_LARGE` |
| Username lookup | — | seed-map / display_name (iter 1) | `telegram_username` column |
| Web JWT | — | client session only | backend JWT post-MVP |

Design review (api-design-principles): [api-contract-review.md](api-contract-review.md) · contract tests: [docs/tech/api-contracts.md](../tech/api-contracts.md).

---

## Правила изменений

1. Любое изменение контракта — сначала этот документ и [openapi.yaml](openapi.yaml), затем код и `backend/tests/`.
2. Новый `error.code` — добавить в [conventions.md](conventions.md).
3. Breaking change (семантика HTTP, обязательные поля, коды) → `/api/v2/`.
4. Non-breaking: новые optional-поля, новые endpoint'ы в v1.

---

## Связанные документы

| Документ | Содержание |
|----------|------------|
| [openapi.yaml](openapi.yaml) | OpenAPI 3.1 (tags: `system`, `assistant`, `events`, `analytics`, `web`) |
| [api-contract-review.md](api-contract-review.md) | Design review (api-design-principles) |
| [frontend-contract.md](frontend-contract.md) | Web endpoint'ы — полные JSON и PG mapping |
| [frontend-requirements.md](../spec/frontend-requirements.md) | UI зоны 1–4, auth, wireframes |
| [conventions.md](conventions.md) | Auth, коды ошибок, лимиты |
| [scenarios/assistant-question.md](scenarios/assistant-question.md) | Сценарий A — детали |
| [scenarios/event-record.md](scenarios/event-record.md) | Сценарий B — детали |
| [scenarios/analytics-progress.md](scenarios/analytics-progress.md) | D3 — progress |
| [scenarios/analytics-signals-recommendations.md](scenarios/analytics-signals-recommendations.md) | D3/D4 — signals, recommendations |
| [data-model.md](../data-model.md) | Сущности и поля домена |
| [integrations.md](../integrations.md) | OpenRouter, PostgreSQL |
| [backend/README.md](../../backend/README.md) | Запуск и env |
