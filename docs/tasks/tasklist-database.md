# Database Tasklist

Опирается на [plan.md](../plan.md) · [vision.md](../vision.md) · [data-model.md](../data-model.md) · [api-contract.md](../api/api-contract.md)

## Обзор

Рабочий план области **слой данных**: от продуктовых сценариев и полной схемы PostgreSQL до инфраструктуры, seed и интеграции в backend. Закрывает пробелы MVP-схемы (`001_initial_schema`) — роли, аналитика, консультации, анализ фото — и готовит единый источник данных для [backend iteration 4](tasklist-backend.md) и [web](tasklist-web.md).

**Текущее состояние:** PostgreSQL + Alembic + SQLAlchemy 2 уже используются backend'ом (users, dialogs, events). Бот не хранит историю в RAM — данные в БД через API. Этот tasklist доводит модель до **полноценного слоя** под web и аналитику.

**Прогресс:** **1 / 5** итераций (01 ✅) · [`docs/spec/`](../../spec/) · [`backend/README.md`](../../backend/README.md)

> **Skills:** на этапах, где уместно, подключать skills для дополнительных проверок:
> - **итерация 2** — [postgresql-table-design](../../.agents/skills/postgresql-table-design/SKILL.md) (review схемы)
> - **итерация 5** — [fastapi-templates](../../.agents/skills/fastapi-templates/SKILL.md) (интеграция БД в backend)
> - **итерация 5** — [python-testing-patterns](../../.agents/skills/python-testing-patterns/SKILL.md) *(если добавляются тесты migrations/repos/E2E)*  
> Подбор других skills — через `/find-skills`.

## Итерации

Сводный план: [impl/database/plan.md](impl/database/plan.md) *(создать перед стартом итерации 1)*

| # | Название | Задача | Статус | Документы |
|---|----------|--------|--------|-----------|
| 1 | Сценарии и требования к данным | 01 | ✅ Done | [plan](impl/database/iteration-1-user-scenarios/plan.md) · [summary](impl/database/iteration-1-user-scenarios/summary.md) |
| 2 | Проектирование схемы | 02 | 📋 Planned | [plan](impl/database/iteration-2-schema-design/plan.md) · [summary](impl/database/iteration-2-schema-design/summary.md) |
| 3 | ADR и практика доступа к БД | 03 | 📋 Planned | [plan](impl/database/iteration-3-data-access-adr/plan.md) · [summary](impl/database/iteration-3-data-access-adr/summary.md) |
| 4 | Инфраструктура, seed, команды | 04 | 📋 Planned | [plan](impl/database/iteration-4-db-infra-seed/plan.md) · [summary](impl/database/iteration-4-db-infra-seed/summary.md) |
| 5 | ORM, репозитории, backend | 05 | 📋 Planned | [plan](impl/database/iteration-5-orm-repos/plan.md) · [summary](impl/database/iteration-5-orm-repos/summary.md) |

## Связь с plan.md и другими tasklist'ами

