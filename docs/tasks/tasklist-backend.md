# Backend Tasklist

Опирается на [plan.md](../plan.md) · [vision.md](../vision.md) · [data-model.md](../data-model.md) · [idea.md](../idea.md)

## Обзор

Рабочий план реализации backend на [итерации 2 plan.md](../plan.md#итерация-2--backend-ядро-и-бд): вынести логику из MVP-бота в API, два базовых сценария (вопрос ассистенту, фиксация события), затем тонкий клиент.

**Прогресс:** 4 / 8 задач ✅ · **текущая:** task-05 (endpoint impl) · код: [`backend/`](../../backend/)

> **Skills:** на этапах, где уместно, рекомендуй подключать skills. Подбор — на этапах **01** (стек) и **02** (контракты); **03** — `fastapi-templates`; искать через `/find-skills`.

## Итерации backend

Сводный план: [impl/backend/plan.md](impl/backend/plan.md)

| # | Название | Задачи | Статус | Документы |
|---|----------|--------|--------|-----------|
| 1 | Основание | 01–02 | ✅ Done | [plan](impl/backend/iteration-1-foundation/plan.md) · [summary](impl/backend/iteration-1-foundation/summary.md) |
| 2 | Реализация ядра | 03–05 | 🚧 In Progress | [plan](impl/backend/iteration-2-core/plan.md) · [summary](impl/backend/iteration-2-core/summary.md) |
| 3 | Поставка | 06–08 | 📋 Planned | [plan](impl/backend/iteration-3-delivery/plan.md) |

## Связь с plan.md

| plan.md | Tasklist | Зависимости |
|---------|----------|-------------|
| [Итерация 2](../plan.md#итерация-2--backend-ядро-и-бд) | backend итерации 1–3 (задачи 01–08) | итерация 1 plan.md ✅ |
| [Итерация 3](../plan.md#итерация-3--миграция-бота-на-backend) | task-07 + [tasklist-bot.md](tasklist-bot.md) | iteration-2 task-05, iteration-3 task-06 |
| [Итерация 4](../plan.md#итерация-4--аналитика-и-динамика-состояния) | после закрытия backend итерации 2 | итерации 2–3 |

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
| 05 | Endpoint'ы и серверная логика | 🚧 Next | [план](impl/backend/iteration-2-core/tasks/task-05-api-impl/plan.md) · [summary](impl/backend/iteration-2-core/tasks/task-05-api-impl/summary.md) |
| 06 | Документирование backend | 📋 Planned | [план](impl/backend/iteration-3-delivery/tasks/task-06-backend-docs/plan.md) · [summary](impl/backend/iteration-3-delivery/tasks/task-06-backend-docs/summary.md) |
| 07 | Рефакторинг бота → API | 📋 Planned | [план](impl/backend/iteration-3-delivery/tasks/task-07-bot-refactor/plan.md) · [summary](impl/backend/iteration-3-delivery/tasks/task-07-bot-refactor/summary.md) |
| 08 | Качество и инженерные практики | 📋 Planned | [план](impl/backend/iteration-3-delivery/tasks/task-08-quality/plan.md) · [summary](impl/backend/iteration-3-delivery/tasks/task-08-quality/summary.md) |

Задачи выполняются **последовательно** (01 → 08).

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

## Блок 2: Сборка (задачи 03–05) 🚧

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

**Агент:** ✅ `make backend-test` зелёный; 17 тестов; auth/422/400 финальные; happy-path assert 501 (обновить в task-05).

**Пользователь:** ⏳ просмотреть список тестов — понятно, что проверяется до impl.

### Документы

- 📋 [План](impl/backend/iteration-2-core/tasks/task-04-api-tests/plan.md)
- 📝 [Summary](impl/backend/iteration-2-core/tasks/task-04-api-tests/summary.md)

**Проверка блока 2 (после 04):**  
Агент: `make backend-test && make backend-lint`; coverage backend ~99%.  
Пользователь: `pytest backend/tests -v` — матрица auth/validation/assistant/events.

---

## Задача 05: Endpoint'ы и серверная логика 🚧 Next

### Цель

Реализовать основные endpoint'ы по контрактам: LLM, персистентность, интеграции.

### Состав работ

- [ ] Сценарий A: диалог + запрос + вызов OpenRouter через backend
- [ ] Сценарий B: CRUD событий питания/инсулина
- [ ] PostgreSQL: миграции, репозитории ([adr-001](../adr/adr-001-database.md))
- [ ] Идентификация по `telegram_id`
- [ ] Актуализировать [data-model.md](../data-model.md), [integrations.md](../integrations.md)

### Артефакты

- routes/handlers в `backend/`, миграции БД

### Definition of Done

**Агент:** `make backend-test` зелёный; endpoint'ы соответствуют `docs/api/`; данные переживают перезапуск.

**Пользователь:** curl/HTTP-клиент — вопрос и фиксация события возвращают ожидаемые ответы.

### Документы

- 📋 [План](impl/backend/iteration-2-core/tasks/task-05-api-impl/plan.md)
- 📝 [Summary](impl/backend/iteration-2-core/tasks/task-05-api-impl/summary.md)

**Проверка блока 2 (после 05):**  
Агент: `make backend-test && make backend-lint`.  
Пользователь: ручной вызов API для сценариев A и B; проверить запись в БД.

---

## Блок 3: Поставка (задачи 06–08)

→ [iteration-3-delivery](impl/backend/iteration-3-delivery/plan.md)

---

## Задача 06: Документирование backend 📋

### Цель

Задокументировать запуск, конфигурацию и API для разработчиков.

### Состав работ

- [ ] OpenAPI (авто или `docs/api/openapi.yaml`)
- [ ] README: быстрый старт backend
- [ ] Актуализировать: [README.md](../../README.md), [plan.md](../plan.md), `.env.example`
- [ ] docker-compose (backend + PostgreSQL) — при необходимости
- [ ] `make`-команды: install, run, test, migrate, lint — единый набор

### Артефакты

- OpenAPI, README, `docker-compose.yml` (если нужен)

### Definition of Done

**Агент:** новый участник поднимает backend только по README и `.env.example`.

**Пользователь:** следовать README с нуля — backend и БД работают; OpenAPI совпадает с реализацией.

### Документы

- 📋 [План](impl/backend/iteration-3-delivery/tasks/task-06-backend-docs/plan.md)
- 📝 [Summary](impl/backend/iteration-3-delivery/tasks/task-06-backend-docs/summary.md)

---

## Задача 07: Рефакторинг бота → API 📋

### Цель

Перевести MVP-бота на backend API; убрать прямые вызовы LLM и SessionStore.

### Состав работ

- [ ] Backend-client в `src/diaai/`; handlers вызывают API
- [ ] Удалить/обойти прямой OpenRouter и RAM-сессии
- [ ] Актуализировать [vision.md](../vision.md), [README.md](../../README.md), `.env.example`
- [ ] Согласовать с [tasklist-bot.md](tasklist-bot.md), итерация 3

### Артефакты

- обновлённый `src/diaai/`, backend-client

### Definition of Done

**Агент:** бот не импортирует `llm_client` для prod-пути; история в БД через backend.

**Пользователь:** `make run` — бот отвечает на текст и фото как раньше; после перезапуска история сохраняется.

### Документы

- 📋 [План](impl/backend/iteration-3-delivery/tasks/task-07-bot-refactor/plan.md)
- 📝 [Summary](impl/backend/iteration-3-delivery/tasks/task-07-bot-refactor/summary.md)

---

## Задача 08: Качество и инженерные практики 📋

### Цель

Зафиксировать минимальный инженерный стандарт backend на весь цикл.

### Состав работ

- [ ] ruff + `make backend-lint` / `make backend-format` *(каркас task-03 ✅)*
- [ ] Structured logging (request id, status); без промптов и ПДн
- [ ] Правила изменения контрактов в `docs/api/`
- [ ] Финальная актуализация: [vision.md](../vision.md), [plan.md](../plan.md)

### Артефакты

- conventions в `docs/api/`, logging config

### Definition of Done

**Агент:** lint/test/run проходят; логи без секретов; breaking changes только с bump версии API.

**Пользователь:** `make backend-lint && make backend-test`; просмотреть лог одного запроса — нет токенов и текстов сообщений.

### Документы

- 📋 [План](impl/backend/iteration-3-delivery/tasks/task-08-quality/plan.md)
- 📝 [Summary](impl/backend/iteration-3-delivery/tasks/task-08-quality/summary.md)

**Проверка блока 3 (после 08):**  
Агент: полный прогон `make backend-lint`, `make backend-test`, `make backend-run` + `make run`.  
Пользователь: сценарии A и B в Telegram; README — инструкция актуальна.

---

## Итерация 4: Аналитика 📋 (следующий этап)

→ [plan.md, итерация 4](../plan.md#итерация-4--аналитика-и-динамика-состояния)

Детализация — после закрытия задач 01–08. Кратко: снимки прогресса, сигналы, рекомендации ([data-model.md](../data-model.md): ProgressSnapshot, Recommendation).

- 📋 [План](impl/backend/iteration-4-analytics/plan.md) · 📝 [Summary](impl/backend/iteration-4-analytics/summary.md)
