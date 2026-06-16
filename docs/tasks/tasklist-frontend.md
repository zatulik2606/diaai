# Frontend Tasklist

Опирается на [plan.md](../plan.md) · [vision.md](../vision.md) · [data-model.md](../data-model.md) · [api-contract.md](../api/api-contract.md) · [spec/user-scenarios.md](../spec/user-scenarios.md)

## Обзор

Рабочий план области **frontend** (`web/`): Next.js App Router + TypeScript + shadcn/ui + Tailwind + pnpm. Тонкий клиент backend REST API ([vision.md](../vision.md)); данные — PostgreSQL через `/api/v1/web/*`.

**Маппинг UI → домен diaai** (зафиксирован iter 0 → [frontend-requirements.md](../spec/frontend-requirements.md)):

| Зона UI (ТЗ) | Роль / домен diaai |
|--------------|-------------------|
| Экран 1 — панель | Панель **пациента с диабетом** — KPI, активность, вопросы, фиксации, матрица прогресса (ХЕ, БЖЕ, инсулин) |
| Экран 2 — лидерборд | Рейтинг **пациентов с диабетом** (doctor + diabetic): таблица / scatter; продукты, ХЕ, топ-5 БЖЕ медалями |
| Глобальный чат (FAB) | Диалог с **ассистентом** (сценарий D2) |
| Матрица «студенты × уроки» | **Пациенты × периоды/метрики** (`progress_snapshots`) |

**Текущее состояние:** spec UI ✅ (iter 0) · backend web API ✅ (iter 1) · web scaffold ✅ (iter 2) · patient dashboard ✅ (iter 3) · **leaderboard** ✅ (iter 4) · routes: `/dashboard`, `/leaderboard`.

**Прогресс:** **5 / 10** итераций ✅ · **5 / 10** задач ✅ · **следующая:** iter 5 — [чат с ассистентом](impl/frontend/iteration-5-assistant-chat/plan.md) · [plan области](impl/frontend/plan.md) · [summary области](impl/frontend/summary.md)

**Зависимости:**

| Область | Статус | Нужно frontend'у |
|---------|--------|------------------|
| Backend MVP (assistant, events) | ✅ | чат, события |
| Database iter 5 (9 таблиц) | ✅ | analytics, snapshots |
| Backend iter 4 (analytics API) | ✅ | leaderboard DTO (`products` + `bje_medal`, patient access) |

## Стек

| Слой | Выбор |
|------|--------|
| Framework | Next.js (App Router) + React |
| Язык | TypeScript |
| UI | shadcn/ui |
| Styling | Tailwind CSS |
| Package manager | pnpm (corepack) |
| Node | 20+; dev pin — `web/.nvmrc` → 24 |

**Toolchain + scaffold (iter 2 ✅):**

```
web/
├── .nvmrc, .npmrc, package.json   # engines, pnpm 11.6
├── app/(auth)/login, app/(app)/   # route groups
├── app/api/auth/                  # BFF login/logout
├── components/ui/, components/    # shadcn + shell
├── lib/                           # session, backend-client
├── middleware.ts
└── Makefile web-* (корень)
```

Локально: `cd web && nvm use && corepack enable && corepack prepare pnpm@11.6.0 --activate`

## Skills (дополнительные проверки)

Подбор других skills — `/find-skills`.

| Skill | Когда | Фокус |
|-------|-------|-------|
| [api-design-principles](../.agents/skills/api-design-principles/SKILL.md) | iter 0, **iter 1** | REST design, ошибки, примеры |
| [fastapi-templates](../.agents/skills/fastapi-templates/SKILL.md) | **iter 1** | handler → service → repo |
| [modern-python](../.agents/skills/modern-python/SKILL.md) | **iter 1** | uv, ruff, async |
| [postgresql-table-design](../.agents/skills/postgresql-table-design/SKILL.md) | **iter 1** | миграции, индексы |
| [sharp-edges](../.agents/skills/sharp-edges/SKILL.md) | **iter 1** | auth, secrets |
| [shadcn](../.agents/skills/shadcn/SKILL.md) | **iter 2–7** | init, theme, components |
| [vercel-react-best-practices](../.agents/skills/vercel-react-best-practices/SKILL.md) | **iter 2–7** | RSC, fetching, bundle |
| [nextjs-app-router-patterns](../.agents/skills/nextjs-app-router-patterns/SKILL.md) | **iter 2–7** | layouts, routes, middleware |

