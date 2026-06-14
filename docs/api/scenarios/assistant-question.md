# Сценарий A: вопрос ассистенту

Полный контракт: [api-contract.md](../api-contract.md) · Продукт: [idea.md](../../idea.md) · Сущности: Диалог, Запрос · Соглашения: [conventions.md](../conventions.md)

Маппинг на MVP-бот: [handlers.py](../../../src/diaai/handlers.py) — `text_handler`, `photo_handler`.

## Endpoint

```
POST /api/v1/assistant/messages
```

## Аутентификация

| Заголовок | Обязательный | Описание |
|-----------|--------------|----------|
| `Authorization` | да | `Bearer ${BACKEND_SERVICE_TOKEN}` — bot → backend |
| `X-Request-Id` | нет | UUID трассировки; backend генерирует, если не передан |

## Request

Content-Type: `application/json`

### Текстовый вопрос

```json
{
  "telegram_id": 123456789,
  "text": "Сколько ХЕ в борще с хлебом?"
}
```

### Вопрос с фото

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
| `telegram_id` | integer | да | Telegram `chat.id` пользователя |
| `text` | string | условно | Текст вопроса или подпись к фото; min 1 символ, если передан |
| `image_base64` | string | условно | Base64 фото; data-URL префиксы снимаются на backend; лимит 5 MB |
| `image_media_type` | string | нет | По умолчанию `image/jpeg` |

**Правила:**

- Обязателен **либо** непустой `text`, **либо** `image_base64` (можно оба — фото с подписью).
- Пустые `text` и отсутствие `image_base64` → **400** `BAD_REQUEST`.

## Response 200

```json
{
  "dialog_id": "550e8400-e29b-41d4-a716-446655440000",
  "request_id": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
  "reply": "Ориентировочно 3–4 ХЕ…"
}
```

| Поле | Тип | Описание |
|------|-----|----------|
| `dialog_id` | uuid string | Активный диалог (channel=`telegram`) |
| `request_id` | uuid string | Сохранённый Запрос |
| `reply` | string | Ответ ассистента (LLM) |

## Поведение backend

1. Resolve user по `telegram_id` (get-or-create).
2. Get-or-create активный **Диалог** (`channel=telegram`).
3. Загрузить историю диалога (лимит — env `LLM_MAX_HISTORY`, как в боте).
4. Вызвать OpenRouter; сохранить **Запрос** и ответ.
5. При фото — тип запроса `mixed` / `photo`; опционально создать **Анализ фото** (task-05).

## Ошибки

| HTTP | Когда |
|------|-------|
| 401 | Нет/неверный `Authorization` или `telegram_id` |
| 400 | Нет текста и фото |
| 422 | Невалидный JSON, тип полей |
| 404 | Диалог не найден (если передан `dialog_id` в будущих версиях) |
| 502 | OpenRouter недоступен |
| 503 | PostgreSQL недоступна |

## Маппинг bot → API

| Bot | API |
|-----|-----|
| `message.chat.id` | `telegram_id` |
| `message.text` | `text` |
| `message.caption` или дефолт | `text` при фото |
| base64 из `download_file` | `image_base64` |
| `RuntimeError` от LLM | клиент показывает fallback; API → 502 |

`/start` (`CommandStart`) — **вне** этого endpoint; сброс диалога — task-07 (`DELETE /api/v1/dialogs/active` или отдельный контракт).
