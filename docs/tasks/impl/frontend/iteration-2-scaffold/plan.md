# Итерация frontend 2: Каркас frontend

Опирается на [tasklist-frontend.md](../../../tasklist-frontend.md) · [impl/frontend/plan.md](../plan.md) · [frontend-requirements.md](../../../../spec/frontend-requirements.md) · [frontend-design-system.md](../../../../spec/frontend-design-system.md) · [frontend-contract.md](../../../../api/frontend-contract.md)

Skills: [shadcn](../../../../.agents/skills/shadcn/SKILL.md) · [vercel-react-best-practices](../../../../.agents/skills/vercel-react-best-practices/SKILL.md) · [nextjs-app-router-patterns](../../../../.agents/skills/nextjs-app-router-patterns/SKILL.md)

**Статус:** ✅ Done · [summary](summary.md) в `web/` с тёмной темой tbench, входом по Telegram username (BFF), app shell с навигацией и FAB-заглушкой — без fetch dashboard/leaderboard (iter 3–4).

## Ценность

- Web-клиент на :3000 — база для iter 3–6
- Auth через iter 1: `POST /api/v1/web/auth/resolve`; demo `doctor_ivanov` / `162684825`
- Единый shell: sidebar, header, FAB; iter 3+ только подключают API

## Зависимости

| Область | Статус | Нужно iter 2 |
|---------|--------|--------------|
| Frontend iter 0 (spec, design system) | ✅ | routes, auth, FAB, tokens |
| Frontend iter 1 (web API) | ✅ | auth/resolve, seed v3 |
| Backend running | ✅ | `make backend-run` :8000 |
| `web/` Next.js | 🚧 partial | см. gap analysis |

**Зона работ:** `web/` + Makefile + docs. **Не** backend, **не** dashboard data.

## Gap analysis (текущее → целевое)

| Блок | Сейчас в `web/` | Целевое iter 2 | Действие |
|------|-----------------|----------------|----------|
| Next.js scaffold | ✅ 16.2.9, App Router, TW4, default `page.tsx` | diaai routes | replace welcome page |
| Toolchain | ✅ `.nvmrc`, `engines`, pnpm 11.6 | — | — |
| shadcn/ui | ❌ | `components/ui/*`, `components.json` | init + add components |
| Design tokens | ❌ Geist, light/dark media query | tbench HSL tokens S1–S13 | `globals.css` + Inter/JetBrains |
| Auth BFF | ❌ | `/api/auth/login`, `/api/auth/logout` | Route Handlers |
| Session | ❌ | httpOnly `diaai_session` | `lib/session.ts` |
| Backend client | ❌ | server-only fetch + Bearer | `lib/backend-client.ts` |
| Middleware | ❌ | auth guard, role redirects | `middleware.ts` |
| Login | ❌ | `/login` form | `(auth)/login/page.tsx` |
| App shell | ❌ | sidebar 240px, header, mobile Sheet | `(app)/layout.tsx` |
| Routes | ❌ only `/` | `/dashboard`, `/leaderboard`, `/chat` placeholders | route groups |
| FAB | ❌ | 56×56 Sheet stub | `chat-fab.tsx` |
| Makefile | ❌ | `web-install/dev/build/lint` | root `Makefile` |
| Env | ❌ | `web/.env.example`, `.env.local` | create |
| Docs | ❌ default Next README | diaai quick start | `web/README.md`, root README |

## Архитектура

```mermaid
flowchart LR
  subgraph browser [Browser]
    LoginPage["/login"]
    AppShell["AppShell + FAB"]
  end
  subgraph next [Next.js BFF]
    LoginRoute["POST /api/auth/login"]
    LogoutRoute["POST /api/auth/logout"]
    Middleware["middleware.ts"]
    SessionCookie["httpOnly diaai_session"]
  end
  subgraph backend [Backend iter1]
    Resolve["POST /api/v1/web/auth/resolve"]
  end
  LoginPage --> LoginRoute
  LoginRoute -->|"Bearer BACKEND_SERVICE_TOKEN"| Resolve
  LoginRoute --> SessionCookie
  Middleware --> SessionCookie
  AppShell --> Middleware
```

### Ключевые решения

