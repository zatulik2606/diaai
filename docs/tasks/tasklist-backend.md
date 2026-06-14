# Backend Tasklist

Опирается на [plan.md](../plan.md) · [vision.md](../vision.md) · [data-model.md](../data-model.md) · [idea.md](../idea.md)

## Обзор

Рабочий план backend: итерации **1–3** ✅ (01–08). Бот — клиент backend API; unit-тесты bot в `tests/`. **Backend delivery complete** — следующий этап: итерация 4 (аналитика).

**Прогресс:** **8 / 12** задач (01–08 ✅) · **`make test`** — 45 (30 backend + 15 bot) · [`backend/README.md`](../../backend/README.md)

> **Skills:** на этапах, где уместно, рекомендуй подключать skills. Подбор — на этапах **01** (стек) и **02** (контракты); **03** — `fastapi-templates`; искать через `/find-skills`.

## Итерации backend

Сводный план: [impl/backend/plan.md](impl/backend/plan.md)

| # | Название | Задачи | Статус | Документы |
|---|----------|--------|--------|-----------|
| 1 | Основание | 01–02 | ✅ Done | [plan](impl/backend/iteration-1-foundation/plan.md) · [summary](impl/backend/iteration-1-foundation/summary.md) |
| 2 | Реализация ядра | 03–05 | ✅ Done | [plan](impl/backend/iteration-2-core/plan.md) · [summary](impl/backend/iteration-2-core/summary.md) |
| 3 | Поставка | 06–08 | ✅ Done | [plan](impl/backend/iteration-3-delivery/plan.md) · [summary](impl/backend/iteration-3-delivery/summary.md) |
| 4 | Аналитика | 09–12 | 📋 Planned | [plan](impl/backend/iteration-4-analytics/plan.md) · [summary](impl/backend/iteration-4-analytics/summary.md) |

## Связь с plan.md

