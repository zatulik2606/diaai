# Backend Tasklist

Опирается на [plan.md](../plan.md) · [vision.md](../vision.md) · [data-model.md](../data-model.md)

## Обзор

Итерации backend-ядра: персистентность, доменная логика, аналитика и рекомендации.

Детализация этапов из [plan.md](../plan.md): итерации **2** и **4** дорожной карты. Итерация 3 (миграция бота) — в [tasklist-bot.md](tasklist-bot.md); task-10 здесь пересекается с ней.

## Связь с plan.md

| Итерация plan.md | Раздел plan.md | Раздел tasklist | Зависимости |
|------------------|----------------|-----------------|-------------|
| 2 — Backend-ядро и БД | [Итерация 2](../plan.md#итерация-2--backend-ядро-и-бд) | [ниже](#итерация-2-backend-ядро-и-бд-) | итерация 1 ✅ |
| 4 — Аналитика и динамика | [Итерация 4](../plan.md#итерация-4--аналитика-и-динамика-состояния) | [ниже](#итерация-4-аналитика-и-динамика-) | итерации 2, 3 |

Критерии завершения итераций в tasklist согласованы с [plan.md](../plan.md); при расхождении приоритет у plan.md до явного обновления обоих документов.

Обзор всех итераций: [plan.md — Обзор итераций](../plan.md#обзор-итераций).

## Ориентир по последовательности задач

1. Выбор backend-стека и фиксация ключевого архитектурного решения
2. Генерация каркаса / шаблона backend-проекта
3. Проектирование и базовое документирование API-контрактов
4. Реализация API по контрактам с базовыми проверками
5. Подключение хранения и интеграций, если это требуется логикой плана
6. Подготовка backend как единой точки входа для клиентов
7. Актуализация проектной документации и соглашений (vision.md, data-model.md, integrations.md) по факту реализации
8. Команды и сценарии локального запуска всей системы

**Итерация 2** — шаги 1–8: task-01 … task-09; task-10 — рефакторинг бота (логика сейчас в `src/diaai/`: SessionStore, LlmClient, OpenRouter напрямую).  
**Итерация 4** — шаги 3–7 в сокращённом виде.

## Легенда статусов

- 📋 Planned — запланирован
- 🚧 In Progress — в работе
- ✅ Done — завершён

## Итерации

| Итерация | Название | Цель | Статус | Plan | Документы |
|----------|----------|------|--------|------|-----------|
| 2 | Backend-ядро и БД | API, PostgreSQL, базовые сущности | 📋 Planned | [plan §2](../plan.md#итерация-2--backend-ядро-и-бд) | [план](impl/backend/iteration-1-core-db/plan.md) · [summary](impl/backend/iteration-1-core-db/summary.md) |
| 4 | Аналитика и динамика | Прогресс, тренды, рекомендации | 📋 Planned | [plan §4](../plan.md#итерация-4--аналитика-и-динамика-состояния) | [план](impl/backend/iteration-2-analytics/plan.md) · [summary](impl/backend/iteration-2-analytics/summary.md) |

---

## Итерация 2: Backend-ядро и БД 📋

→ [plan.md, итерация 2](../plan.md#итерация-2--backend-ядро-и-бд)

### Цель

Создать единое ядро: API + PostgreSQL + сохранение событий питания и инсулина.

### Ценность

Данные не теряются между сессиями; основа для bot, web и аналитики.

### Критерии завершения

- [ ] backend принимает и возвращает данные через API
- [ ] PostgreSQL: пользователи, диалоги, запросы, события питания/инсулина
- [ ] LLM и анализ фото — через backend
- [ ] бот переведён на backend API (без прямых вызовов LLM и RAM-сессий)
- [ ] миграции БД работают

### Список задач

| Задача | Описание | Шаг | Статус | Документы |
|--------|----------|-----|--------|-----------|
| 01 | Стек backend и ADR | 1 | 📋 Planned | [план](impl/backend/iteration-1-core-db/tasks/task-01-stack-adr/plan.md) · [summary](impl/backend/iteration-1-core-db/tasks/task-01-stack-adr/summary.md) |
| 02 | Каркас backend | 2 | 📋 Planned | [план](impl/backend/iteration-1-core-db/tasks/task-02-scaffold/plan.md) · [summary](impl/backend/iteration-1-core-db/tasks/task-02-scaffold/summary.md) |
| 03 | API-контракты (эндпоинты) | 3 | 📋 Planned | [план](impl/backend/iteration-1-core-db/tasks/task-03-api-contracts/plan.md) · [summary](impl/backend/iteration-1-core-db/tasks/task-03-api-contracts/summary.md) |
| 04 | Соглашения API | 3 | 📋 Planned | [план](impl/backend/iteration-1-core-db/tasks/task-04-api-conventions/plan.md) · [summary](impl/backend/iteration-1-core-db/tasks/task-04-api-conventions/summary.md) |
| 05 | Реализация API | 4 | 📋 Planned | [план](impl/backend/iteration-1-core-db/tasks/task-05-api-impl/plan.md) · [summary](impl/backend/iteration-1-core-db/tasks/task-05-api-impl/summary.md) |
| 06 | PostgreSQL и интеграции | 5 | 📋 Planned | [план](impl/backend/iteration-1-core-db/tasks/task-06-storage-integrations/plan.md) · [summary](impl/backend/iteration-1-core-db/tasks/task-06-storage-integrations/summary.md) |
| 07 | Единая точка входа | 6 | 📋 Planned | [план](impl/backend/iteration-1-core-db/tasks/task-07-entry-point/plan.md) · [summary](impl/backend/iteration-1-core-db/tasks/task-07-entry-point/summary.md) |
| 08 | Актуализация docs | 7 | 📋 Planned | [план](impl/backend/iteration-1-core-db/tasks/task-08-docs-sync/plan.md) · [summary](impl/backend/iteration-1-core-db/tasks/task-08-docs-sync/summary.md) |
| 09 | Локальный запуск | 8 | 📋 Planned | [план](impl/backend/iteration-1-core-db/tasks/task-09-local-run/plan.md) · [summary](impl/backend/iteration-1-core-db/tasks/task-09-local-run/summary.md) |
| 10 | Бот → backend API | — | 📋 Planned | [план](impl/backend/iteration-1-core-db/tasks/task-10-bot-refactor/plan.md) · [summary](impl/backend/iteration-1-core-db/tasks/task-10-bot-refactor/summary.md) |

### Артефакты

- `backend/` — код сервера
- `docs/api/` — контракты и соглашения
- схема БД (миграции)
- ADR: [adr-001-database.md](../adr/adr-001-database.md), adr-002 (стек backend)

### Документы

- 📋 [План](impl/backend/iteration-1-core-db/plan.md)
- 📝 [Summary](impl/backend/iteration-1-core-db/summary.md)

---

### Задача 01: Стек backend и ADR 📋

**Цель:** зафиксировать стек и ADR-002.  
**Состав:** выбор стека, структура `backend/`, uv/ruff/Makefile.  
**Артефакты:** `docs/adr/adr-002-backend-stack.md`

- 📋 [План](impl/backend/iteration-1-core-db/tasks/task-01-stack-adr/plan.md) · 📝 [Summary](impl/backend/iteration-1-core-db/tasks/task-01-stack-adr/summary.md)

---

### Задача 02: Каркас backend 📋

**Цель:** минимальный каркас, готовый к API.  
**Состав:** структура `backend/`, env, health, lint/format.  
**Артефакты:** `backend/`, команды в Makefile

- 📋 [План](impl/backend/iteration-1-core-db/tasks/task-02-scaffold/plan.md) · 📝 [Summary](impl/backend/iteration-1-core-db/tasks/task-02-scaffold/summary.md)

---

### Задача 03: API-контракты (эндпоинты) 📋

**Цель:** описать эндпоинты базовых сущностей.  
**Состав:** users, dialogs, requests, food/insulin events, photo analysis; согласование с [data-model.md](../data-model.md).  
**Артефакты:** `docs/api/` или OpenAPI

- 📋 [План](impl/backend/iteration-1-core-db/tasks/task-03-api-contracts/plan.md) · 📝 [Summary](impl/backend/iteration-1-core-db/tasks/task-03-api-contracts/summary.md)

---

### Задача 04: Соглашения API 📋

**Цель:** единые правила для всех клиентов.  
**Состав:** форматы запросов/ответов, коды и тело ошибок, версионирование API, правила breaking/non-breaking изменений.  
**Артефакты:** раздел в `docs/api/` (conventions)

- 📋 [План](impl/backend/iteration-1-core-db/tasks/task-04-api-conventions/plan.md) · 📝 [Summary](impl/backend/iteration-1-core-db/tasks/task-04-api-conventions/summary.md)

---

### Задача 05: Реализация API 📋

**Цель:** эндпоинты по контрактам task-03 и соглашениям task-04.  
**Состав:** handlers, валидация, smoke-проверки ключевых сценариев.  
**Артефакты:** routes в `backend/`

- 📋 [План](impl/backend/iteration-1-core-db/tasks/task-05-api-impl/plan.md) · 📝 [Summary](impl/backend/iteration-1-core-db/tasks/task-05-api-impl/summary.md)

---

### Задача 06: PostgreSQL и интеграции 📋

**Цель:** персистентность и внешние сервисы.  
**Состав:** миграции, репозитории, OpenRouter через backend; S3 для фото — по необходимости.  
**Артефакты:** миграции, модули интеграций

- 📋 [План](impl/backend/iteration-1-core-db/tasks/task-06-storage-integrations/plan.md) · 📝 [Summary](impl/backend/iteration-1-core-db/tasks/task-06-storage-integrations/summary.md)

---

### Задача 07: Единая точка входа 📋

**Цель:** backend — единый слой для bot и web.  
**Состав:** идентификация пользователя (telegram_id), единая маршрутизация доменных операций.  
**Артефакты:** auth/middleware в `backend/`

- 📋 [План](impl/backend/iteration-1-core-db/tasks/task-07-entry-point/plan.md) · 📝 [Summary](impl/backend/iteration-1-core-db/tasks/task-07-entry-point/summary.md)

---

### Задача 08: Актуализация docs 📋

**Цель:** docs отражают реализацию.  
**Состав:** обновить [vision.md](../vision.md), [data-model.md](../data-model.md), [integrations.md](../integrations.md).  
**Артефакты:** обновлённые docs

- 📋 [План](impl/backend/iteration-1-core-db/tasks/task-08-docs-sync/plan.md) · 📝 [Summary](impl/backend/iteration-1-core-db/tasks/task-08-docs-sync/summary.md)

---

### Задача 09: Локальный запуск 📋

**Цель:** воспроизводимый локальный стенд.  
**Состав:** make-команды, docker-compose (backend + PostgreSQL), инструкция в README.  
**Артефакты:** `docker-compose.yml`, README

- 📋 [План](impl/backend/iteration-1-core-db/tasks/task-09-local-run/plan.md) · 📝 [Summary](impl/backend/iteration-1-core-db/tasks/task-09-local-run/summary.md)

---

### Задача 10: Бот → backend API 📋

**Цель:** убрать дублирование логики из MVP-бота.  
**Состав:** заменить прямые вызовы OpenRouter и SessionStore на backend API; бот — тонкий клиент. Связано с [tasklist-bot.md](tasklist-bot.md), итерация 3.  
**Артефакты:** обновлённый `src/diaai/` или `bot/`, backend-client

- 📋 [План](impl/backend/iteration-1-core-db/tasks/task-10-bot-refactor/plan.md) · 📝 [Summary](impl/backend/iteration-1-core-db/tasks/task-10-bot-refactor/summary.md)

---

## Итерация 4: Аналитика и динамика 📋

→ [plan.md, итерация 4](../plan.md#итерация-4--аналитика-и-динамика-состояния)

### Цель

Агрегировать события, формировать снимки прогресса и справочные рекомендации.

### Ценность

Пользователь видит динамику ХЕ / БЖЕ / БЖУ / инсулина, а не только текущий момент.

### Критерии завершения

- [ ] снимки прогресса за день / неделю / месяц
- [ ] сигналы изменений (улучшение / ухудшение)
- [ ] рекомендации на основе истории (без назначения доз)
- [ ] API для клиентов (bot, web)

### Список задач

| Задача | Описание | Статус | Документы |
|--------|----------|--------|-----------|
| 01 | Контракты аналитики | 📋 Planned | [план](impl/backend/iteration-2-analytics/tasks/task-01-analytics-contracts/plan.md) · [summary](impl/backend/iteration-2-analytics/tasks/task-01-analytics-contracts/summary.md) |
| 02 | Снимки прогресса | 📋 Planned | [план](impl/backend/iteration-2-analytics/tasks/task-02-progress-snapshots/plan.md) · [summary](impl/backend/iteration-2-analytics/tasks/task-02-progress-snapshots/summary.md) |
| 03 | Рекомендации и сигналы | 📋 Planned | [план](impl/backend/iteration-2-analytics/tasks/task-03-recommendations/plan.md) · [summary](impl/backend/iteration-2-analytics/tasks/task-03-recommendations/summary.md) |
| 04 | Docs и запуск | 📋 Planned | [план](impl/backend/iteration-2-analytics/tasks/task-04-docs-and-run/plan.md) · [summary](impl/backend/iteration-2-analytics/tasks/task-04-docs-and-run/summary.md) |

### Артефакты

- модули аналитики в `backend/`
- сущности: Снимок прогресса, Рекомендация (см. [data-model.md](../data-model.md))

### Документы

- 📋 [План](impl/backend/iteration-2-analytics/plan.md)
- 📝 [Summary](impl/backend/iteration-2-analytics/summary.md)

---

### Задача 01: Контракты аналитики 📋

**Цель:** API прогресса и рекомендаций.  
**Состав:** эндпоинты снимков и сигналов; дополнение `docs/api/` по соглашениям task-04.  
**Артефакты:** OpenAPI / `docs/api/`

- 📋 [План](impl/backend/iteration-2-analytics/tasks/task-01-analytics-contracts/plan.md) · 📝 [Summary](impl/backend/iteration-2-analytics/tasks/task-01-analytics-contracts/summary.md)

---

### Задача 02: Снимки прогресса 📋

**Цель:** агрегация и API снимков за день/неделю/месяц.  
**Артефакты:** модуль аналитики, ProgressSnapshot в БД

- 📋 [План](impl/backend/iteration-2-analytics/tasks/task-02-progress-snapshots/plan.md) · 📝 [Summary](impl/backend/iteration-2-analytics/tasks/task-02-progress-snapshots/summary.md)

---

### Задача 03: Рекомендации и сигналы 📋

**Цель:** справочные рекомендации без назначения доз.  
**Артефакты:** модуль рекомендаций, Recommendation в БД

- 📋 [План](impl/backend/iteration-2-analytics/tasks/task-03-recommendations/plan.md) · 📝 [Summary](impl/backend/iteration-2-analytics/tasks/task-03-recommendations/summary.md)

---

### Задача 04: Docs и запуск 📋

**Цель:** docs и локальный стенд с аналитикой актуальны.  
**Состав:** vision/data-model/integrations, проверка make/docker-compose.

- 📋 [План](impl/backend/iteration-2-analytics/tasks/task-04-docs-and-run/plan.md) · 📝 [Summary](impl/backend/iteration-2-analytics/tasks/task-04-docs-and-run/summary.md)

---

## Качество и инженерные практики

Применяются на всех этапах backend, без отдельного backlog:

- **Тесты** — smoke/integration на ключевые API-сценарии; unit там, где есть нетривиальная логика (аналитика, агрегации).
- **Линтеры** — ruff + `make lint` / `make format` для `backend/` (как в MVP-боте).
- **Наблюдаемость** — structured logging (request id, статус, latency); без логирования промптов и персональных данных.
- **Контракты** — изменения через `docs/api/`; breaking changes только с bump версии API (см. task-04); клиенты (bot, web) обновляются в той же итерации.
