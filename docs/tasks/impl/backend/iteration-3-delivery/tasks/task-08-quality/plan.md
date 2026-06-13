# Task 08: Качество и инженерные практики

Опирается на [iteration-3-delivery/plan.md](../../plan.md) · [api-contracts.md](../../../../../../tech/api-contracts.md)

Skills: [fastapi-templates](.agents/skills/fastapi-templates/SKILL.md) — middleware, health endpoints, testing standards

## Цель

Зафиксировать минимальный инженерный стандарт backend на весь цикл.

## Состав работ

### 1. Structured logging

- middleware: log `request_id`, method, path, status, duration_ms
- **не** логировать: Authorization, body text, `image_base64`, промпты
- формат: key=value или JSON (KISS)

### 2. Ruff

- `backend/` в scope `make backend-lint` / `make backend-format`
- align с конфигом бота в `pyproject.toml`

### 3. Exception handlers

- единый `ErrorBody` для app errors ([conventions.md](../../../../../../api/conventions.md))
- 422: по возможности маппинг в понятный формат (tech debt из api-contracts)

### 4. Health (optional)

- `GET /health` → `{ "status": "ok", "version": "1.0.0" }`
- опционально `/health/detailed` — DB ping, degraded → 503 (только если KISS)

### 5. Правила контрактов

- ссылка на [conventions.md#правила-изменений](../../../../../../api/conventions.md#правила-изменений)
- breaking changes → bump API version

### 6. Финальная синхронизация

- [vision.md](../../../../../../vision.md), [plan.md](../../../../../../plan.md)

## Затронутые файлы

- `backend/main.py` (middleware, handlers)
- `Makefile`, `pyproject.toml`
- `docs/vision.md`, `docs/plan.md`

## DoD

| Кто | Критерий |
|-----|----------|
| Агент | `make backend-lint && make backend-test && make backend-run` |
| Пользователь | лог одного запроса — нет токенов и текстов сообщений |

## Следующий шаг

Закрыть [iteration-3-delivery/summary.md](../../summary.md); итерация 4 — аналитика.