| # | Решение | Обоснование |
|---|---------|-------------|
| 1 | BFF-only auth | `BACKEND_SERVICE_TOKEN` не в browser bundle |
| 2 | httpOnly cookie session | MVP без JWT; безопаснее localStorage |
| 3 | Route groups `(auth)` / `(app)` | public login vs protected shell |
| 4 | Role matrix | `diabetic`: Dashboard+Chat; `doctor`: Leaderboard+Chat |
| 5 | Placeholder pages | iter 2 = каркас, API fetch — iter 3+ |
| 6 | FAB Sheet stub | полный чат — iter 5–6 |
| 7 | Tailwind 4 + shadcn | create-next-app дал TW4; shadcn CLI или manual Radix deps |
| 8 | Root `/` → redirect | authenticated → role default; else → `/login` |

## Целевая структура `web/`

```
web/
├── app/
│   ├── layout.tsx              # dark, Inter + JetBrains Mono
│   ├── globals.css             # design-system tokens
│   ├── page.tsx                # redirect root
│   ├── (auth)/login/page.tsx
│   ├── (app)/
│   │   ├── layout.tsx          # AppShell + ChatFab
│   │   ├── dashboard/page.tsx
│   │   ├── leaderboard/page.tsx
│   │   └── chat/page.tsx
│   └── api/auth/
│       ├── login/route.ts
│       └── logout/route.ts
├── components/
│   ├── ui/                     # shadcn
│   ├── app-sidebar.tsx
│   ├── app-header.tsx
│   └── chat-fab.tsx
├── lib/
│   ├── session.ts
│   ├── backend-client.ts
│   └── types/auth.ts
├── middleware.ts
├── components.json
├── .env.example
└── README.md
```

## Задачи

| # | Задача | Статус | Документы |
|---|--------|--------|-----------|
| 02 | Каркас Next.js + layout + auth | ✅ Done | [plan](tasks/task-02-scaffold/plan.md) · [summary](tasks/task-02-scaffold/summary.md) |

## Фазы реализации (task 02)

| Фаза | Содержание | Статус |
|------|------------|--------|
| 0 | Plan-артефакты | ✅ |
| 1 | `create next-app` + merge toolchain | ✅ |
| 2 | shadcn + design tokens | ✅ |
| 3 | Auth BFF + session + middleware | ✅ |
| 4 | Login UI | ✅ |
| 5 | App shell + FAB + placeholders | ✅ |
| 6 | Makefile + env + docs | ✅ |
| 7 | lint/build/dev + summary | ✅ |

## Env

| Файл | Переменные |
|------|------------|
| `web/.env.example` | `BACKEND_URL=http://127.0.0.1:8000`, `BACKEND_SERVICE_TOKEN=` |
| `web/.env.local` | копия + token из корневого `.env` |
| `.env.example` | комментарий `NEXT_PUBLIC_BACKEND_URL` (iter 3+) |

## Make-команды (целевые)

```bash
make web-install && make web-dev      # :3000
make web-lint && make web-build
make backend-run && make db-reset     # :8000 + seed
```

## Definition of Done

**Self-check (агент):**

```bash
make db-reset && make backend-run
make web-install && make web-dev
make web-lint && make web-build
```

- `/login` → patient from seed → `/dashboard`; `doctor_ivanov` → `/leaderboard`
- Nav Dashboard / Leaderboard / Chat; FAB Sheet
- Header: display_name + logout
- Dark theme tbench-green

**User-check:** localhost:3000; login patient → dashboard; `doctor_ivanov` → leaderboard; FAB; logout.

## Out of scope

- Dashboard/leaderboard/history API fetch (iter 3–5)
- JWT/OAuth, E2E Playwright (iter 7)

## Риски

| Риск | Mitigation |
|------|------------|
| shadcn CLI недоступен | manual: clsx, cva, radix, lucide + copy components |
| TW4 vs shadcn docs | следовать `@theme inline` из create-next-app; tokens в CSS vars |
| Cookie в middleware | `request.cookies.get`; `sameSite: lax`, `path: /` |
| `pnpm-workspace.yaml` в `web/` | артеfact create-next-app; удалить при cleanup |

## Skills (при реализации)

| Skill | Фокус |
|-------|-------|
| shadcn | init, semantic tokens, Sheet/Sidebar |
| vercel-react-best-practices | минимум `"use client"` |
| nextjs-app-router-patterns | route groups, middleware, Route Handlers |
