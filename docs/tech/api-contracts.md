# API-контракты diaai (v1)

Сводка REST API backend для MVP. **Полный контракт:** [`docs/api/api-contract.md`](../api/api-contract.md). Детали — в [`docs/api/`](../api/).

Опирается на [ADR-002](../adr/adr-002-backend-stack.md) · [data-model.md](../data-model.md) · [integrations.md](../integrations.md).

## Назначение и scope

- **Версия:** v1 (`/api/v1/…`)
- **Клиент MVP:** Telegram-бот → backend (service token); Next.js BFF → web routes
- **Сценарии:** A — вопрос ассистенту; B — фиксация питания и инсулина; C — analytics (D3/D4); Web — dashboard, leaderboard, auth, history
- **Analytics REST:** `/api/v1/analytics/*` — ✅ impl (iter 4). Web dashboard — `/api/v1/web/*` ✅
- **Вне scope v1:** JWT/web-session на backend, CRUD консультаций

## Базовый URL и версионирование

| Параметр | Значение |
|----------|----------|
| Префикс | `/api/v1/` |
| Breaking changes | только `/api/v2/` |
| Non-breaking | новые optional-поля, новые endpoint'ы в v1 |

Подробнее: [conventions.md](../api/conventions.md#версионирование).

## Карта endpoint'ов

| Method | Path | Назначение | Success | Auth |
|--------|------|------------|---------|------|
| GET | `/health` | health check | 200 | нет |
| POST | `/api/v1/assistant/messages` | сценарий A — вопрос ассистенту | 200 | Bearer |
| POST | `/api/v1/media/transcribe` | STT: audio → text (bot voice, web fallback) | 200 | Bearer |
| POST | `/api/v1/web/analytics/query` | NL → read-only SQL → answer + rows (iter 9) | 200 | Bearer |
| POST | `/api/v1/events/food` | создать событие питания | 201 | Bearer |
| GET | `/api/v1/events/food` | список событий питания (optional MVP) | 200 | Bearer |
| POST | `/api/v1/events/insulin` | создать событие инсулина | 201 | Bearer |
| GET | `/api/v1/analytics/progress` | D3 — снимок прогресса | 200 | Bearer |
| GET | `/api/v1/analytics/signals` | D3 — сигналы изменений | 200 | Bearer |
| GET | `/api/v1/analytics/recommendations` | D4 — рекомендации | 200 | Bearer |
| POST | `/api/v1/web/auth/resolve` | username → user (web login) | 200 | Bearer |
| GET | `/api/v1/web/patient/dashboard/*` | KPI, activity, questions, submissions, matrix | 200 | Bearer |
| GET | `/api/v1/web/doctor/dashboard/*` | KPI, activity, questions, submissions, matrix | 200 | Bearer |
| GET | `/api/v1/web/leaderboard` | рейтинг + scatter | 200 | Bearer |
| GET | `/api/v1/web/assistant/history` | история FAB-чата | 200 | Bearer |

Web DTO: [frontend-contract.md](../api/frontend-contract.md).

## Cross-cutting

### Аутентификация

| Механизм | Описание |
|----------|----------|
| `Authorization: Bearer <token>` | Service token bot → backend (`BACKEND_SERVICE_TOKEN`) |
| `telegram_id` | В теле POST или query GET; маппинг на Telegram `chat.id` |

### Заголовки

| Заголовок | Обязательный | Описание |
|-----------|--------------|----------|
| `Authorization` | да (кроме `/health`) | Bearer service token |
| `X-Request-Id` | нет | UUID трассировки |
| `Content-Type` | да для POST | `application/json` |

### Именование JSON

- Поля: `snake_case`
- UUID: RFC 4122 string
- Время: ISO 8601 UTC (`…Z`)
- Домен: `xe` (ХЕ), `bje` (БЖЕ) — [data-model.md](../data-model.md#api-поля-v1)

### Формат ошибок

Единое тело `ErrorBody` для 4xx/5xx (кроме 422 — допускается FastAPI `detail`). См. [conventions.md](../api/conventions.md#формат-ошибки).

## Сценарии

| Сценарий | Endpoint | Документ |
|----------|----------|----------|
| A — вопрос ассистенту | `POST /api/v1/assistant/messages` | [assistant-question.md](../api/scenarios/assistant-question.md) |
| B — фиксация события | `POST /api/v1/events/food`, `/events/insulin` | [event-record.md](../api/scenarios/event-record.md) |

**Сценарий A:** текст или фото → LLM (OpenRouter) → ответ + сохранение Запроса в диалоге.

**Сценарий B:** структурированная запись ХЕ/БЖЕ и дозы инсулина в PostgreSQL.

## MVP-ограничения и backlog

| Тема | Статус v1 | Backlog |
|------|-----------|---------|
| Pagination (`GET /events/food`) | голый array, без limit | `page`/`page_size` или cursor |
| Rate limiting | не реализовано | 429 + `Retry-After` |
| Idempotency keys | нет | `Idempotency-Key` для POST events |
| `telegram_id` в query (GET) | допустимо на MVP | header или nested resource в v2 |
| `POST /assistant/messages` → 200 | осознанно (см. Design review) | 201 + `Location` post-MVP |
| Единый формат 422 | dual format (FastAPI `detail`) | deferred post-MVP; см. conventions |

## Design review (api-design-principles)

Проверка по [api-design-checklist](../../.agents/skills/api-design-principles/assets/api-design-checklist.md) · [rest-best-practices](../../.agents/skills/api-design-principles/references/rest-best-practices.md).

### Pass

| Критерий | Обоснование |
|----------|-------------|
| URL versioning | `/api/v1/` во всех path |
| Ресурсы — существительные | `/events/food`, `/events/insulin`; nesting ≤ 2 уровня |
| HTTP-методы | GET — чтение; POST — создание; 201 для events |
| Коды ошибок | 400/401/403/404/422/502/503 в conventions |
| Единый формат ошибок | `ErrorBody` в OpenAPI + conventions |
| Auth | Bearer token; 401 vs 403 разведены |
| Документация | scenarios + OpenAPI 3.1 + примеры JSON |
| Health | `GET /health` без auth; `status` + `version` |
| Structured request logging | middleware key=value; без body/tokens |

### Warn (зафиксировано, не блокирует MVP)

| Критерий | Наблюдение | Решение v1 |
|----------|------------|------------|
| POST `/assistant/messages` → 200 | создаётся `Request`, не новый ресурс top-level | 200 — ответ диалога; post-MVP: 201 + `Location` |
| 401 за отсутствие `telegram_id` | по REST чаще 422 | MVP: bot всегда передаёт id; пересмотр в v2 |
| 422 dual format | FastAPI `detail` vs `ErrorBody` | deferred post-MVP (task-08) |
| GET list без pagination | массив без metadata | optional MVP; pagination в backlog |
| `telegram_id` в query | риск access-логов | backlog v2 |
| `image_base64` | лимит в conventions (5 MB рекомендация) | 413 зарезервирован |
| Rate limiting | defer | post-MVP |
| Idempotency keys | defer | риск дублей при retry bot |

### Fix (устранено в этом ревью)

| Проблема | Исправление |
|----------|-------------|
| 404 для assistant отсутствовал в OpenAPI | добавлен в `openapi.yaml` |
| 403 для food POST при чужом `request_id` | синхронизированы scenario + OpenAPI |
| 422 для GET food (invalid `from`/`to`) | добавлен в scenario + OpenAPI |
| Лимит `image_base64` не описан | добавлен в conventions |

## Contract tests (task-04–08 ✅)

Реализация: `backend/tests/` + `tests/` — **109** тестов (`make test`: 92 backend + 17 bot).

| Группа | Файл | Коды |
|--------|------|------|
| Auth | `test_auth.py` | 401, health 200 + version |
| Validation | `test_validation.py` | 422 |
| Сценарий A | `test_assistant.py` | 200, 400, headers |
| Media STT | `test_media_transcribe.py` | 200, 401, 422 |
| Analytics query | `test_analytics_query.py` | golden 3, guardrails, 401, 422 |
| Analytics REST | `test_analytics_api.py` | progress, signals, recommendations; 401, 403, 422 |
| Сценарий B | `test_events.py`, `test_events_domain.py` | 201/200, 403/404 |
| Web API | `test_web_api.py` | 200 auth/dashboard/leaderboard/history; 403 non-doctor; 404 auth |

## Связанные документы

| Документ | Содержание |
|----------|------------|
| [docs/api/api-contract.md](../api/api-contract.md) | **API-контракт v1** — endpoint'ы, схемы, примеры |
| [docs/api/README.md](../api/README.md) | индекс API |
| [conventions.md](../api/conventions.md) | коды ошибок, auth, правила изменений |
| [openapi.yaml](../api/openapi.yaml) | OpenAPI 3.1 |
| [tasklist-backend.md](../tasks/tasklist-backend.md) | task-02 … task-12 ✅ |
| [backend-structure.md](backend-structure.md) | структура FastAPI backend, design review |
