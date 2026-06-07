# Backend Tasklist

Опирается на [plan.md](../plan.md) · [vision.md](../vision.md) · [data-model.md](../data-model.md)

## Обзор

Backend-область: персистентность, API, интеграции, аналитика.  
[plan.md, итерация 2](../plan.md#итерация-2--backend-ядро-и-бд) декомпозирована на под-итерации **2.1–2.9** (шаги 1–8 + рефакторинг бота).  
[plan.md, итерация 4](../plan.md#итерация-4--аналитика-и-динамика-состояния) — аналитика ниже.

## Связь с plan.md

| plan.md | Backend tasklist | Зависимости |
|---------|----------------|-------------|
| Итерация 2 | [2.1–2.9](#итерации) | итерация 1 ✅ |
| Итерация 4 | [4 — Аналитика](#итерация-4-аналитика-и-динамика-) | 2.9, [bot §3](tasklist-bot.md) |

Критерии — в [plan.md](../plan.md); при расхождении приоритет у plan.md.

## Легенда статусов

- 📋 Planned — запланирован
- 🚧 In Progress — в работе
- ✅ Done — завершён

## Итерации

| ID | Название | Шаг | Plan | Статус | Документы |
|----|----------|-----|------|--------|-----------|
| 2.1 | Стек backend и ADR | 1 | [§2](../plan.md#итерация-2--backend-ядро-и-бд) | 📋 Planned | [план](impl/backend/iteration-1-stack-adr/plan.md) · [summary](impl/backend/iteration-1-stack-adr/summary.md) |
| 2.2 | Каркас backend | 2 | [§2](../plan.md#итерация-2--backend-ядро-и-бд) | 📋 Planned | [план](impl/backend/iteration-2-scaffold/plan.md) · [summary](impl/backend/iteration-2-scaffold/summary.md) |
| 2.3 | API-контракты | 3 | [§2](../plan.md#итерация-2--backend-ядро-и-бд) | 📋 Planned | [план](impl/backend/iteration-3-api-contracts/plan.md) · [summary](impl/backend/iteration-3-api-contracts/summary.md) |
| 2.4 | Реализация API | 4 | [§2](../plan.md#итерация-2--backend-ядро-и-бд) | 📋 Planned | [план](impl/backend/iteration-4-api-impl/plan.md) · [summary](impl/backend/iteration-4-api-impl/summary.md) |
| 2.5 | Хранение и интеграции | 5 | [§2](../plan.md#итерация-2--backend-ядро-и-бд) | 📋 Planned | [план](impl/backend/iteration-5-storage-integrations/plan.md) · [summary](impl/backend/iteration-5-storage-integrations/summary.md) |
| 2.6 | Единая точка входа | 6 | [§2](../plan.md#итерация-2--backend-ядро-и-бд) | 📋 Planned | [план](impl/backend/iteration-6-entry-point/plan.md) · [summary](impl/backend/iteration-6-entry-point/summary.md) |
| 2.7 | Актуализация документации | 7 | [§2](../plan.md#итерация-2--backend-ядро-и-бд) | 📋 Planned | [план](impl/backend/iteration-7-docs-sync/plan.md) · [summary](impl/backend/iteration-7-docs-sync/summary.md) |
| 2.8 | Локальный запуск | 8 | [§2](../plan.md#итерация-2--backend-ядро-и-бд) | 📋 Planned | [план](impl/backend/iteration-8-local-run/plan.md) · [summary](impl/backend/iteration-8-local-run/summary.md) |
| 2.9 | Бот → backend API | — | [§2](../plan.md#итерация-2--backend-ядро-и-бд) · [§3](tasklist-bot.md) | 📋 Planned | [план](impl/backend/iteration-9-bot-refactor/plan.md) · [summary](impl/backend/iteration-9-bot-refactor/summary.md) |
| 4 | Аналитика и динамика | — | [§4](../plan.md#итерация-4--аналитика-и-динамика-состояния) | 📋 Planned | [план](impl/backend/iteration-10-analytics/plan.md) · [summary](impl/backend/iteration-10-analytics/summary.md) |

Под-итерации 2.1–2.8 выполняются **последовательно**. 2.9 — после 2.4–2.6; связана с [tasklist-bot.md](tasklist-bot.md), итерация 3.

---

## Итерация 2.1: Стек backend и ADR 📋

**Шаг 1.** Выбор backend-стека и фиксация ключевого архитектурного решения.

| Задача | Описание | Статус | Документы |
|--------|----------|--------|-----------|
| 01 | ADR-002, структура `backend/`, uv/ruff/Makefile | 📋 Planned | [план](impl/backend/iteration-1-stack-adr/tasks/task-01-stack-adr/plan.md) · [summary](impl/backend/iteration-1-stack-adr/tasks/task-01-stack-adr/summary.md) |

**Артефакты:** `docs/adr/adr-002-backend-stack.md`

---

## Итерация 2.2: Каркас backend 📋

**Шаг 2.** Генерация каркаса / шаблона backend-проекта.

| Задача | Описание | Статус | Документы |
|--------|----------|--------|-----------|
| 01 | Структура `backend/`, env, health, lint/format | 📋 Planned | [план](impl/backend/iteration-2-scaffold/tasks/task-01-scaffold/plan.md) · [summary](impl/backend/iteration-2-scaffold/tasks/task-01-scaffold/summary.md) |

**Артефакты:** `backend/`, команды в Makefile

---

## Итерация 2.3: API-контракты 📋

**Шаг 3.** Проектирование и базовое документирование API-контрактов.

| Задача | Описание | Статус | Документы |
|--------|----------|--------|-----------|
| 01 | Эндпоинты: users, dialogs, events, photo analysis | 📋 Planned | [план](impl/backend/iteration-3-api-contracts/tasks/task-01-endpoints/plan.md) · [summary](impl/backend/iteration-3-api-contracts/tasks/task-01-endpoints/summary.md) |
| 02 | Соглашения: форматы, коды ошибок, версионирование | 📋 Planned | [план](impl/backend/iteration-3-api-contracts/tasks/task-02-conventions/plan.md) · [summary](impl/backend/iteration-3-api-contracts/tasks/task-02-conventions/summary.md) |

**Артефакты:** `docs/api/`

---

## Итерация 2.4: Реализация API 📋

**Шаг 4.** Реализация API по контрактам с базовыми проверками.

| Задача | Описание | Статус | Документы |
|--------|----------|--------|-----------|
| 01 | Handlers, валидация, smoke-проверки | 📋 Planned | [план](impl/backend/iteration-4-api-impl/tasks/task-01-api-impl/plan.md) · [summary](impl/backend/iteration-4-api-impl/tasks/task-01-api-impl/summary.md) |

**Артефакты:** routes в `backend/`

---

## Итерация 2.5: Хранение и интеграции 📋

**Шаг 5.** Подключение хранения и интеграций, если это требуется логикой плана.

| Задача | Описание | Статус | Документы |
|--------|----------|--------|-----------|
| 01 | PostgreSQL, миграции, репозитории | 📋 Planned | [план](impl/backend/iteration-5-storage-integrations/tasks/task-01-postgresql/plan.md) · [summary](impl/backend/iteration-5-storage-integrations/tasks/task-01-postgresql/summary.md) |
| 02 | OpenRouter через backend; S3 — по необходимости | 📋 Planned | [план](impl/backend/iteration-5-storage-integrations/tasks/task-02-integrations/plan.md) · [summary](impl/backend/iteration-5-storage-integrations/tasks/task-02-integrations/summary.md) |

**Артефакты:** миграции, [adr-001](../adr/adr-001-database.md)

---

## Итерация 2.6: Единая точка входа 📋

**Шаг 6.** Подготовка backend как единой точки входа для клиентов.

| Задача | Описание | Статус | Документы |
|--------|----------|--------|-----------|
| 01 | Идентификация (telegram_id), единая маршрутизация | 📋 Planned | [план](impl/backend/iteration-6-entry-point/tasks/task-01-entry-point/plan.md) · [summary](impl/backend/iteration-6-entry-point/tasks/task-01-entry-point/summary.md) |

**Артефакты:** auth/middleware в `backend/`

---

## Итерация 2.7: Актуализация документации 📋

**Шаг 7.** Актуализация проектной документации и соглашений по факту реализации.

| Задача | Описание | Статус | Документы |
|--------|----------|--------|-----------|
| 01 | vision.md, data-model.md, integrations.md | 📋 Planned | [план](impl/backend/iteration-7-docs-sync/tasks/task-01-docs-sync/plan.md) · [summary](impl/backend/iteration-7-docs-sync/tasks/task-01-docs-sync/summary.md) |

---

## Итерация 2.8: Локальный запуск 📋

**Шаг 8.** Команды и сценарии локального запуска всей системы.

| Задача | Описание | Статус | Документы |
|--------|----------|--------|-----------|
| 01 | make-команды, docker-compose, README | 📋 Planned | [план](impl/backend/iteration-8-local-run/tasks/task-01-local-run/plan.md) · [summary](impl/backend/iteration-8-local-run/tasks/task-01-local-run/summary.md) |

**Артефакты:** `docker-compose.yml`, README

---

## Итерация 2.9: Бот → backend API 📋

Логика MVP сейчас в `src/diaai/` (SessionStore, LlmClient, OpenRouter). Рефакторинг после готовности API.

| Задача | Описание | Статус | Документы |
|--------|----------|--------|-----------|
| 01 | Бот — тонкий клиент backend API | 📋 Planned | [план](impl/backend/iteration-9-bot-refactor/tasks/task-01-bot-refactor/plan.md) · [summary](impl/backend/iteration-9-bot-refactor/tasks/task-01-bot-refactor/summary.md) |

Связано: [tasklist-bot.md](tasklist-bot.md), итерация 3.

---

## Итерация 4: Аналитика и динамика 📋

→ [plan.md, итерация 4](../plan.md#итерация-4--аналитика-и-динамика-состояния)

### Цель

Снимки прогресса, сигналы изменений, справочные рекомендации.

### Список задач

| Задача | Описание | Статус | Документы |
|--------|----------|--------|-----------|
| 01 | Контракты API аналитики | 📋 Planned | [план](impl/backend/iteration-10-analytics/tasks/task-01-analytics-contracts/plan.md) · [summary](impl/backend/iteration-10-analytics/tasks/task-01-analytics-contracts/summary.md) |
| 02 | Снимки прогресса | 📋 Planned | [план](impl/backend/iteration-10-analytics/tasks/task-02-progress-snapshots/plan.md) · [summary](impl/backend/iteration-10-analytics/tasks/task-02-progress-snapshots/summary.md) |
| 03 | Рекомендации и сигналы | 📋 Planned | [план](impl/backend/iteration-10-analytics/tasks/task-03-recommendations/plan.md) · [summary](impl/backend/iteration-10-analytics/tasks/task-03-recommendations/summary.md) |
| 04 | Docs и запуск | 📋 Planned | [план](impl/backend/iteration-10-analytics/tasks/task-04-docs-and-run/plan.md) · [summary](impl/backend/iteration-10-analytics/tasks/task-04-docs-and-run/summary.md) |

**Артефакты:** модули аналитики, ProgressSnapshot, Recommendation — [data-model.md](../data-model.md)

- 📋 [План итерации](impl/backend/iteration-10-analytics/plan.md) · 📝 [Summary](impl/backend/iteration-10-analytics/summary.md)

---

## Качество и инженерные практики

На всех этапах 2.1–4:

- **Тесты** — smoke/integration на ключевые API; unit для аналитики.
- **Линтеры** — ruff, `make lint` / `make format` для `backend/`.
- **Наблюдаемость** — structured logging; без промптов и ПДн.
- **Контракты** — изменения через `docs/api/`; breaking — только с bump версии (2.3, task-02).
