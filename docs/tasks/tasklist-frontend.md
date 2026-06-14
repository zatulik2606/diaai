# Frontend Tasklist

Опирается на [plan.md](../plan.md) · [vision.md](../vision.md) · [data-model.md](../data-model.md) · [api-contract.md](../api/api-contract.md) · [spec/user-scenarios.md](../spec/user-scenarios.md)

## Обзор

Рабочий план области **frontend** (`web/`): Next.js App Router + TypeScript + shadcn/ui + Tailwind + pnpm. Тонкий клиент backend API ([vision.md](../vision.md)); данные — PostgreSQL через REST.

**Маппинг UI → домен diaai** (зафиксирован ✅ iter 0 → [frontend-requirements.md](../spec/frontend-requirements.md)):

| Зона UI (ТЗ) | Роль / домен diaai |
|--------------|-------------------|
| Панель преподавателя | Панель **доктора** — когорта пациентов, KPI, активность, вопросы, сдачи, матрица прогресса |
| Лидерборд | Рейтинг прогресса **диабетиков** (ХЕ/БЖЕ/инсулин / периоды) |
| Чат (глобальный + страницы) | Диалог с **ассистентом** (сценарий D2) |
| Студенты × уроки | **Пациенты × периоды/метрики** (progress matrix) |

**Текущее состояние:** spec UI + API contracts ✅ (iter 0); `web/` — toolchain only (Next.js iter 2).

**Прогресс:** **1 / 10** итераций ✅ · **1 / 10** задач ✅ · **следующая:** iter 1 (API) · [impl/frontend/plan.md](impl/frontend/plan.md) · [summary](impl/frontend/summary.md)

**Зависимости:**

| Область | Статус | Нужно frontend'у |
|---------|--------|------------------|
| Backend MVP (assistant, events) | ✅ | базовый чат, события |
| Database iter 5 (9 таблиц) | ✅ | analytics, consultations |
| Backend iter 4 (analytics API) | 📋 | KPI, snapshots, leaderboard *(iter 1 frontend частично закрывает gap)* |

## Стек

| Слой | Выбор |
|------|--------|
| Framework | Next.js (App Router) + React |
| Язык | TypeScript |
| UI | shadcn/ui |
| Styling | Tailwind CSS |
| Package manager | pnpm (corepack) |
| Node | 20+; dev pin — `web/.nvmrc` → 24 |

**Toolchain (уже в репо):**

```
web/
├── .nvmrc          # 24
├── .npmrc          # engine-strict=true
└── package.json    # engines, packageManager
```

Локально: `cd web && nvm use && corepack enable && corepack prepare pnpm@11.6.0 --activate`

## Skills (дополнительные проверки)

Подбор других skills — `/find-skills`.

| Skill | Когда | Фокус проверки |
|-------|-------|----------------|
| [api-design-principles](../.agents/skills/api-design-principles/SKILL.md) | **iter 0** (контракты), **iter 1** (реализация API) | REST design, ошибки, versioning, примеры |
| [fastapi-templates](../.agents/skills/fastapi-templates/SKILL.md) | **iter 1** — новые backend endpoint'ы | handler → service → repo → `get_db` |
| [modern-python](../.agents/skills/modern-python/SKILL.md) | **iter 1** — при новых services/утилитах | uv, ruff, pyproject, async patterns |
| [postgresql-table-design](../.agents/skills/postgresql-table-design/SKILL.md) | **iter 1** — если нужна доработка схемы | типы, индексы, FK, TIMESTAMPTZ |
| [sharp-edges](../.agents/skills/sharp-edges/SKILL.md) | **iter 1** — при изменении схемы/API | security, auth, config pitfalls |
| `shadcn` | **iter 2** (каркас), **iter 3–6** (экраны), **iter 7** (ревью) | компоненты, a11y, theming *(skill — `/find-skills`)* |
| [vercel-react-best-practices](../.agents/skills/vercel-react-best-practices/SKILL.md) | **iter 2**, **iter 3–6**, **iter 7** | RSC, data fetching, rerenders, bundle |
| [nextjs-app-router-patterns](../.agents/skills/nextjs-app-router-patterns/SKILL.md) | **iter 2**, **iter 3–6**, **iter 7** | layouts, routes, server/client components |

