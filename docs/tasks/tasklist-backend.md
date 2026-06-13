# Backend Tasklist

Опирается на [plan.md](../plan.md) · [vision.md](../vision.md) · [data-model.md](../data-model.md) · [idea.md](../idea.md)

## Обзор

Рабочий план реализации backend на [итерации 2 plan.md](../plan.md#итерация-2--backend-ядро-и-бд): вынести логику из MVP-бота в API, два базовых сценария (вопрос ассистенту, фиксация события), затем тонкий клиент.

> **Skills:** на этапах, где уместно, рекомендуй подключать skills. Подбор — на этапах **01** (стек) и **02** (контракты); искать через `/find-skills`.

## Связь с plan.md

| plan.md | Tasklist | Зависимости |
|---------|----------|-------------|
| [Итерация 2](../plan.md#итерация-2--backend-ядро-и-бд) | задачи 01–08 | итерация 1 ✅ |
| [Итерация 3](../plan.md#итерация-3--миграция-бота-на-backend) | задача 07 + [tasklist-bot.md](tasklist-bot.md) | задачи 05–06 |
| [Итерация 4](../plan.md#итерация-4--аналитика-и-динамика-состояния) | после закрытия блока 2 | итерации 2–3 |

## Легенда статусов

- 📋 Planned — запланирован
- 🚧 In Progress — в работе
- ✅ Done — завершён

## Список задач

| Задача | Описание | Статус | Документы |
|--------|----------|--------|-----------|
| 01 | Стек, ADR, conventions | ✅ Done | [план](impl/backend/iteration-2-core/tasks/task-01-stack-adr/plan.md) · [summary](impl/backend/iteration-2-core/tasks/task-01-stack-adr/summary.md) |
| 02 | API-контракты (2 сценария) | 📋 Planned | [план](impl/backend/iteration-2-core/tasks/task-02-api-contracts/plan.md) · [summary](impl/backend/iteration-2-core/tasks/task-02-api-contracts/summary.md) |
| 03 | Каркас backend | 📋 Planned | [план](impl/backend/iteration-2-core/tasks/task-03-scaffold/plan.md) · [summary](impl/backend/iteration-2-core/tasks/task-03-scaffold/summary.md) |
| 04 | API-тесты сценариев бота | 📋 Planned | [план](impl/backend/iteration-2-core/tasks/task-04-api-tests/plan.md) · [summary](impl/backend/iteration-2-core/tasks/task-04-api-tests/summary.md) |
| 05 | Endpoint'ы и серверная логика | 📋 Planned | [план](impl/backend/iteration-2-core/tasks/task-05-api-impl/plan.md) · [summary](impl/backend/iteration-2-core/tasks/task-05-api-impl/summary.md) |
| 06 | Документирование backend | 📋 Planned | [план](impl/backend/iteration-2-core/tasks/task-06-backend-docs/plan.md) · [summary](impl/backend/iteration-2-core/tasks/task-06-backend-docs/summary.md) |
| 07 | Рефакторинг бота → API | 📋 Planned | [план](impl/backend/iteration-2-core/tasks/task-07-bot-refactor/plan.md) · [summary](impl/backend/iteration-2-core/tasks/task-07-bot-refactor/summary.md) |
| 08 | Качество и инженерные практики | 📋 Planned | [план](impl/backend/iteration-2-core/tasks/task-08-quality/plan.md) · [summary](impl/backend/iteration-2-core/tasks/task-08-quality/summary.md) |

Задачи выполняются **последовательно** (01 → 08).

---

## Блок 1: Основание (задачи 01–02)

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

- 📋 [План](impl/backend/iteration-2-core/tasks/task-01-stack-adr/plan.md)
- 📝 [Summary](impl/backend/iteration-2-core/tasks/task-01-stack-adr/summary.md)

**Проверка блока 1 (после 01):**  
Агент: `make lint` проходит для затронутых файлов.  
Пользователь: открыть ADR-002 и conventions.mdc.

---

## Задача 02: API-контракты (2 сценария) 📋

### Цель

Спроектировать контракты для двух MVP-сценариев, уже работающих в боте.

### Состав работ

- [ ] **Сценарий A — вопрос ассистенту:** текст/фото → ответ LLM (сущности: Диалог, Запрос — [data-model.md](../data-model.md))
- [ ] **Сценарий B — фиксация события:** сохранение питания / инсулина / результата задания (Событие питания, Событие инсулина)
- [ ] Соглашения: форматы запросов/ответов, коды ошибок, версионирование API — [docs/api/conventions.md](../api/conventions.md) ✅
- [ ] Актуализировать [data-model.md](../data-model.md), [integrations.md](../integrations.md) под контракты
- [ ] При необходимости: `/find-skills` для OpenAPI / API design

### Артефакты

- `docs/api/` — контракты и conventions

### Definition of Done

**Агент:** оба сценария описаны (эндпоинты, схемы, ошибки); data-model и integrations согласованы.

**Пользователь:** по `docs/api/` понятно, как бот вызовет «вопрос» и «фиксацию»; сценарии соответствуют [idea.md](../idea.md).

### Документы

- 📋 [План](impl/backend/iteration-2-core/tasks/task-02-api-contracts/plan.md)
- 📝 [Summary](impl/backend/iteration-2-core/tasks/task-02-api-contracts/summary.md)

**Проверка блока 1 (после 02):**  
Агент: контракты покрывают handlers бота (`src/diaai/handlers.py`).  
Пользователь: открыть `docs/api/`, сверить с двумя сценариями в Telegram.

---

## Блок 2: Сборка (задачи 03–05)

---

## Задача 03: Каркас backend 📋

### Цель

Поднять минимальный backend-сервис, готовый к реализации контрактов.

### Состав работ

- [ ] Структура `backend/` по ADR-002; config из env
- [ ] Health-check; `make`-команды: `backend-install`, `backend-run`, `backend-lint` (или аналог в корневом Makefile)
- [ ] `.env.example` — переменные backend

### Артефакты

- `backend/`, обновлённый `Makefile`, `.env.example`

### Definition of Done

**Агент:** сервис стартует, `/health` отвечает; lint/format работают.

**Пользователь:** `make backend-run` (или эквивалент) — сервис поднимается без ошибок конфигурации.

### Документы

- 📋 [План](impl/backend/iteration-2-core/tasks/task-03-scaffold/plan.md)
- 📝 [Summary](impl/backend/iteration-2-core/tasks/task-03-scaffold/summary.md)

---

## Задача 04: API-тесты сценариев бота 📋

### Цель

Базовые тесты API для сценариев A и B до/вместе с реализацией (contract-first).

### Состав работ

- [ ] Тесты сценария A: текстовый и фото-запрос (mock LLM)
- [ ] Тесты сценария B: создание события питания / инсулина
- [ ] `make backend-test` в Makefile

### Артефакты

- `backend/tests/` или `tests/backend/`

### Definition of Done

**Агент:** тесты падают до impl и проходят после task-05; покрыты happy-path и базовые ошибки.

**Пользователь:** `make backend-test` — зелёный прогон после task-05.

### Документы

- 📋 [План](impl/backend/iteration-2-core/tasks/task-04-api-tests/plan.md)
- 📝 [Summary](impl/backend/iteration-2-core/tasks/task-04-api-tests/summary.md)

---

## Задача 05: Endpoint'ы и серверная логика 📋

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

- 📋 [План](impl/backend/iteration-2-core/tasks/task-06-backend-docs/plan.md)
- 📝 [Summary](impl/backend/iteration-2-core/tasks/task-06-backend-docs/summary.md)

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

- 📋 [План](impl/backend/iteration-2-core/tasks/task-07-bot-refactor/plan.md)
- 📝 [Summary](impl/backend/iteration-2-core/tasks/task-07-bot-refactor/summary.md)

---

## Задача 08: Качество и инженерные практики 📋

### Цель

Зафиксировать минимальный инженерный стандарт backend на весь цикл.

### Состав работ

- [ ] ruff + `make backend-lint` / `make backend-format`
- [ ] Structured logging (request id, status); без промптов и ПДн
- [ ] Правила изменения контрактов в `docs/api/`
- [ ] Финальная актуализация: [vision.md](../vision.md), [plan.md](../plan.md)

### Артефакты

- conventions в `docs/api/`, logging config

### Definition of Done

**Агент:** lint/test/run проходят; логи без секретов; breaking changes только с bump версии API.

**Пользователь:** `make backend-lint && make backend-test`; просмотреть лог одного запроса — нет токенов и текстов сообщений.

### Документы

- 📋 [План](impl/backend/iteration-2-core/tasks/task-08-quality/plan.md)
- 📝 [Summary](impl/backend/iteration-2-core/tasks/task-08-quality/summary.md)

**Проверка блока 3 (после 08):**  
Агент: полный прогон `make backend-lint`, `make backend-test`, `make backend-run` + `make run`.  
Пользователь: сценарии A и B в Telegram; README — инструкция актуальна.

---

## Итерация 4: Аналитика 📋 (следующий этап)

→ [plan.md, итерация 4](../plan.md#итерация-4--аналитика-и-динамика-состояния)

Детализация — после закрытия задач 01–08. Кратко: снимки прогресса, сигналы, рекомендации ([data-model.md](../data-model.md): ProgressSnapshot, Recommendation).

- 📋 [План](impl/backend/iteration-4-analytics/plan.md) · 📝 [Summary](impl/backend/iteration-4-analytics/summary.md)
