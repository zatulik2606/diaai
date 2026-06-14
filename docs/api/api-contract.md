# API-контракт diaai (v1)

Описание REST API backend для MVP. Machine-readable: [openapi.yaml](openapi.yaml). Соглашения и коды ошибок: [conventions.md](conventions.md).

**Статус:** реализовано ✅ (итерации 2–3). Клиент MVP — Telegram-бот (`src/diaai/backend_client.py`).

---

## Обзор

| Параметр | Значение |
|----------|----------|
| Базовый URL (local) | `http://127.0.0.1:8000` |
| Версия API | `/api/v1/` |
| Формат | JSON, `Content-Type: application/json` |
| Auth | `Authorization: Bearer <BACKEND_SERVICE_TOKEN>` |
| Пользователь | `telegram_id` — Telegram `chat.id` в теле POST или query GET |

**Сценарии:**

| ID | Назначение | Endpoint'ы |
|----|------------|------------|
| A | Вопрос ассистенту (текст / фото → LLM) | `POST /api/v1/assistant/messages` |
| B | Фиксация питания и инсулина | `POST /api/v1/events/food`, `POST /api/v1/events/insulin`, `GET /api/v1/events/food` |

**Вне scope v1:** web-auth, роли доктора, аналитика (`/api/v1/analytics/*` — итерация 4), CRUD диалогов.

---

## Карта endpoint'ов

| Method | Path | Auth | Success | Описание |
|--------|------|------|---------|----------|
| GET | `/health` | нет | 200 | Health check + версия приложения |
| POST | `/api/v1/assistant/messages` | Bearer | 200 | Сценарий A — вопрос ассистенту |
| POST | `/api/v1/events/food` | Bearer | 201 | Создать событие питания |
| GET | `/api/v1/events/food` | Bearer | 200 | Список событий питания (optional MVP) |
| POST | `/api/v1/events/insulin` | Bearer | 201 | Создать событие инсулина |

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

Сценарий A: текстовый вопрос или фото → OpenRouter → ответ ассистента. Сохраняет **Запрос** в активном **Диалоге**.

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

## Маппинг bot → API

| Bot | API |
|-----|-----|
| `message.chat.id` | `telegram_id` |
| `message.text` | `text` |
| `message.caption` или дефолт | `text` при фото |
| bytes из `download_file` → base64 | `image_base64` |
| env `BACKEND_SERVICE_TOKEN` | заголовок `Authorization` |

---

## MVP-ограничения и backlog

| Тема | v1 | Backlog |
|------|----|---------|
| `POST /assistant/messages` → 200 | осознанно (ответ диалога) | 201 + `Location` |
| Pagination GET food | голый array | `page`/`page_size` или cursor |
| Rate limiting | нет | 429 + `Retry-After` |
| Idempotency keys | нет | `Idempotency-Key` для POST events |
| Единый формат 422 | dual (FastAPI `detail` + `ErrorBody`) | маппинг post-MVP |
| `telegram_id` в query | допустимо | header / nested resource v2 |
| `image_base64` > 5 MB | 422 | 413 `PAYLOAD_TOO_LARGE` |

Design review и contract tests: [docs/tech/api-contracts.md](../tech/api-contracts.md).

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
| [openapi.yaml](openapi.yaml) | OpenAPI 3.1 |
| [conventions.md](conventions.md) | Auth, коды ошибок, лимиты |
| [scenarios/assistant-question.md](scenarios/assistant-question.md) | Сценарий A — детали |
| [scenarios/event-record.md](scenarios/event-record.md) | Сценарий B — детали |
| [data-model.md](../data-model.md) | Сущности и поля домена |
| [integrations.md](../integrations.md) | OpenRouter, PostgreSQL |
| [backend/README.md](../../backend/README.md) | Запуск и env |