## Make-команды

| Команда | Действие | Итерация |
|---------|----------|----------|
| `make web-install` | `cd web && pnpm install` | 2 |
| `make web-dev` | `cd web && pnpm dev` (:3000) | 2 |
| `make web-build` | `cd web && pnpm build` | 2+ |
| `make web-lint` | `cd web && pnpm lint` | 2+ |
| `make backend-run` | FastAPI :8000 | 1+ |
| `make db-reset` | migrate + seed v3 | 1+ |
| `make db-inspect` | counts по ролям/таблицам | 1+ |

*Целевые `web-*` — в корневом `Makefile`.*

## Итерации

Сводный план: [impl/frontend/plan.md](impl/frontend/plan.md) · [summary](impl/frontend/summary.md)

| # | Название | Задача | Статус | Документы |
|---|----------|--------|--------|-----------|
| 0 | Требования UI и API-контракты | 00 | ✅ Done | [plan](impl/frontend/iteration-0-ui-contracts/plan.md) · [summary](impl/frontend/iteration-0-ui-contracts/summary.md) |
| 1 | API для frontend | 01 | ✅ Done | [plan](impl/frontend/iteration-1-frontend-api/plan.md) · [summary](impl/frontend/iteration-1-frontend-api/summary.md) |
| 2 | Каркас frontend | 02 | ✅ Done | [plan](impl/frontend/iteration-2-scaffold/plan.md) · [summary](impl/frontend/iteration-2-scaffold/summary.md) |
| 3 | Панель пациента с диабетом | 03 | ✅ Done | [plan](impl/frontend/iteration-3-patient-dashboard/plan.md) · [summary](impl/frontend/iteration-3-patient-dashboard/summary.md) |
| 4 | Лидерборд | 04 | ✅ Done | [plan](impl/frontend/iteration-4-leaderboard/plan.md) · [summary](impl/frontend/iteration-4-leaderboard/summary.md) |
| 5 | Чат с ассистентом | 05 | 📋 Next | [plan](impl/frontend/iteration-5-assistant-chat/plan.md) |
| 6 | Чат в основной области | 06 | 📋 Planned | [plan](impl/frontend/iteration-6-main-chat/plan.md) |
| 7 | Ревью качества | 07 | 📋 Planned | [plan](impl/frontend/iteration-7-quality-review/plan.md) |
| 8 | Голосовой режим | 08 | 📋 Planned | [plan](impl/frontend/iteration-8-voice-chat/plan.md) |
| 9 | Text-to-SQL | 09 | 📋 Planned | [plan](impl/frontend/iteration-9-text-to-sql/plan.md) |

## Связь с plan.md