## Make-команды (целевые)

| Команда | Действие | Итерация |
|---------|----------|----------|
| `make web-install` | `cd web && pnpm install` | 2 |
| `make web-dev` | `cd web && pnpm dev` | 2 |
| `make web-build` | `cd web && pnpm build` | 2+ |
| `make web-lint` | `cd web && pnpm lint` | 2+ |
| `make backend-run` | API для frontend | 1+ |
| `make db-reset` | seeded PG для E2E | 1+ |

*Добавить в корневой `Makefile` при реализации iter 2.*

## Итерации

Сводный план: [impl/frontend/plan.md](impl/frontend/plan.md) · [summary](impl/frontend/summary.md)

| # | Название | Задача | Статус | Документы |
|---|----------|--------|--------|-----------|
| 0 | Требования UI и API-контракты | 00 | ✅ Done | [plan](impl/frontend/iteration-0-ui-contracts/plan.md) · [summary](impl/frontend/iteration-0-ui-contracts/summary.md) |
| 1 | API для frontend | 01 | 📋 Planned | [plan](impl/frontend/iteration-1-frontend-api/plan.md) · [summary](impl/frontend/iteration-1-frontend-api/summary.md) |
| 2 | Каркас frontend | 02 | 📋 Planned | [plan](impl/frontend/iteration-2-scaffold/plan.md) · [summary](impl/frontend/iteration-2-scaffold/summary.md) |
| 3 | Панель преподавателя | 03 | 📋 Planned | [plan](impl/frontend/iteration-3-teacher-dashboard/plan.md) · [summary](impl/frontend/iteration-3-teacher-dashboard/summary.md) |
| 4 | Лидерборд | 04 | 📋 Planned | [plan](impl/frontend/iteration-4-leaderboard/plan.md) · [summary](impl/frontend/iteration-4-leaderboard/summary.md) |
| 5 | Чат с ассистентом | 05 | 📋 Planned | [plan](impl/frontend/iteration-5-assistant-chat/plan.md) · [summary](impl/frontend/iteration-5-assistant-chat/summary.md) |
| 6 | Чат в основной области | 06 | 📋 Planned | [plan](impl/frontend/iteration-6-main-chat/plan.md) · [summary](impl/frontend/iteration-6-main-chat/summary.md) |
| 7 | Ревью качества | 07 | 📋 Planned | [plan](impl/frontend/iteration-7-quality-review/plan.md) · [summary](impl/frontend/iteration-7-quality-review/summary.md) |
| 8 | Голосовой режим | 08 | 📋 Planned | [plan](impl/frontend/iteration-8-voice-chat/plan.md) · [summary](impl/frontend/iteration-8-voice-chat/summary.md) |
| 9 | Text-to-SQL | 09 | 📋 Planned | [plan](impl/frontend/iteration-9-text-to-sql/plan.md) · [summary](impl/frontend/iteration-9-text-to-sql/summary.md) |

## Связь с plan.md