| plan.md / область | Этот tasklist | Зависимости |
|-------------------|---------------|-------------|
| [Итерация 4 — аналитика](../plan.md#итерация-4--аналитика-и-динамика-состояния) | итерации 2, 5 — таблицы `progress_snapshots`, агрегаты | [tasklist-backend](tasklist-backend.md) 09–12 |
| [Итерация 5 — web](../plan.md#итерация-5--веб-интерфейс-диабетикдоктор) | итерация 1 — сценарии UI диабетика/доктора | [tasklist-web.md](tasklist-web.md) |
| Backend MVP ✅ | миграция `001_initial_schema` — база для расширения | [iteration-2-core summary](impl/backend/iteration-2-core/summary.md) |

## Легенда статусов

- 📋 Planned — запланирован
- 🚧 In Progress — в работе
- ✅ Done — завершён

## Список задач

| Задача | Описание | Статус | Документы |
|--------|----------|--------|-----------|
| 01 | Сценарии пользователя и требования к данным | ✅ Done | [план](impl/database/iteration-1-user-scenarios/tasks/task-01-user-scenarios/plan.md) · [summary](impl/database/iteration-1-user-scenarios/tasks/task-01-user-scenarios/summary.md) |
| 02 | Проектирование схемы (логика + физика + ER) | 📋 Planned | [план](impl/database/iteration-2-schema-design/tasks/task-02-schema-design/plan.md) · [summary](impl/database/iteration-2-schema-design/tasks/task-02-schema-design/summary.md) |
| 03 | ADR и практика: миграции и доступ к БД | 📋 Planned | [план](impl/database/iteration-3-data-access-adr/tasks/task-03-data-access-adr/plan.md) · [summary](impl/database/iteration-3-data-access-adr/tasks/task-03-data-access-adr/summary.md) |
| 04 | Инфраструктура БД, seed, команды обслуживания | 📋 Planned | [план](impl/database/iteration-4-db-infra-seed/tasks/task-04-db-infra-seed/plan.md) · [summary](impl/database/iteration-4-db-infra-seed/tasks/task-04-db-infra-seed/summary.md) |
| 05 | ORM, репозитории, интеграция в backend | 📋 Planned | [план](impl/database/iteration-5-orm-repos/tasks/task-05-orm-repos/plan.md) · [summary](impl/database/iteration-5-orm-repos/tasks/task-05-orm-repos/summary.md) |

Итерации выполняются **последовательно** (1 → 5).

---

## Итерация 1: Сценарии и требования к данным ✅

→ [iteration-1-user-scenarios/plan.md](impl/database/iteration-1-user-scenarios/plan.md) · [summary](impl/database/iteration-1-user-scenarios/summary.md)

### Цель итерации

Зафиксировать продуктовые сценарии диабетика и доктора и вывести минимальный набор сущностей, полей и связей для web и аналитики.

### Задача 01

#### Состав работ

- [x] Описать **5–7 базовых сценариев диабетика**: дневник питания/инсулина, вопрос ассистенту, динамика за период, рекомендации, запись к доктору, просмотр истории консультаций
- [x] Описать **3–4 сценария доктора**: список пациентов, обзор динамики пациента, консультация (статус, комментарий), справочные заметки без назначения доз
- [x] Для каждого сценария — таблица «экран / действие → данные (read) → сохранение (write)»
- [x] Сверить с [idea.md](../idea.md), [vision.md](../vision.md#роли-и-сценарии), [api-contract.md](../api/api-contract.md)
- [x] Выделить **MVP data scope** vs **backlog**

#### Актуализация документации

| Файл | Что обновить |
|------|--------------|
| `docs/spec/user-scenarios.md` | **создано** — сценарии диабетика и доктора |
| `docs/spec/data-requirements.md` | **создано** — матрица read/write по ролям |
| `docs/data-model.md` | раздел «Требования из сценариев», gap analysis |
| `docs/vision.md` | ссылка на `docs/spec/` |

#### Make-команды

Не требуются (только документы). Проверка: `make lint` — если затронуты markdown-ссылки в коде — опционально.

#### Артефакты

- `docs/spec/user-scenarios.md`, `docs/spec/data-requirements.md`
- обновления: `docs/data-model.md`, `docs/vision.md`

### Definition of Done — итерация 1

**Self-check (агент):** документы согласованы с vision/idea; для каждого сценария перечислены сущности и связи; явный gap-list относительно MVP-схемы (`users`, `dialogs`, `food_events`, `insulin_events`); нет противоречий с [api-contract.md](../api/api-contract.md) v1.

**User-check (пользователь):** прочитать `user-scenarios.md` — понятно, что увидит диабетик и доктор в web; по `data-requirements.md` видно, какие таблицы понадобятся; сценарии покрывают итерации 4–5 из [plan.md](../plan.md).

### Документы

- 📋 [План итерации](impl/database/iteration-1-user-scenarios/plan.md) · [task-01 plan](impl/database/iteration-1-user-scenarios/tasks/task-01-user-scenarios/plan.md)
- 📝 [Summary](impl/database/iteration-1-user-scenarios/summary.md) · [task-01 summary](impl/database/iteration-1-user-scenarios/tasks/task-01-user-scenarios/summary.md)

---

## Итерация 2: Проектирование схемы данных 📋

→ [iteration-2-schema-design/plan.md](impl/database/iteration-2-schema-design/plan.md)

### Цель итерации

Актуализировать логическую и физическую модель PostgreSQL, ER-диаграмму и design review по `postgresql-table-design`.

### Задача 02

#### Состав работ

- [ ] Логическая модель: сущности из итерации 1 + связи, cardinality, nullable FK
- [ ] Физическая модель: таблицы, типы PG (`UUID`, `TIMESTAMPTZ`, `NUMERIC`, `JSONB`), PK/FK, индексы на FK и фильтры (`user_id`, `recorded_at`, `telegram_id`)
- [ ] ER-диagram (Mermaid) в `docs/spec/schema-er.md`; mapping «логика → таблица/колонка»
- [ ] Diff MVP → целевая схема: новые таблицы, расширение `users`
- [ ] Review по [postgresql-table-design](../../.agents/skills/postgresql-table-design/SKILL.md) → `docs/spec/schema-review.md`
- [ ] Черновик DDL миграции `002_*` (в plan; impl — итерация 5)
- [ ] **Skill:** пройти checklist [postgresql-table-design](../../.agents/skills/postgresql-table-design/SKILL.md); результат — в `schema-review.md`

#### Skills

[postgresql-table-design](../../.agents/skills/postgresql-table-design/SKILL.md) — обязательный review физической схемы: типы, FK-индексы, `TIMESTAMPTZ`, NOT NULL, checklist pass/warn/fix.

#### Актуализация документации

| Файл | Что обновить |
|------|--------------|
| `docs/spec/schema-er.md` | **создать** — ER + физическая схема |
| `docs/spec/schema-review.md` | **создать** — pass/warn/fix из skill review |
| `docs/data-model.md` | логическая модель, SQL-схема (целевая), diff с MVP |
| `docs/api/api-contract.md` | только если меняются доменные persisted fields *(без новых endpoint'ов)* |

#### Make-команды

Не требуются. Self-check: сверка с `alembic/versions/001_initial_schema.py` вручную или через diff в summary.

#### Артефакты

- `docs/spec/schema-er.md`, `docs/spec/schema-review.md`
- обновления: `docs/data-model.md`

### Definition of Done — итерация 2

**Self-check (агент):** ER покрывает итерацию 1; для каждой FK — индекс; время — `TIMESTAMPTZ`; review по `postgresql-table-design` задокументирован в `schema-review.md`; diff с `001_initial_schema.py` явный; согласовано с [ADR-001](../adr/adr-001-database.md).

**User-check (пользователь):** открыть `schema-er.md` — связи читаются; `schema-er.md` и `data-model.md` описывают одни сущности; в `schema-review.md` нет незакрытых **Fix** без defer.

### Документы

- 📋 [План итерации](impl/database/iteration-2-schema-design/plan.md) · [task-02 plan](impl/database/iteration-2-schema-design/tasks/task-02-schema-design/plan.md)
- 📝 [Summary](impl/database/iteration-2-schema-design/summary.md) · [task-02 summary](impl/database/iteration-2-schema-design/tasks/task-02-schema-design/summary.md)

---

## Итерация 3: ADR и практика доступа к БД 📋

→ [iteration-3-data-access-adr/plan.md](impl/database/iteration-3-data-access-adr/plan.md)

### Цель итерации

Зафиксировать инструменты миграций и доступа к данным в ADR и практической справке для разработчиков.

### Задача 03

#### Состав работ

- [ ] Сравнить SQLAlchemy 2 + Alembic vs raw SQL vs альтернативные ORM
- [ ] ADR: `docs/adr/adr-003-data-access-layer.md` — async session, repositories, миграции, rollback
- [ ] Справка: `docs/tech/database-access.md` — устройство `backend/database.py`, `alembic/`, `repositories/`; workflow «новая таблица»
- [ ] Соглашения: naming, один файл модели на таблицу, транзакции в service, без SQL в handlers

#### Актуализация документации

| Файл | Что обновить |
|------|--------------|
| `docs/adr/adr-003-data-access-layer.md` | **создать** |
| `docs/tech/database-access.md` | **создать** — пошаговый guide + make-команды |
| `docs/adr/README.md` | запись ADR-003 |
| `docs/tech/backend-structure.md` | слой данных, ссылка на database-access |
| `backend/README.md` | секция «Миграции и БД», ссылки на ADR и guide |

#### Make-команды

Задокументировать в `database-access.md` *(существующие и целевые)*:

| Команда | Назначение |
|---------|------------|
| `make backend-migrate` | `alembic upgrade head` |
| `make backend-test` | pytest backend (в т.ч. после migrate) |
| `make db-*` | см. итерацию 4 — добавить в guide после task-04 |

Self-check: `make backend-migrate` и `make backend-test` проходят на текущей схеме.

#### Артефакты

- `docs/adr/adr-003-data-access-layer.md`, `docs/tech/database-access.md`
- обновления: `docs/adr/README.md`, `docs/tech/backend-structure.md`, `backend/README.md`

### Definition of Done — итерация 3

**Self-check (агент):** ADR принят; `database-access.md` содержит copy-paste команды (`make backend-migrate`, создание revision); conventions не противоречат [conventions.mdc](../../.cursor/rules/conventions.mdc); `make backend-migrate && make backend-test` — green.

**User-check (пользователь):** по ADR понятно «почему Alembic + SQLAlchemy»; по `database-access.md` — как добавить таблицу за 5 шагов; `backend/README.md` ссылается на guide.

### Документы

- 📋 [План итерации](impl/database/iteration-3-data-access-adr/plan.md) · [task-03 plan](impl/database/iteration-3-data-access-adr/tasks/task-03-data-access-adr/plan.md)
- 📝 [Summary](impl/database/iteration-3-data-access-adr/summary.md) · [task-03 summary](impl/database/iteration-3-data-access-adr/tasks/task-03-data-access-adr/summary.md)

---

## Итерация 4: Инфраструктура, seed, команды 📋

→ [iteration-4-db-infra-seed/plan.md](impl/database/iteration-4-db-infra-seed/plan.md)

### Цель итерации

Повторяемое локальное окружение PostgreSQL: поднятие/сброс, seed из реального прогресса, скрипты просмотра данных.

### Задача 04

#### Состав работ

- [ ] Спецификация `data/progress-import.v1.json` — users, food/insulin events, опционально snapshots
- [ ] `scripts/db/seed_from_progress.py` — idempotent load после migrate
- [ ] `scripts/db/inspect.py` — counts, sample rows (без ПДн по умолчанию)
- [ ] Добавить цели в корневой `Makefile` (см. таблицу ниже)
- [ ] Проверка: `make db-reset` → `make db-inspect`

#### Актуализация документации

| Файл | Что обновить |
|------|--------------|
| `data/progress-import.v1.json` | **создать** — эталонная анонимизированная выгрузка |
| `data/progress-import.v1.schema.json` | **создать** *(опционально)* — JSON Schema |
| `scripts/db/seed_from_progress.py`, `inspect.py` | **создать** |
| `Makefile` | цели `db-*` |
| `docker-compose.yml` | healthcheck/wait при необходимости |
| `backend/README.md` | таблица `db-*` команд |
| `README.md` | quick start: `make db-reset` |
| `.env.example` | `DATABASE_URL` |
| `docs/tech/database-access.md` | дополнить секцией «Локальное окружение и seed» |

#### Make-команды

**Добавить / актуализировать в `Makefile`:**

| Команда | Действие |
|---------|----------|
| `make db-up` | `docker compose up -d` + wait healthy |
| `make db-down` | остановка PostgreSQL |
| `make db-reset` | volumes down + up + migrate + seed |
| `make db-migrate` | alias `backend-migrate` / `alembic upgrade head` |
| `make db-seed` | загрузка `data/progress-import.v1.json` |
| `make db-shell` | `psql` → localhost:5433 / контейнер |
| `make db-inspect` | `python scripts/db/inspect.py` |

Self-check: `make db-reset && make db-inspect`; повторный `make db-seed` — без дублей (upsert documented).

#### Артефакты

- `data/progress-import.v1.json`, `scripts/db/*`, `Makefile`
- обновления: README, `docker-compose.yml`, `database-access.md`

### Definition of Done — итерация 4

**Self-check (агент):** `make db-reset && make db-inspect` — green; seed idempotent; миграции на чистой БД; `make backend-test` на seeded DB — green.

**User-check (пользователь):** выполнить `make db-reset`; открыть `data/progress-import.v1.json`; `make db-inspect` — видны users/events; `make db-shell` — ручной SELECT; `backend/README.md` и корневой `README.md` описывают все `db-*`.

### Документы

- 📋 [План итерации](impl/database/iteration-4-db-infra-seed/plan.md) · [task-04 plan](impl/database/iteration-4-db-infra-seed/tasks/task-04-db-infra-seed/plan.md)
- 📝 [Summary](impl/database/iteration-4-db-infra-seed/summary.md) · [task-04 summary](impl/database/iteration-4-db-infra-seed/tasks/task-04-db-infra-seed/summary.md)

---

## Итерация 5: ORM, репозитории, backend 📋

→ [iteration-5-orm-repos/plan.md](impl/database/iteration-5-orm-repos/plan.md)

### Цель итерации

Реализовать целевую схему в коде: модели, репозитории, миграция `002_*`, интеграция в services — полный слой данных в PostgreSQL, E2E с seed.

### Задача 05

#### Состав работ

- [ ] `alembic/versions/002_full_data_layer.py` — DDL по итерации 2
- [ ] `backend/models/` — новые сущности + расширение `User`
- [ ] `backend/repositories/` — CRUD/list/filter; async session
- [ ] Services: `events_service`, `assistant_service` *(photo_analysis persist)*; заготовки progress/consultation
- [ ] Нет in-memory store для доменных данных
- [ ] Тесты: `test_migrations.py`, `test_repositories_*.py`, `conftest.py`
- [ ] Прогон: `make db-reset && make backend-test && make test`
- [ ] **Skill:** сверка структуры `backend/models/`, `repositories/`, wiring в services с [fastapi-templates](../../.agents/skills/fastapi-templates/SKILL.md)
- [ ] **Skill:** *(при расширении тестов)* — fixtures, async DB session, isolation по [python-testing-patterns](../../.agents/skills/python-testing-patterns/SKILL.md)

#### Skills

| Skill | Когда | Фокус проверки |
|-------|-------|----------------|
| [fastapi-templates](../../.agents/skills/fastapi-templates/SKILL.md) | интеграция ORM/repos в backend | слои models → repos → services → API deps; async session lifecycle |
| [python-testing-patterns](../../.agents/skills/python-testing-patterns/SKILL.md) | доп. тесты migrations/repos/E2E | fixtures, test DB, transaction rollback, pytest-asyncio |

#### Актуализация документации

| Файл | Что обновить |
|------|--------------|
| `docs/data-model.md` | SQL-схема (фактическая после `002_*`) |
| `docs/api/api-contract.md` | persisted fields *(если менялись)* |
| `docs/tasks/tasklist-backend.md` | зависимость для задач 09–12 |
| `docs/plan.md` | готовность data layer для итераций 4–5 |
| `docs/tasks/impl/database/summary.md` | **создать** — сводка области |
| `backend/README.md` | новые таблицы / миграция `002_*` |

#### Make-команды

| Команда | Когда |
|---------|-------|
| `make db-reset` | перед прогоном тестов на чистой seeded БД |
| `make backend-migrate` | применить `002_*` |
| `make backend-test` | migrations + repositories |
| `make test` | backend + bot |
| `make db-inspect` | проверка записей после curl E2E |
| `make backend-run` | manual E2E user-check |

Self-check: `make db-reset && make test` — green; migrate up/down на чистой БД.

#### Артефакты

- `alembic/versions/002_*.py`, `backend/models/*`, `backend/repositories/*`, tests
- обновления services, docs (см. таблицу выше)

### Definition of Done — итерация 5

**Self-check (агент):** `make db-reset && make test` green; репозитории покрыты тестами; assistant/events пишут в новые таблицы где предусмотрено; нет RAM persistence; структура backend согласована с `fastapi-templates`; новые тесты *(если есть)* — по `python-testing-patterns`.

**User-check (пользователь):** `make db-reset` → `make backend-run` → curl assistant + events → `make db-inspect` — записи в PG; restart backend — данные на месте; сценарий «bot → backend → PostgreSQL → inspect» на seeded данных.

### Документы

- 📋 [План итерации](impl/database/iteration-5-orm-repos/plan.md) · [task-05 plan](impl/database/iteration-5-orm-repos/tasks/task-05-orm-repos/plan.md)
- 📝 [Summary](impl/database/iteration-5-orm-repos/summary.md) · [task-05 summary](impl/database/iteration-5-orm-repos/tasks/task-05-orm-repos/summary.md)

---

## Критерии завершения области (все 5 итераций)

| Итерация | Критерий | Проверка |
|----------|----------|----------|
| 1 | Сценарии + матрица данных | ✅ `docs/spec/user-scenarios.md`, `data-requirements.md` |
| 2 | ER + PG review | `schema-er.md`, `schema-review.md` *(postgresql-table-design)* |
| 3 | ADR + guide | `adr-003`, `docs/tech/database-access.md` |
| 4 | One-command окружение | `make db-reset`, `make db-inspect`, `make db-shell` |
| 5 | Backend на полной схеме | `make test`, seeded E2E; skills: fastapi-templates, python-testing-patterns |

## Связанные документы

| Документ | Назначение |
|----------|------------|
| [data-model.md](../data-model.md) | доменные сущности |
| [api-contract.md](../api/api-contract.md) | REST v1 (сценарии A/B) |
| [adr-001-database.md](../adr/adr-001-database.md) | выбор PostgreSQL |
| [adr-002-backend-stack.md](../adr/adr-002-backend-stack.md) | FastAPI + SQLAlchemy + Alembic |
| [tasklist-backend.md](tasklist-backend.md) | API и аналитика (09–12) |
| [tasklist-web.md](tasklist-web.md) | frontend диабетик/доктор |
| [templates/workflow.md](../templates/workflow.md) | процесс plan/summary |