| plan.md | Frontend tasklist | Зависимости |
|---------|-------------------|-------------|
| [Итерация 5 — веб](../plan.md#итерация-5--веб-интерфейс-пациент-с-диабетом--доктор) | итерации 0–9 | backend + database ✅ |
| [Итерация 4 — аналитика](../plan.md#итерация-4--аналитика-и-динамика-состояния) | iter 1, 3, 4 | [tasklist-backend](tasklist-backend.md) 09–12 |

## Легенда статусов

- 📋 Planned — запланирован
- 🚧 In Progress / Next — в работе или следующий
- ✅ Done — завершён

## Список задач

| Задача | Описание | Статус | Документы |
|--------|----------|--------|-----------|
| 00 | UI-требования и API-контракты frontend | ✅ Done | [план](impl/frontend/iteration-0-ui-contracts/tasks/task-00-ui-contracts/plan.md) · [summary](impl/frontend/iteration-0-ui-contracts/tasks/task-00-ui-contracts/summary.md) |
| 01 | Backend API + demo seed для UI | ✅ Done | [план](impl/frontend/iteration-1-frontend-api/tasks/task-01-frontend-api/plan.md) · [summary](impl/frontend/iteration-1-frontend-api/tasks/task-01-frontend-api/summary.md) |
| 02 | Каркас Next.js + layout + auth | ✅ Done | [план](impl/frontend/iteration-2-scaffold/tasks/task-02-scaffold/plan.md) · [summary](impl/frontend/iteration-2-scaffold/tasks/task-02-scaffold/summary.md) |
| 03 | Панель пациента с диабетом (`/dashboard`) | ✅ Done | [план](impl/frontend/iteration-3-patient-dashboard/plan.md) · [summary](impl/frontend/iteration-3-patient-dashboard/tasks/task-03-patient-dashboard/summary.md) |
| 04 | Лидерборд | ✅ Done | [план](impl/frontend/iteration-4-leaderboard/tasks/task-04-leaderboard/plan.md) · [summary](impl/frontend/iteration-4-leaderboard/tasks/task-04-leaderboard/summary.md) |
| 05 | Чат с ассистентом (FAB / страница) | 📋 Next | [план](impl/frontend/iteration-5-assistant-chat/tasks/task-05-assistant-chat/plan.md) |
| 06 | Чат в меню «Чат» | 📋 Planned | [план](impl/frontend/iteration-6-main-chat/tasks/task-06-main-chat/plan.md) |
| 07 | Ревью качества frontend | 📋 Planned | [план](impl/frontend/iteration-7-quality-review/tasks/task-07-quality-review/plan.md) |
| 08 | Голосовой режим (web + bot) | 📋 Planned | [план](impl/frontend/iteration-8-voice-chat/tasks/task-08-voice-chat/plan.md) |
| 09 | Text-to-SQL по данным БД | 📋 Planned | [план](impl/frontend/iteration-9-text-to-sql/tasks/task-09-text-to-sql/plan.md) |

Итерации выполняются **последовательно** (0 → 9).

---

## Итерация 0: Требования к UI и API-контракты ✅

→ [iteration-0-ui-contracts/plan.md](impl/frontend/iteration-0-ui-contracts/plan.md)

### Цель

Зафиксировать функциональные требования к четырём зонам UI, общий стиль, вход и REST-контракты для всех экранов.

### Задача 00

#### Состав работ

- [x] **Экран 1 — панель пациента с диабетом:** 4 KPI с дельтой; график активности 14 дней; лента вопросов (время, вопрос + ответ); лента фиксаций (клик → детали); матрица прогресса (ХЕ, БЖЕ, инсулин; периоды)
- [x] **Экран 2 — лидерборд:** переключатель таблица / scatter plot; таблица — место, progress bar, иконки по потребляемым продуктам и количеству ХЕ; медальки топ-5 по БЖЕ на эти продукты
- [x] **Глобальный чат:** плавающая кнопка (FAB) на всех экранах
- [x] **Стиль UI:** тёмная тема, dev-эстетика (ориентир [tbench.ai](https://www.tbench.ai/))
- [x] **Вход:** без сложной авторизации — ввод Telegram username
- [x] API-контракты для всех экранов: endpoint'ы, query/body, примеры JSON
- [x] Сверка с [user-scenarios.md](../spec/user-scenarios.md), [data-model.md](../data-model.md), [api-contract.md](../api/api-contract.md)

#### Skills

| Skill | Фокус |
|-------|-------|
| [api-design-principles](../.agents/skills/api-design-principles/SKILL.md) | review контрактов; pass/warn/fix |

#### Актуализация документации

| Файл | Что обновлено |
|------|---------------|
| [docs/spec/frontend-requirements.md](../spec/frontend-requirements.md) | 4 зоны, wireframes, auth |
| [docs/spec/frontend-design-system.md](../spec/frontend-design-system.md) | tbench dark, tokens |
| [docs/api/frontend-contract.md](../api/frontend-contract.md) | web endpoint'ы, JSON |
| [docs/api/openapi.yaml](../api/openapi.yaml) | tag `web` |
| [docs/api/api-contract.md](../api/api-contract.md) | web-секция |
| [docs/api/api-contract-review.md](../api/api-contract-review.md) | api-design-principles review |
| [docs/integrations.md](../integrations.md) | web client |

#### Definition of Done

**Self-check (агент):** spec покрывает 4 зоны; контракты согласованы с data-model; нет противоречий с api v1; review в [api-contract-review.md](../api/api-contract-review.md).

**User-check (пользователь):** открыть `frontend-requirements.md` и `frontend-contract.md` — понятно содержание каждого экрана; вход через username описан.

### Документы

- ✅ [План итерации](impl/frontend/iteration-0-ui-contracts/plan.md) · [Summary](impl/frontend/iteration-0-ui-contracts/summary.md)

---

## Итерация 1: Реализация API для frontend ✅

→ [iteration-1-frontend-api/plan.md](impl/frontend/iteration-1-frontend-api/plan.md)

**Зона:** backend + database *(координация с [tasklist-backend.md](tasklist-backend.md))*

### Цель

Проверить достаточность данных, реализовать endpoint'ы для всех экранов, подготовить demo seed.

### Задача 01

#### Состав работ

- [x] Gap analysis: data-model + iter 0 контракты → недостающие поля/таблицы
- [x] Новые endpoint'ы: dashboard KPI, activity, questions, submissions, progress matrix, leaderboard, assistant history, auth resolve
- [x] Миграция `003_telegram_username` + seed v3 для demo-наполнения
- [x] Добавить доктора в БД: `@doctor_ivanov`, `telegram_id: 162684825`, `role: doctor`
- [x] Contract tests (`backend/tests/test_web_api.py`)
- [x] Обновить [docs/tech/api-contracts.md](../tech/api-contracts.md), [backend/README.md](../../backend/README.md)

#### Skills

| Skill | Фокус |
|-------|-------|
| [api-design-principles](../.agents/skills/api-design-principles/SKILL.md) | контракты ↔ impl |
| [fastapi-templates](../.agents/skills/fastapi-templates/SKILL.md) | слои, DI |
| [modern-python](../.agents/skills/modern-python/SKILL.md) | uv/ruff |
| [postgresql-table-design](../.agents/skills/postgresql-table-design/SKILL.md) | миграция 003 |
| [sharp-edges](../.agents/skills/sharp-edges/SKILL.md) | auth, secrets |

#### Make-команды

```bash
make db-reset && make db-inspect
make lint && make test
make backend-run   # curl smoke 8 web endpoints
```

#### Definition of Done

**Self-check (агент):** миграция 003; seed idempotent; 8 endpoint'ов 200 + schema; doctor `@doctor_ivanov` в PG; `make test` green; skills review.

**User-check (пользователь):** `make db-inspect` — demo counts; `make backend-run` + curl dashboard/leaderboard — JSON по контракту.

### Документы

- ✅ [План итерации](impl/frontend/iteration-1-frontend-api/plan.md) · [Summary](impl/frontend/iteration-1-frontend-api/summary.md)

---

## Итерация 2: Каркас frontend-проекта ✅

→ [iteration-2-scaffold/plan.md](impl/frontend/iteration-2-scaffold/plan.md)

### Цель

Инициализировать Next.js App Router + shadcn/ui + Tailwind; настроить тему, вход, layout, make-команды.

### Задача 02

#### Состав работ

- [x] Plan-артефакты iter 2 + task 02 ([plan](impl/frontend/iteration-2-scaffold/plan.md), [summary](impl/frontend/iteration-2-scaffold/summary.md))
- [x] `pnpm create next-app` в `web/` — Next.js 16.2.9, React 19, Tailwind 4, ESLint (default template)
- [x] shadcn/ui init; базовые компоненты (Button, Card, Table, Chart wrapper)
- [x] Тёмная тема (CSS variables); ориентир tbench dev-style
- [x] Вход: форма Telegram username → BFF → session (httpOnly cookie); header: user info + logout
- [x] Layout: sidebar/nav (Dashboard, Leaderboard, Chat); **FAB глобального чата**
- [x] API client (server BFF; `BACKEND_URL` + `BACKEND_SERVICE_TOKEN` только на сервере)
- [x] Makefile: `web-install`, `web-dev`, `web-build`, `web-lint`
- [x] `web/README.md` — quick start

#### Skills

| Skill | Фокус |
|-------|-------|
| [shadcn](../.agents/skills/shadcn/SKILL.md) | init, theme, компоненты |
| [vercel-react-best-practices](../.agents/skills/vercel-react-best-practices/SKILL.md) | app/, data fetching |
| [nextjs-app-router-patterns](../.agents/skills/nextjs-app-router-patterns/SKILL.md) | layout, routes, middleware |

#### Актуализация документации

| Файл | Что обновить |
|------|--------------|
| [README.md](../../README.md) | секция web quick start |
| [docs/integrations.md](../integrations.md) | web → backend env |
| [.env.example](../../.env.example) | `NEXT_PUBLIC_BACKEND_URL` (iter 3+) |
| [web/README.md](../../web/README.md) | заменить default Next README на diaai quick start |

#### Make-команды

```bash
make web-install && make web-dev
make web-lint && make web-build
```

#### Definition of Done

**Self-check (агент):** `make web-dev` — app на :3000; навигация; FAB виден; login/logout; lint/build green.

**User-check (пользователь):** login пациента из seed → `/dashboard`; `doctor_ivanov` → `/leaderboard`; навигация, FAB, logout.

### Документы

- ✅ [План итерации](impl/frontend/iteration-2-scaffold/plan.md) · [Summary](impl/frontend/iteration-2-scaffold/summary.md) · [task-02 plan](impl/frontend/iteration-2-scaffold/tasks/task-02-scaffold/plan.md) · [task-02 summary](impl/frontend/iteration-2-scaffold/tasks/task-02-scaffold/summary.md)

---

## Итерация 3: Панель пациента с диабетом ✅

→ [iteration-3-patient-dashboard/plan.md](impl/frontend/iteration-3-patient-dashboard/plan.md)

### Цель

Страница `/dashboard` для роли `diabetic`: личные KPI, график активности, вопросы ассистенту, фиксации, матрица прогресса (D1, D3).

### Задача 03

#### Состав работ

- [x] Plan-артефакты iter 3 + task 03 ([plan](impl/frontend/iteration-3-patient-dashboard/plan.md), [summary](impl/frontend/iteration-3-patient-dashboard/summary.md))
- [x] 4 KPI-карточки с дельтой — данные **текущего пользователя** (ХЕ, вопросы, события питания, инсулин)
- [x] Line chart — активность 14 дней (вопросы + food events по `telegram_id` из сессии)
- [x] Таблица своих вопросов ассистенту — сортировка по времени
- [x] Лента своих фиксаций (food / photo) — клик → детали
- [x] Матрица прогресса — периоды × метрики (ХЕ, БЖЕ, инсулин) для пациента
- [x] Backend: patient-scoped API `/patient/dashboard/*`
- [x] Loading / error / empty states
- [x] Smoke: `make backend-run` + login пациента из seed

#### Skills

| Skill | Фокус |
|-------|-------|
| [shadcn](../.agents/skills/shadcn/SKILL.md) | Card, Table, Chart |
| [vercel-react-best-practices](../.agents/skills/vercel-react-best-practices/SKILL.md) | charts, lists |
| [nextjs-app-router-patterns](../.agents/skills/nextjs-app-router-patterns/SKILL.md) | server data fetching |

#### Актуализация документации

| Файл | Что обновить |
|------|--------------|
| [frontend-requirements.md](../spec/frontend-requirements.md) | экран 1 — панель пациента |
| [frontend-contract.md](../api/frontend-contract.md) | patient dashboard endpoints *(при добавлении)* |
| [web/README.md](../../web/README.md) | dashboard smoke |

#### Definition of Done

**Self-check (агент):** dashboard рендерит данные залогиненного пациента; нет hardcoded mock; TypeScript strict; `make web-build` green.

**User-check (пользователь):** login пациента из seed → `/dashboard` заполнен; KPI и график отражают его активность.

### Документы

- ✅ [План итерации](impl/frontend/iteration-3-patient-dashboard/plan.md) · [Summary](impl/frontend/iteration-3-patient-dashboard/summary.md) · [task-03 plan](impl/frontend/iteration-3-patient-dashboard/tasks/task-03-patient-dashboard/plan.md) · [task-03 summary](impl/frontend/iteration-3-patient-dashboard/tasks/task-03-patient-dashboard/summary.md)

---

## Итерация 4: Лидерборд ✅

→ [iteration-4-leaderboard/plan.md](impl/frontend/iteration-4-leaderboard/plan.md) · [summary](impl/frontend/iteration-4-leaderboard/summary.md)

### Цель

Страница `/leaderboard` (doctor + diabetic): таблица / scatter; продукты, ХЕ, топ-5 БЖЕ с медалями; подсветка строки пациента.

### Подготовка ✅

- [x] Спека экрана 2: продукты + ХЕ, медали топ-5 БЖЕ (`frontend-requirements.md`, `frontend-design-system.md`)
- [x] Контракт leaderboard DTO: `products[]`, `bje_medal` (`frontend-contract.md`, `api-contract.md`, `openapi.yaml`)
- [x] План итерации + task 04
- [x] Summary итерации
- [x] Demo doctor `doctor_ivanov` синхронизирован в docs/smoke

### Задача 04 ✅

#### Состав работ (реализация)

- [x] Backend: `products[]` + `bje_medal`, убрать legacy `metrics`/`medal`
- [x] Переключатель «Таблица / Карта» (tabs)
- [x] Таблица: место (rank), progress bar, иконки по потребляемым продуктам и количеству ХЕ
- [x] Медальки топ-5 по БЖЕ на эти продукты
- [x] Scatter plot по метрикам из API
- [x] Блок «Топ-5 продуктов когорты по БЖЕ» + emoji-медали на чипах
- [x] Доступ пациента: API `patient_telegram_id`, nav, подсветка своей строки
- [x] Responsive layout + loading/error states

#### Skills

| Skill | Фокус |
|-------|-------|
| [shadcn](../.agents/skills/shadcn/SKILL.md) | Tabs, Table, Badge |
| [vercel-react-best-practices](../.agents/skills/vercel-react-best-practices/SKILL.md) | chart performance |
| [nextjs-app-router-patterns](../.agents/skills/nextjs-app-router-patterns/SKILL.md) | loading states |

#### Definition of Done

**Self-check (агент):** оба режима на API; переключение без remount bugs; `make backend-test` (53 passed); `make web-build` green.

**User-check (пользователь):** `doctor_ivanov` → `/leaderboard`: топ-5 БЖЕ, медали на чипах, scatter; `ivan_p` → `/leaderboard`: рейтинг когорты, подсветка своей строки.

### Документы

- ✅ [План итерации](impl/frontend/iteration-4-leaderboard/plan.md) · [summary](impl/frontend/iteration-4-leaderboard/summary.md) · [task-04 plan](impl/frontend/iteration-4-leaderboard/tasks/task-04-leaderboard/plan.md) · [task-04 summary](impl/frontend/iteration-4-leaderboard/tasks/task-04-leaderboard/summary.md)

---

## Итерация 5: Чат с ассистентом 📋 Next

→ [iteration-5-assistant-chat/plan.md](impl/frontend/iteration-5-assistant-chat/plan.md)

### Цель

FAB-виджет и/или страница чата: история переписки, отправка текста.

### Задача 05

#### Состав работ

- [ ] UI чата: message list, input, send
- [ ] `GET /api/v1/web/assistant/history` — загрузка истории
- [ ] `POST /api/v1/assistant/messages` — отправка (BFF)
- [ ] Optimistic UI / error handling

#### Skills

| Skill | Фокус |
|-------|-------|
| [shadcn](../.agents/skills/shadcn/SKILL.md) | Sheet, ScrollArea, Input |
| [vercel-react-best-practices](../.agents/skills/vercel-react-best-practices/SKILL.md) | optimistic updates |
| [nextjs-app-router-patterns](../.agents/skills/nextjs-app-router-patterns/SKILL.md) | client chat |

#### Definition of Done

**Self-check (агент):** send → reply; history после reload из PG.

**User-check (пользователь):** задать вопрос → ответ; история видна в FAB.

### Документы

- 📋 [План итерации](impl/frontend/iteration-5-assistant-chat/plan.md) · [task-05 plan](impl/frontend/iteration-5-assistant-chat/tasks/task-05-assistant-chat/plan.md)

---

## Итерация 6: Чат в основной области (меню «Чат») 📋

→ [iteration-6-main-chat/plan.md](impl/frontend/iteration-6-main-chat/plan.md)

### Цель

Полноэкранный чат по пункту меню; переиспользование компонентов iter 5.

### Задача 06

#### Состав работ

- [ ] Route `/chat` — full-page chat
- [ ] Shared components с FAB (iter 5)
- [ ] Единая история (тот же user / dialog)

#### Skills

| Skill | Фокус |
|-------|-------|
| [shadcn](../.agents/skills/shadcn/SKILL.md) | layout reuse |
| [vercel-react-best-practices](../.agents/skills/vercel-react-best-practices/SKILL.md) | DRY, shared state |
| [nextjs-app-router-patterns](../.agents/skills/nextjs-app-router-patterns/SKILL.md) | route groups |

#### Definition of Done

**Self-check (агент):** FAB и `/chat` — одна история; DRY components.

**User-check (пользователь):** сообщение из FAB видно на `/chat` и наоборот.

### Документы

- 📋 [План итерации](impl/frontend/iteration-6-main-chat/plan.md) · [task-06 plan](impl/frontend/iteration-6-main-chat/tasks/task-06-main-chat/plan.md)

---

## Итерация 7: Ревью качества frontend 📋

→ [iteration-7-quality-review/plan.md](impl/frontend/iteration-7-quality-review/plan.md)

### Цель

Проверка best practices; исправление критичных замечаний.

### Задача 07

#### Состав работ

- [ ] Audit: [vercel-react-best-practices](../.agents/skills/vercel-react-best-practices/SKILL.md)
- [ ] Audit: [nextjs-app-router-patterns](../.agents/skills/nextjs-app-router-patterns/SKILL.md)
- [ ] Audit: [shadcn](../.agents/skills/shadcn/SKILL.md) — consistency, a11y
- [ ] Fix критичных (data fetching, rerenders, bundle)
- [ ] `make web-lint` + `make web-build` green
- [ ] Отчёт pass/warn/fix в `docs/tech/frontend-review.md`

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

- [ ] Web: Web Speech API или STT/TTS; UI mic button
- [ ] Bot: voice message handler → backend assistant
- [ ] Fallback на текст при ошибке распознавания
- [ ] Документировать ограничения браузера / Telegram

#### Актуализация документации

| Файл | Что обновить |
|------|--------------|
| [docs/integrations.md](../integrations.md) | voice providers |
| [docs/tasks/tasklist-bot.md](tasklist-bot.md) | voice handler *(при изменении bot)* |

#### Definition of Done

**Self-check (агент):** web voice → текст → assistant → ответ; bot voice roundtrip.

**User-check (пользователь):** записать голос в web; отправить voice в Telegram bot.

### Документы

- 📋 [План итерации](impl/frontend/iteration-8-voice-chat/plan.md) · [task-08 plan](impl/frontend/iteration-8-voice-chat/tasks/task-08-voice-chat/plan.md)

---

## Итерация 9: Text-to-SQL 📋

→ [iteration-9-text-to-sql/plan.md](impl/frontend/iteration-9-text-to-sql/plan.md)

### Цель

Ответы на вопросы по данным БД; проработка архитектуры и реализация.

### Задача 09

#### Состав работ

- [ ] ADR / spec: варианты (LLM → SQL → read-only; guardrails, allowlist tables)
- [ ] Backend endpoint или tool `query_analytics` в assistant
- [ ] Frontend: UI «вопрос по данным» + таблица/график
- [ ] Тест-сценарии (golden questions)
- [ ] **Out of scope:** write SQL, destructive queries

#### Актуализация документации

| Файл | Что обновить |
|------|--------------|
| `docs/adr/adr-NNN-text-to-sql.md` | **создать** |
| `docs/spec/text-to-sql-scenarios.md` | **создать** |

#### Definition of Done

**Self-check (агент):** ADR принят; 3+ сценария на seed; SQL только SELECT; timeouts.

**User-check (пользователь):** «сколько ХЕ за неделю у пациента X» — осмысленный ответ из PG.

### Документы

- 📋 [План итерации](impl/frontend/iteration-9-text-to-sql/plan.md) · [task-09 plan](impl/frontend/iteration-9-text-to-sql/tasks/task-09-text-to-sql/plan.md)

---

## Критерии завершения области (все 10 итераций)

| Итерация | Критерий | Проверка |
|----------|----------|----------|
| 0 | UI spec + frontend API contracts | ✅ `frontend-requirements.md`, `frontend-contract.md` |
| 1 | Backend API + demo seed | ✅ 8 endpoints, `@doctor_ivanov`, seed v3 |
| 2 | Next.js scaffold | ✅ auth BFF, shell, FAB, `make web-*` |
| 3 | Панель пациента с диабетом | live API, patient dashboard UI | ✅ `/dashboard` + `/patient/dashboard/*` |
| 4 | Leaderboard | table/scatter, продукты+ХЕ, топ-5 БЖЕ, doctor+diabetic | ✅ `/leaderboard` + products DTO + patient row highlight |
| 5–6 | Chat | history + send; FAB + `/chat` |
| 7 | Quality review | `frontend-review.md` |
| 8 | Voice | web + bot smoke |
| 9 | Text-to-SQL | ADR + 3 scenarios |

## Связанные документы

| Документ | Назначение |
|----------|------------|
| [tasklist-backend.md](tasklist-backend.md) | backend + analytics 09–12 |
| [tasklist-database.md](tasklist-database.md) | PG schema ✅ |
| [frontend-requirements.md](../spec/frontend-requirements.md) | UI 4 зоны |
| [frontend-contract.md](../api/frontend-contract.md) | Web API |
| [api-contract.md](../api/api-contract.md) | REST v1 |
| [templates/tasklist.md](../templates/tasklist.md) | формат tasklist |
| [templates/workflow.md](../templates/workflow.md) | plan/summary workflow |
| [web/package.json](../../web/package.json) | engines, pnpm |