| plan.md | Frontend tasklist | Зависимости |
|---------|-------------------|-------------|
| [Итерация 5 — веб](../plan.md#итерация-5--веб-интерфейс-диабетикдоктор) | итерации 0–9 | backend + database ✅ |
| [Итерация 4 — аналитика](../plan.md#итерация-4--аналитика-и-динамика-состояния) | iter 1, 3, 4 | [tasklist-backend](tasklist-backend.md) 09–12 |

## Легенда статусов

- 📋 Planned — запланирован
- 🚧 In Progress — в работе
- ✅ Done — завершён

## Список задач

| Задача | Описание | Статус | Документы |
|--------|----------|--------|-----------|
| 00 | UI-требования и API-контракты frontend | ✅ Done | [план](impl/frontend/iteration-0-ui-contracts/tasks/task-00-ui-contracts/plan.md) · [summary](impl/frontend/iteration-0-ui-contracts/tasks/task-00-ui-contracts/summary.md) |
| 01 | Backend API + mock seed для UI | 📋 Planned | [план](impl/frontend/iteration-1-frontend-api/tasks/task-01-frontend-api/plan.md) |
| 02 | Каркас Next.js + layout + auth | 📋 Planned | [план](impl/frontend/iteration-2-scaffold/tasks/task-02-scaffold/plan.md) |
| 03 | Панель преподавателя / доктора | 📋 Planned | [план](impl/frontend/iteration-3-teacher-dashboard/tasks/task-03-teacher-dashboard/plan.md) |
| 04 | Лидерборд | 📋 Planned | [план](impl/frontend/iteration-4-leaderboard/tasks/task-04-leaderboard/plan.md) |
| 05 | Чат с ассистентом (страница) | 📋 Planned | [план](impl/frontend/iteration-5-assistant-chat/tasks/task-05-assistant-chat/plan.md) |
| 06 | Чат в меню «Чат» | 📋 Planned | [план](impl/frontend/iteration-6-main-chat/tasks/task-06-main-chat/plan.md) |
| 07 | Ревью качества frontend | 📋 Planned | [план](impl/frontend/iteration-7-quality-review/tasks/task-07-quality-review/plan.md) |
| 08 | Голосовой режим (web + bot) | 📋 Planned | [план](impl/frontend/iteration-8-voice-chat/tasks/task-08-voice-chat/plan.md) |
| 09 | Text-to-SQL по данным БД | 📋 Planned | [план](impl/frontend/iteration-9-text-to-sql/tasks/task-09-text-to-sql/plan.md) |

Итерации выполняются **последовательно** (0 → 9).

---

## Итерация 0: Требования к UI и API-контракты ✅

→ [iteration-0-ui-contracts/plan.md](impl/frontend/iteration-0-ui-contracts/plan.md)

### Цель

Зафиксировать функциональные требования к четырём зонам UI, стиль, вход и REST-контракты для всех экранов.

### Задача 00

#### Состав работ

- [x] **Экран 1 — панель преподавателя (доктора):** 4 KPI с дельтой; график активности 14 дней; лента вопросов (кто, когда, вопрос + ответ); лента сдач (клик → отчёт и ссылки); матрица прогресса (студенты × уроки → пациенты × периоды/метрики, дата при hover)
- [x] **Экран 2 — лидерборд:** переключатель таблица / scatter plot; таблица — место, progress bar, иконки по урокам, топ-3 с медалями
- [x] **Глобальный чат:** плавающая кнопка на всех экранах (FAB → виджет чата)
- [x] **Стиль UI:** тёмная тема, dev-эстетика (ориентир [tbench.ai](https://www.tbench.ai/)); design tokens в spec
- [x] **Вход:** без сложной авторизации — ввод Telegram username; маппинг на `users.telegram_id` / demo user
- [x] API-контракты v2 frontend: endpoint'ы, query/body, примеры JSON для каждого экрана
- [x] Сверка с [user-scenarios.md](../spec/user-scenarios.md), [data-requirements.md](../spec/data-requirements.md), [api-contract.md](../api/api-contract.md) v1

#### Skills

| Skill | Фокус |
|-------|-------|
| [api-design-principles](../.agents/skills/api-design-principles/SKILL.md) | review контрактов frontend API; pass/warn/fix в summary |

#### Актуализация документации

| Файл | Статус |
|------|--------|
| [docs/spec/frontend-requirements.md](../spec/frontend-requirements.md) | ✅ 4 зоны, wireframes, auth |
| [docs/spec/frontend-design-system.md](../spec/frontend-design-system.md) | ✅ tbench dark, tokens |
| [docs/api/frontend-contract.md](../api/frontend-contract.md) | ✅ web endpoint'ы, JSON |
| [docs/api/openapi.yaml](../api/openapi.yaml) | ✅ tag `web` |
| [docs/api/api-contract.md](../api/api-contract.md) | ✅ web-секция |
| [docs/api/api-contract-review.md](../api/api-contract-review.md) | ✅ api-design-principles |
| [docs/spec/README.md](../spec/README.md) | ✅ индекс |
| [docs/integrations.md](../integrations.md) | ✅ web client |

#### Definition of Done

**Self-check (агент):** ✅ spec покрывает 4 зоны; контракты согласованы с data-model; нет противоречий с api v1; review в [api-contract-review.md](../api/api-contract-review.md).

**User-check (пользователь):** открыть `frontend-requirements.md` и `frontend-contract.md` — понятно, что на каждом экране; вход через username описан.

### Документы

- ✅ [План итерации](impl/frontend/iteration-0-ui-contracts/plan.md) · [Summary](impl/frontend/iteration-0-ui-contracts/summary.md) · [task-00](impl/frontend/iteration-0-ui-contracts/tasks/task-00-ui-contracts/summary.md)

---

## Итерация 1: Реализация API для frontend 📋

→ [iteration-1-frontend-api/plan.md](impl/frontend/iteration-1-frontend-api/plan.md)

**Зона:** backend + database *(координация с [tasklist-backend.md](tasklist-backend.md)*)

### Цель

Достаточность данных и endpoint'ы для отрисовки всех экранов; demo seed для наполнения UI.

### Задача 01

#### Состав работ

- [ ] Gap analysis: data-model + iter 0 контракты → список недостающих полей/таблиц
- [ ] Новые endpoint'ы backend: dashboard KPI, activity series, questions feed, submissions feed, progress matrix, leaderboard
- [ ] Миграция `003_*` (при необходимости) + seed/mock для «красивого» demo-наполнения
- [ ] Добавить **преподавателя/доктора** в БД: `@akozhin`, `telegram_id: 162684825` (role `doctor`, `display_name`)
- [ ] Contract tests / pytest для новых endpoint'ов
- [ ] Обновить [api-contracts.md](../tech/api-contracts.md), [backend/README.md](../../backend/README.md)

#### Skills

| Skill | Когда | Фокус |
|-------|-------|-------|
| [api-design-principles](../.agents/skills/api-design-principles/SKILL.md) | контракты ↔ impl | соответствие iter 0 spec |
| [fastapi-templates](../.agents/skills/fastapi-templates/SKILL.md) | новые routers/services | слои, DI, async session |
| [modern-python](../.agents/skills/modern-python/SKILL.md) | новые services/утилиты | uv/ruff, структура модулей |
| [postgresql-table-design](../.agents/skills/postgresql-table-design/SKILL.md) | миграция `003_*` | schema review перед merge |
| [sharp-edges](../.agents/skills/sharp-edges/SKILL.md) | изменения API/схемы | auth, SQL injection, secrets |

#### Make-команды

```bash
make db-reset && make db-inspect
make backend-test && make test
curl # smoke новых endpoint'ов
```

#### Definition of Done

**Self-check (агент):** миграция применяется; seed/idempotent; новые endpoint'ы 200 + schema; doctor akozhin в PG; `make test` green.

**User-check (пользователь):** `make db-inspect` — demo counts; `make backend-run` + curl dashboard/leaderboard — JSON как в контракте.

### Документы

- 📋 [План итерации](impl/frontend/iteration-1-frontend-api/plan.md) · [task-01 plan](impl/frontend/iteration-1-frontend-api/tasks/task-01-frontend-api/plan.md)

---

## Итерация 2: Каркас frontend-проекта 📋

→ [iteration-2-scaffold/plan.md](impl/frontend/iteration-2-scaffold/plan.md)

### Цель

Инициализировать Next.js App Router + shadcn/ui + Tailwind; тема, layout, вход, make-команды.

### Задача 02

#### Состав работ

- [ ] `pnpm create next-app` в `web/` (App Router, TS, Tailwind, ESLint)
- [ ] shadcn/ui init; базовые компоненты (Button, Card, Table, Chart wrapper)
- [ ] Тёмная тема (CSS variables); ориентир tbench dev-style
- [ ] Вход: форма Telegram username → session (localStorage / cookie MVP); header: user info + logout
- [ ] Layout: sidebar/nav (Dashboard, Leaderboard, Chat); **FAB глобального чата**
- [ ] API client (`fetch` + env `NEXT_PUBLIC_BACKEND_URL`, service token или public auth MVP)
- [ ] Makefile: `web-install`, `web-dev`, `web-build`, `web-lint`
- [ ] `web/README.md` — quick start

#### Skills

| Skill | Фокус |
|-------|-------|
| `shadcn` | init, theme, базовые компоненты |
| [vercel-react-best-practices](../.agents/skills/vercel-react-best-practices/SKILL.md) | структура app/, data fetching |
| [nextjs-app-router-patterns](../.agents/skills/nextjs-app-router-patterns/SKILL.md) | layout, routes, client boundaries |

#### Актуализация документации

| Файл | Что обновить |
|------|--------------|
| `README.md` | секция web quick start |
| `docs/integrations.md` | web → backend env |
| `.env.example` | `NEXT_PUBLIC_BACKEND_URL` |
| `web/README.md` | **создать** |

#### Make-команды

```bash
make web-install && make web-dev
make web-lint && make web-build
```

#### Definition of Done

**Self-check (агент):** `make web-dev` — app на :3000; навигация; FAB виден; login/logout; lint/build green.

**User-check (пользователь):** открыть localhost; ввести username; перейти по пунктам меню; тёмная тема.

### Документы

- 📋 [План итерации](impl/frontend/iteration-2-scaffold/plan.md) · [task-02 plan](impl/frontend/iteration-2-scaffold/tasks/task-02-scaffold/plan.md)

---

## Итерация 3: Панель преподавателя 📋

→ [iteration-3-teacher-dashboard/plan.md](impl/frontend/iteration-3-teacher-dashboard/plan.md)

### Цель

Страница `/dashboard` (панель доктора): KPI, график, таблицы, матрица.

### Задача 03

#### Состав работ

- [ ] 4 KPI-карточки с дельтой (к backend dashboard API)
- [ ] Line chart — активность 14 дней (recharts / shadcn chart)
- [ ] Таблица вопросов — сортировка по времени
- [ ] Лента последних сдач — клик → детали / ссылки
- [ ] Heatmap / matrix — пациенты × периоды, tooltip с датой
- [ ] Loading / error / empty states
- [ ] Интеграционные smoke: backend running + seeded data

#### Skills

| Skill | Фокус |
|-------|-------|
| `shadcn` | Card, Table, Chart |
| [vercel-react-best-practices](../.agents/skills/vercel-react-best-practices/SKILL.md) | charts, lists, memo |
| [nextjs-app-router-patterns](../.agents/skills/nextjs-app-router-patterns/SKILL.md) | server components для data |

#### Definition of Done

**Self-check (агент):** все блоки рендерятся на seed data; нет hardcoded mock в prod path; TypeScript strict.

**User-check (пользователь):** `make web-dev` + `make backend-run` + `make db-reset` → dashboard заполнен; KPI и график осмысленны.

### Документы

- 📋 [План итерации](impl/frontend/iteration-3-teacher-dashboard/plan.md) · [task-03 plan](impl/frontend/iteration-3-teacher-dashboard/tasks/task-03-teacher-dashboard/plan.md)

---

## Итерация 4: Лидерборд 📋

→ [iteration-4-leaderboard/plan.md](impl/frontend/iteration-4-leaderboard/plan.md)

### Цель

Страница `/leaderboard`: таблица и scatter plot.

### Задача 04

#### Состав работ

- [ ] Toggle «Таблица / Карта» (tabs)
- [ ] Таблица: rank, progress bar, иконки метрик, медали топ-3
- [ ] Scatter plot: ось X/Y по выбранным метрикам (из API)
- [ ] Responsive layout

#### Skills

| Skill | Фокус |
|-------|-------|
| `shadcn` | Tabs, Table, badges |
| [vercel-react-best-practices](../.agents/skills/vercel-react-best-practices/SKILL.md) | chart performance |
| [nextjs-app-router-patterns](../.agents/skills/nextjs-app-router-patterns/SKILL.md) | parallel routes / loading |

#### Definition of Done

**Self-check (агент):** оба режима работают на API; переключение без remount bugs.

**User-check (пользователь):** leaderboard открывается; топ-3 с медалями; scatter интерактивен (hover/tooltip).

### Документы

- 📋 [План итерации](impl/frontend/iteration-4-leaderboard/plan.md) · [task-04 plan](impl/frontend/iteration-4-leaderboard/plan.md)

---

## Итерация 5: Чат с ассистентом 📋

→ [iteration-5-assistant-chat/plan.md](impl/frontend/iteration-5-assistant-chat/plan.md)

### Цель

Страница чата: история переписки, отправка текста (и опционально фото).

### Задача 05

#### Состав работ

- [ ] UI чата: message list, input, send
- [ ] Интеграция `POST /api/v1/assistant/messages` (существующий контракт)
- [ ] Загрузка истории из backend *(endpoint list dialog requests — iter 1 или расширение v1)*
- [ ] Optimistic UI / error handling

#### Skills

| Skill | Фокус |
|-------|-------|
| `shadcn` | ScrollArea, Input, Button |
| [vercel-react-best-practices](../.agents/skills/vercel-react-best-practices/SKILL.md) | streaming, optimistic updates |
| [nextjs-app-router-patterns](../.agents/skills/nextjs-app-router-patterns/SKILL.md) | client component chat |

#### Definition of Done

**Self-check (агент):** send → reply; history persist после reload страницы (из PG).

**User-check (пользователь):** задать вопрос → ответ; история видна.

### Документы

- 📋 [План итерации](impl/frontend/iteration-5-assistant-chat/plan.md) · [task-05 plan](impl/frontend/iteration-5-assistant-chat/plan.md)

---

## Итерация 6: Чат в основной области (меню «Чат») 📋

→ [iteration-6-main-chat/plan.md](impl/frontend/iteration-6-main-chat/plan.md)

### Цель

Полноэкранный чат по пункту меню; переиспользование компонентов iter 5.

### Задача 06

#### Состав работ

- [ ] Route `/chat` — full-page chat
- [ ] Shared chat components с iter 5 и FAB widget
- [ ] Единая история (тот же dialog_id / user)

#### Skills

| Skill | Фокус |
|-------|-------|
| `shadcn` | Sheet / Dialog для FAB |
| [vercel-react-best-practices](../.agents/skills/vercel-react-best-practices/SKILL.md) | shared state, DRY |
| [nextjs-app-router-patterns](../.agents/skills/nextjs-app-router-patterns/SKILL.md) | layout reuse |

#### Definition of Done

**Self-check (агент):** FAB и `/chat` показывают одну историю; DRY components.

**User-check (пользователь):** сообщение из FAB видно на `/chat` и наоборот.

### Документы

- 📋 [План итерации](impl/frontend/iteration-6-main-chat/plan.md) · [task-06 plan](impl/frontend/iteration-6-main-chat/plan.md)

---

## Итерация 7: Ревью качества frontend 📋

→ [iteration-7-quality-review/plan.md](impl/frontend/iteration-7-quality-review/plan.md)

### Цель

Проверка best practices; исправление критичных замечаний.

### Задача 07

#### Состав работ

- [ ] Audit: [vercel-react-best-practices](../.agents/skills/vercel-react-best-practices/SKILL.md)
- [ ] Audit: [nextjs-app-router-patterns](../.agents/skills/nextjs-app-router-patterns/SKILL.md)
- [ ] Audit: `shadcn` — consistency, a11y
- [ ] Fix: критичные (data fetching, rerenders, bundle)
- [ ] `make web-lint` + `make web-build` green
- [ ] Краткий отчёт pass/warn/fix в `docs/tech/frontend-review.md`

#### Skills

| Skill | Фокус |
|-------|-------|
| [vercel-react-best-practices](../.agents/skills/vercel-react-best-practices/SKILL.md) | полный checklist |
| [nextjs-app-router-patterns](../.agents/skills/nextjs-app-router-patterns/SKILL.md) | routing, RSC boundaries |
| `shadcn` | component patterns, theme |

#### Definition of Done

**Self-check (агент):** review doc; нет open **Fix**; build/lint green.

**User-check (пользователь):** прочитать `frontend-review.md`; smoke всех страниц.

### Документы

- 📋 [План итерации](impl/frontend/iteration-7-quality-review/plan.md) · [task-07 plan](impl/frontend/iteration-7-quality-review/plan.md)

---

## Итерация 8: Голосовой режим чата 📋

→ [iteration-8-voice-chat/plan.md](impl/frontend/iteration-8-voice-chat/plan.md)

### Цель

Голосовой ввод/вывод в web и Telegram.

### Задача 08

#### Состав работ

- [ ] Web: Web Speech API или STT/TTS сервис; UI mic button
- [ ] Bot: voice message handler → backend assistant
- [ ] Fallback на текст при ошибке распознавания
- [ ] Документировать ограничения браузера / Telegram

#### Актуализация документации

| Файл | Что обновить |
|------|--------------|
| `docs/integrations.md` | voice providers |
| `docs/tasks/tasklist-bot.md` | voice handler *(при изменении bot)* |

#### Definition of Done

**Self-check (агент):** web voice → текст → assistant → ответ; bot voice roundtrip на test fixture.

**User-check (пользователь):** записать голос в web; отправить voice в Telegram bot.

### Документы

- 📋 [План итерации](impl/frontend/iteration-8-voice-chat/plan.md) · [task-08 plan](impl/frontend/iteration-8-voice-chat/plan.md)

---

## Итерация 9: Text-to-SQL 📋

→ [iteration-9-text-to-sql/plan.md](impl/frontend/iteration-9-text-to-sql/plan.md)

### Цель

Ответы на вопросы по данным БД; архитектура и реализация.

### Задача 09

#### Состав работ

- [ ] ADR / spec: варианты (LLM → SQL → read-only query; guardrails, allowlist tables)
- [ ] Backend endpoint или расширение assistant с tool `query_analytics`
- [ ] Frontend: UI «вопрос по данным» + отображение таблицы/графика
- [ ] Тест-сценарии (golden questions + expected shape)
- [ ] **Out of scope MVP:** write SQL, destructive queries

#### Актуализация документации

| Файл | Что обновить |
|------|--------------|
| `docs/adr/adr-NNN-text-to-sql.md` | **создать** |
| `docs/spec/text-to-sql-scenarios.md` | **создать** |

#### Definition of Done

**Self-check (агент):** ADR принят; 3+ сценария проходят на seed; SQL только SELECT; timeouts.

**User-check (пользователь):** задать «сколько ХЕ за неделю у пациента X» — осмысленный ответ из PG.

### Документы

- 📋 [План итерации](impl/frontend/iteration-9-text-to-sql/plan.md) · [task-09 plan](impl/frontend/iteration-9-text-to-sql/plan.md)

---

## Критерии завершения области (все 10 итераций)

| Итерация | Критерий | Проверка |
|----------|----------|----------|
| 0 | UI spec + frontend API contracts | ✅ `frontend-requirements.md`, `frontend-contract.md`, [review](../api/api-contract-review.md) |
| 1 | Backend API + demo seed | curl; skills: api-design, fastapi-templates, modern-python, pg/sharp-edges *при схеме* |
| 2 | Next.js scaffold | `make web-dev`; skills: shadcn, vercel, nextjs |
| 3 | Dashboard | live API; skills: shadcn, vercel, nextjs |
| 4 | Leaderboard | table + scatter; skills: shadcn, vercel, nextjs |
| 5–6 | Chat | history + send; skills: shadcn, vercel, nextjs |
| 7 | Quality review | `frontend-review.md`; skills: shadcn, vercel, nextjs |
| 8 | Voice | web + bot smoke |
| 9 | Text-to-SQL | ADR + 3 scenarios on PG |

## Связанные документы

| Документ | Назначение |
|----------|------------|
| [tasklist-web.md](tasklist-web.md) | краткий обзор *(legacy; детализация — этот файл)* |
| [tasklist-backend.md](tasklist-backend.md) | analytics API 09–12 |
| [tasklist-database.md](tasklist-database.md) | PG schema ✅ |
| [frontend-requirements.md](../spec/frontend-requirements.md) | UI 4 зоны (iter 0 ✅) |
| [frontend-contract.md](../api/frontend-contract.md) | Web API (iter 0 ✅) |
| [api-contract.md](../api/api-contract.md) | REST v1 bot + web |
| [api-contract-review.md](../api/api-contract-review.md) | Design review iter 0 |
| [templates/workflow.md](../templates/workflow.md) | plan/summary workflow |
| [web/package.json](../../web/package.json) | engines, pnpm |