| plan.md | Tasklist | Зависимости |
|---------|----------|-------------|
| [Итерация 2](../plan.md#итерация-2--backend-ядро-и-бд) | backend итерации 1–2 ✅ (01–05) | [iteration-2 summary](impl/backend/iteration-2-core/summary.md) ✅ |
| [Итерация 3](../plan.md#итерация-3--миграция-бота-на-backend) | task-06–08 ✅ + [tasklist-bot.md](tasklist-bot.md) ✅ | [iteration-3 summary](impl/backend/iteration-3-delivery/summary.md) ✅ |
| [Итерация 4](../plan.md#итерация-4--аналитика-и-динамика-состояния) | iteration-4 📋 (09–12) | [iteration-3 summary](impl/backend/iteration-3-delivery/summary.md) ✅ |

## Легенда статусов

- 📋 Planned — запланирован
- 🚧 In Progress / Next — в работе или следующая
- ✅ Done — завершён

## Список задач

| Задача | Описание | Статус | Документы |
|--------|----------|--------|-----------|
| 01 | Стек, ADR, conventions | ✅ Done | [план](impl/backend/iteration-1-foundation/tasks/task-01-stack-adr/plan.md) · [summary](impl/backend/iteration-1-foundation/tasks/task-01-stack-adr/summary.md) |
| 02 | API-контракты (2 сценария) | ✅ Done | [план](impl/backend/iteration-1-foundation/tasks/task-02-api-contracts/plan.md) · [summary](impl/backend/iteration-1-foundation/tasks/task-02-api-contracts/summary.md) |
| 03 | Каркас backend | ✅ Done | [план](impl/backend/iteration-2-core/tasks/task-03-scaffold/plan.md) · [summary](impl/backend/iteration-2-core/tasks/task-03-scaffold/summary.md) |
| 04 | API-тесты сценариев бота | ✅ Done | [план](impl/backend/iteration-2-core/tasks/task-04-api-tests/plan.md) · [summary](impl/backend/iteration-2-core/tasks/task-04-api-tests/summary.md) |
| 05 | Endpoint'ы и серверная логика | ✅ Done | [план](impl/backend/iteration-2-core/tasks/task-05-api-impl/plan.md) · [summary](impl/backend/iteration-2-core/tasks/task-05-api-impl/summary.md) |
| 06 | Документирование backend | ✅ Done | [план](impl/backend/iteration-3-delivery/tasks/task-06-backend-docs/plan.md) · [summary](impl/backend/iteration-3-delivery/tasks/task-06-backend-docs/summary.md) |
| 07 | Рефакторинг бота → API | ✅ Done | [план](impl/backend/iteration-3-delivery/tasks/task-07-bot-refactor/plan.md) · [summary](impl/backend/iteration-3-delivery/tasks/task-07-bot-refactor/summary.md) |
| 08 | Качество и инженерные практики | ✅ Done | [план](impl/backend/iteration-3-delivery/tasks/task-08-quality/plan.md) · [summary](impl/backend/iteration-3-delivery/tasks/task-08-quality/summary.md) |
| 09 | Контракты аналитики | 📋 Planned | [план](impl/backend/iteration-4-analytics/tasks/task-09-analytics-contracts/plan.md) |
| 10 | Снимки прогресса | 📋 Planned | [план](impl/backend/iteration-4-analytics/tasks/task-10-progress-snapshots/plan.md) |
| 11 | Сигналы и рекомендации | 📋 Planned | [план](impl/backend/iteration-4-analytics/tasks/task-11-recommendations-signals/plan.md) |
| 12 | Тесты и документация | 📋 Planned | [план](impl/backend/iteration-4-analytics/tasks/task-12-docs-and-quality/plan.md) |

Задачи выполняются **последовательно** (01 → 12). Итерации **1–3** закрыты ✅; **4** — следующая.

---

## Блок 1: Основание (задачи 01–02) ✅

→ [iteration-1-foundation](impl/backend/iteration-1-foundation/plan.md)

---

## Задача 01: Стек, ADR, conventions ✅

### Цель

Выбрать backend-стек, зафиксировать решение в ADR и обновить соглашения проекта.

### Состав работ

- [x] Сравнить варианты стека; оформить `docs/adr/adr-002-backend-stack.md`
- [x] Обновить [.cursor/rules/conventions.mdc](../../.cursor/rules/conventions.mdc) под backend
- [x] Актуализировать [vision.md](../vision.md), [plan.md](../plan.md) — стек и структура `backend/`
- [x] Skills: `fastapi-templates`, `api-design-principles` (см. summary)

### Артефакты

- `docs/adr/adr-002-backend-stack.md`
- `.cursor/rules/conventions.mdc`

### Definition of Done

**Агент:** ADR принят; conventions отражают структуру `backend/`, инструменты (uv, ruff, make); vision и plan согласованы.

**Пользователь:** прочитать ADR-002 и conventions.mdc — понятно, почему выбран стек и как устроен backend.

### Документы

- 📋 [План](impl/backend/iteration-1-foundation/tasks/task-01-stack-adr/plan.md)
- 📝 [Summary](impl/backend/iteration-1-foundation/tasks/task-01-stack-adr/summary.md)

**Проверка блока 1 (после 01):**  
Агент: `make lint` проходит для затронутых файлов.  
Пользователь: открыть ADR-002 и conventions.mdc.

---

## Задача 02: API-контракты (2 сценария) ✅

### Цель

Спроектировать контракты для двух MVP-сценариев, уже работающих в боте.

### Состав работ

- [x] **Сценарий A — вопрос ассистенту:** [assistant-question.md](../api/scenarios/assistant-question.md)
- [x] **Сценарий B — фиксация события:** [event-record.md](../api/scenarios/event-record.md)
- [x] Соглашения — [conventions.md](../api/conventions.md), [openapi.yaml](../api/openapi.yaml)
- [x] Актуализировать [data-model.md](../data-model.md), [integrations.md](../integrations.md)
- [x] Post-review: [api-contracts.md](../tech/api-contracts.md), [backend-structure.md](../tech/backend-structure.md)
- [x] Skills: `api-design-principles`, `fastapi-templates` (task-03+)

### Артефакты

- `docs/api/` — контракты и conventions

### Definition of Done

**Агент:** оба сценария описаны (эндпоинты, схемы, ошибки); data-model и integrations согласованы.

**Пользователь:** по `docs/api/` понятно, как бот вызовет «вопрос» и «фиксацию»; сценарии соответствуют [idea.md](../idea.md).

### Документы

- 📋 [План](impl/backend/iteration-1-foundation/tasks/task-02-api-contracts/plan.md)
- 📝 [Summary](impl/backend/iteration-1-foundation/tasks/task-02-api-contracts/summary.md)

**Проверка блока 1 (после 02):**  
Агент: контракты покрывают handlers бота (`src/diaai/handlers.py`).  
Пользователь: открыть `docs/api/`, сверить с двумя сценариями в Telegram.

---

## Блок 2: Сборка (задачи 03–05) ✅

→ [iteration-2-core](impl/backend/iteration-2-core/plan.md) · [summary](impl/backend/iteration-2-core/summary.md)

---

## Задача 03: Каркас backend ✅

### Цель

Поднять backend-сервис с API-скелетом по [ADR-002](../adr/adr-002-backend-stack.md) и контрактам task-02 — готов к task-04 (тесты) и task-05 (impl).

> Skills: [api-design-principles](.agents/skills/api-design-principles/SKILL.md) · [fastapi-templates](.agents/skills/fastapi-templates/SKILL.md)

### Состав работ

**Инфраструктура**
- [x] Структура `backend/` по ADR-002; `config.py` (pydantic-settings)
- [x] Запуск: `uvicorn backend.main:app`; пакет `backend` в `pyproject.toml`
- [x] `GET /health` (без auth); `make`: `backend-install`, `backend-run`, `backend-lint`, `backend-format`
- [x] `.env.example` — `BACKEND_SERVICE_TOKEN`, `BACKEND_HOST`, `BACKEND_PORT`, заготовки под БД/LLM
- [x] `pyproject.toml`: fastapi, uvicorn, pydantic-settings; dev: **httpx**, pytest, pytest-asyncio

**API-скелет (contract-first)**
- [x] Роутеры `api/v1/`: `assistant`, `events` — **async** handlers; stub `501` до task-05
- [x] Pydantic-схемы в `schemas/` по контрактам task-02
- [x] Dependency `verify_service_token` — `Authorization: Bearer` (кроме `/health`)
- [x] Exception handlers → формат `{ "error": { "code", "message", "details" } }`
- [x] Lifespan в `main.py` — placeholder под БД (task-05)
- [x] Middleware `X-Request-Id` — async, трассировка в логах
- [x] OpenAPI: `/docs` согласован с [openapi.yaml](../api/openapi.yaml)

**Задел под тесты (task-04)**
- [x] `backend/tests/conftest.py` — `AsyncClient`, fixture `app`, auth headers
- [x] Smoke: `test_health.py`, `test_auth.py`

### Артефакты

- `backend/` — см. [backend-structure.md](../tech/backend-structure.md)
- `Makefile`, `.env.example`, `pyproject.toml`

### Definition of Done

**Агент:** `make backend-run` → `/health` 200; `/docs` v1 paths; no token → 401; `pytest backend/tests/test_health.py` OK; lint/format OK.

**Пользователь:** `make backend-run`, открыть `/docs` — endpoint'ы assistant/events на месте; `/health` отвечает.

### Документы

- 📋 [План](impl/backend/iteration-2-core/tasks/task-03-scaffold/plan.md)
- 📝 [Summary](impl/backend/iteration-2-core/tasks/task-03-scaffold/summary.md)

**Проверка блока 2 (после 03):**  
Агент: `curl /health`; `curl /api/v1/...` без Bearer → 401.  
Пользователь: Swagger `/docs` совпадает с [openapi.yaml](../api/openapi.yaml).

---

## Задача 04: API-тесты сценариев бота ✅

### Цель

Базовые тесты API для сценариев A и B на каркасе task-03 (routes, auth, errors).

### Состав работ

- [x] Тесты auth: без Bearer → 401; невалидный Bearer → 401
- [x] Тесты validation: невалидное тело → 422
- [x] Тесты сценария A: text/photo → 501; пустой контент → 400
- [x] Тесты сценария B: food/insulin/list → 501
- [x] `make backend-test` в Makefile (17 тестов)

### Артефакты

- `backend/tests/conftest.py` — fixtures auth/payloads
- `backend/tests/test_auth.py`, `test_validation.py`, `test_assistant.py`, `test_events.py`
- `backend/tests/test_health.py` — smoke (дубль health в test_auth)

### Definition of Done

**Агент:** ✅ `make backend-test` зелёный; 17 тестов; auth/422/400 финальные; happy-path 501 → обновлено в task-05.

**Пользователь:** ✅ список тестов понятен; impl в task-05.

### Документы

- 📋 [План](impl/backend/iteration-2-core/tasks/task-04-api-tests/plan.md)
- 📝 [Summary](impl/backend/iteration-2-core/tasks/task-04-api-tests/summary.md)

**Проверка блока 2 (после 04):**  
Агент: `make backend-test && make backend-lint`; coverage backend ~99%.  
Пользователь: `pytest backend/tests -v` — матрица auth/validation/assistant/events.

---

## Задача 05: Endpoint'ы и серверная логика ✅

### Цель

Реализовать основные endpoint'ы по контрактам: LLM, персистентность, интеграции.

### Состав работ

- [x] Сценарий A: диалог + запрос + OpenRouter через backend
- [x] Сценарий B: CRUD событий питания/инсулина + GET list
- [x] PostgreSQL: Alembic, ORM, repositories
- [x] Идентификация по `telegram_id`
- [x] Обновлены contract tests (**21**); domain 403/404
- [x] `docker-compose.yml` (PG :5433), `make backend-migrate`
- [x] [data-model.md](../data-model.md) — SQL-схема MVP

### Артефакты

- `backend/` — services, repositories, models, Alembic
- `docker-compose.yml`, `alembic/`

### Definition of Done

**Агент:** ✅ `make backend-test` (21); endpoint'ы по `docs/api/`.

**Пользователь:** ✅ curl A/B; assistant 200, events 201; PG persistence.

### Документы

- 📋 [План](impl/backend/iteration-2-core/tasks/task-05-api-impl/plan.md)
- 📝 [Summary](impl/backend/iteration-2-core/tasks/task-05-api-impl/summary.md)

**Проверка блока 2 (после 05):**  
Агент: `docker compose up -d && make backend-migrate && make backend-test` — ✅  
Пользователь: curl assistant/food — ✅ · [iteration-2 summary](impl/backend/iteration-2-core/summary.md)

---

## Блок 3: Поставка (задачи 06–08) ✅

→ [iteration-3-delivery/plan.md](impl/backend/iteration-3-delivery/plan.md) · [summary](impl/backend/iteration-3-delivery/summary.md)

**Прогресс блока:** 3 / 3 ✅

---

## Задача 06: Документирование backend ✅

### Цель

Задокументировать запуск, конфигурацию и API для разработчиков.

### Состав работ

- [x] `backend/README.md` — quick start, env, curl, troubleshooting
- [x] OpenAPI sync: paths совпадают; `make backend-openapi-export` для diff
- [x] docker-compose: healthcheck PostgreSQL, комментарии (порт 5433)
- [x] Актуализировать: [README.md](../../README.md), [plan.md](../plan.md), [docs/api/README.md](../api/README.md), `.env.example`
- [x] docker-compose PostgreSQL
- [x] `make backend-migrate`, `backend-run`, `backend-test`, `backend-lint`, `backend-openapi-export`

### Артефакты

- [`backend/README.md`](../../backend/README.md), OpenAPI yaml, `docker-compose.yml`

### Definition of Done

**Агент:** ✅ новый участник поднимает backend только по README и `.env.example`.

**Пользователь:** ✅ следовать README с нуля — backend и БД работают; OpenAPI совпадает с реализацией.

### Документы

- 📋 [План](impl/backend/iteration-3-delivery/tasks/task-06-backend-docs/plan.md)
- 📝 [Summary](impl/backend/iteration-3-delivery/tasks/task-06-backend-docs/summary.md)

**Проверка блока 3 (после 06):**  
Агент: `make backend-test` (30), `make backend-lint` — ✅  
Пользователь: онбординг по [`backend/README.md`](../../backend/README.md) — ✅

---

## Задача 07: Рефакторинг бота → API ✅

### Цель

Перевести MVP-бота на backend API; убрать прямые вызовы LLM и SessionStore.

### Состав работ

- [x] Backend-client в `src/diaai/backend_client.py`; handlers вызывают API
- [x] Prod-путь без `LlmClient` и `SessionStore`
- [x] Unit-тесты: `tests/test_backend_client.py`, `tests/test_config.py`; `make test` (45)
- [x] Актуализировать [vision.md](../vision.md), [README.md](../../README.md), `.env.example`
- [x] Согласовать с [tasklist-bot.md](tasklist-bot.md), итерация 3 ✅

### Артефакты

- `src/diaai/backend_client.py`, handlers/main/bot/config, `tests/`, `make test`

### Definition of Done

**Агент:** ✅ prod-путь без `llm_client`; `make lint`, `make test` (45), `make backend-test` (30).

**Пользователь:** ✅ `make run` + backend — текст/фото в Telegram; история в PG после перезапуска бота.

### Документы

- 📋 [План](impl/backend/iteration-3-delivery/tasks/task-07-bot-refactor/plan.md)
- 📝 [Summary](impl/backend/iteration-3-delivery/tasks/task-07-bot-refactor/summary.md)

**Проверка блока 3 (после 07):**  
Агент: `make lint` ✅ · `make test` (45) ✅  
Пользователь: backend + bot up; Telegram text/photo; история после restart бота

---

## Задача 08: Качество и инженерные практики ✅

### Цель

Зафиксировать минимальный инженерный стандарт backend на весь цикл.

### Состав работ

- [x] ruff + `make lint` / `make test` *(45: 30 backend + 15 bot)*
- [x] Structured logging (request id, status, `telegram_id`, размеры); без промптов и ПДн
- [x] Правила изменения контрактов в `docs/api/`
- [x] Финальная актуализация: README, api-contracts, `/health` + version
- [x] Post-audit: secure token, async LLM, `image_base64` limits + data-URL strip

### Артефакты

- conventions в `docs/api/`, logging config

### Definition of Done

**Агент:** lint/test/run проходят; логи без секретов; breaking changes только с bump версии API.

**Пользователь:** `make lint && make test`; просмотреть лог одного запроса — нет токенов и текстов сообщений.

### Документы

- 📋 [План](impl/backend/iteration-3-delivery/tasks/task-08-quality/plan.md)
- 📝 [Summary](impl/backend/iteration-3-delivery/tasks/task-08-quality/summary.md)

**Проверка блока 3 (после 08):**  
Агент: `make lint`, `make test` (45), `make backend-run` + `make run`; логи без секретов.  
Пользователь: сценарий A в Telegram; README актуален; [iteration-3 summary](impl/backend/iteration-3-delivery/summary.md) ✅.

---

## Блок 4: Аналитика (задачи 09–12) 📋

→ [iteration-4-analytics/plan.md](impl/backend/iteration-4-analytics/plan.md) · [summary](impl/backend/iteration-4-analytics/summary.md)

**Прогресс блока:** 0 / 4

---

## Итерация 4: Аналитика 📋 (следующий этап)

→ [plan.md, итерация 4](../plan.md#итерация-4--аналитика-и-динамика-состояния) · [iteration-4 plan](impl/backend/iteration-4-analytics/plan.md)

Снимки прогресса, сигналы изменений, справочные рекомендации ([data-model.md](../data-model.md): ProgressSnapshot, Recommendation).

| Задача | Описание | Статус | Документы |
|--------|----------|--------|-----------|
| 09 | Контракты аналитики | 📋 Planned | [план](impl/backend/iteration-4-analytics/tasks/task-09-analytics-contracts/plan.md) |
| 10 | Снимки прогресса | 📋 Planned | [план](impl/backend/iteration-4-analytics/tasks/task-10-progress-snapshots/plan.md) |
| 11 | Сигналы и рекомендации | 📋 Planned | [план](impl/backend/iteration-4-analytics/tasks/task-11-recommendations-signals/plan.md) |
| 12 | Тесты и документация | 📋 Planned | [план](impl/backend/iteration-4-analytics/tasks/task-12-docs-and-quality/plan.md) |

- 📋 [План итерации](impl/backend/iteration-4-analytics/plan.md) · 📝 [Summary](impl/backend/iteration-4-analytics/summary.md)
- Сводка области: [impl/backend/summary.md](impl/backend/summary.md) ✅ (01–08)
