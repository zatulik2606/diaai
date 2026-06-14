# Сценарий B: фиксация события

Полный контракт: [api-contract.md](../api-contract.md) · Продукт: [idea.md](../../idea.md) · Сущности: Событие питания, Событие инсулина · Соглашения: [conventions.md](../conventions.md)

Структурированная фиксация питания и инсулина (сейчас в боте — через диалог LLM; API готовит task-05 и task-07).

## POST /api/v1/events/food

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
| `xe` | number | да | Хлебные единицы (≥ 0) |
| `bje` | number | да | Белково-жировые единицы (≥ 0) |
| `proteins` | number \| null | нет | БЖУ: белки, г |
| `fats` | number \| null | нет | БЖУ: жиры, г |
| `carbs` | number \| null | нет | БЖУ: углеводы, г |
| `source` | enum | да | `text`, `photo_dish`, `photo_product` |
| `request_id` | uuid string | нет | Связь с Запросом (сценарий A) |
| `comment` | string | нет | Пояснение пользователя или LLM |

### Response 201

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "recorded_at": "2026-06-07T12:00:00Z"
}
```

---

## POST /api/v1/events/insulin

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
| `dose` | number | да | Доза в единицах (> 0); **фиксация**, не назначение |
| `food_event_id` | uuid string | нет | Связанный приём пищи |
| `injected_at` | datetime ISO 8601 | нет | По умолчанию — now UTC |
| `comment` | string | нет | Контекст |

### Response 201

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440002",
  "recorded_at": "2026-06-07T11:55:00Z"
}
```

---

## GET /api/v1/events/food (optional MVP)

Список событий питания пользователя.

```
GET /api/v1/events/food?telegram_id=123456789&from=2026-06-01T00:00:00Z&to=2026-06-07T23:59:59Z
```

Response 200: массив объектов (те же поля, что при создании + `id`, `recorded_at`).

**Backlog (post-MVP):** pagination (`page`/`page_size` или cursor); сейчас — голый array без limit.

Реализация — task-05; контракт зафиксирован для клиентов.

## Аутентификация

Как в [assistant-question.md](assistant-question.md): `Authorization: Bearer …`, опционально `X-Request-Id`.

## Ошибки

### POST `/events/food`

| HTTP | Когда |
|------|-------|
| 401 | Нет/неверный token или `telegram_id` |
| 403 | `request_id` принадлежит другому пользователю |
| 404 | `request_id` не найден |
| 422 | отрицательные `xe`/`bje`, неверный `source`, невалидный UUID |
| 503 | PostgreSQL недоступна |

### POST `/events/insulin`

| HTTP | Когда |
|------|-------|
| 401 | Нет/неверный token или `telegram_id` |
| 403 | `food_event_id` принадлежит другому пользователю |
| 404 | `food_event_id` не найден |
| 422 | `dose` ≤ 0, невалидный UUID |
| 503 | PostgreSQL недоступна |

### GET `/events/food`

| HTTP | Когда |
|------|-------|
| 401 | Нет/неверный token или `telegram_id` |
| 422 | невалидный формат `from`/`to` |
| 503 | PostgreSQL недоступна |

## Примеры из idea.md

| Запрос пользователя | API |
|---------------------|-----|
| «Я съел борщ и хлеб — 3.5 ХЕ» | POST `/events/food` после ответа LLM или парсинга |
| «Вколол 4 единицы перед обедом» | POST `/events/insulin` + опционально `food_event_id` |
