# Task 02: Каркас Next.js + layout + auth — Summary

> **Статус:** 🚧 In Progress

Итерация: [iteration-2-scaffold](../../plan.md) · [plan](plan.md)

---

## Сделано

### Планирование ✅

- Plan-артефакты iter 2 и task 02 по [tasklist-frontend.md](../../../../../tasklist-frontend.md)
- Архитектура BFF-auth, route groups, role matrix, целевая структура `web/`
- [tasklist-frontend.md](../../../../../tasklist-frontend.md) актуализирован (iter 2 → next)

### Частичная реализация

- `pnpm create next-app` в `web/` — Next.js 16.2.9, React 19, Tailwind 4, ESLint, App Router
- Восстановлены toolchain-файлы: `.nvmrc` (24), `.npmrc`, `engines`/`packageManager` в `package.json`
- Default scaffold: `app/layout.tsx`, `app/page.tsx`, `app/globals.css`, `next.config.ts`

## Не сделано (остаток iter 2)

| Блок | Статус |
|------|--------|
| shadcn/ui init + компоненты | 📋 |
| Design tokens tbench в `globals.css` | 📋 |
| BFF `/api/auth/login|logout`, session cookie | 📋 |
| `middleware.ts`, role redirects | 📋 |
| Login page, AppShell, sidebar, header | 📋 |
| Placeholder routes (`/dashboard`, `/leaderboard`, `/chat`) | 📋 |
| ChatFab + Sheet-заглушка | 📋 |
| Makefile `web-*` targets | 📋 |
| `web/.env.example`, `web/README.md` (diaai) | 📋 |
| Skills review (shadcn, vercel, nextjs) | 📋 |

## Отклонения от плана

| Отклонение | Причина |
|------------|---------|
| shadcn CLI init не завершён | сеть / `ui.shadcn.com` недоступна; fallback — ручная установка deps |
| Default create-next-app page | iter 2 не закрыт — placeholder diaai UI не добавлен |
| `pnpm-workspace.yaml` в `web/` | артеfact create-next-app; не блокирует, можно удалить при cleanup |

## Решения (зафиксированы в plan)

| Решение | Обоснование |
|---------|-------------|
| BFF-only auth | `BACKEND_SERVICE_TOKEN` только server-side |
| httpOnly cookie `diaai_session` | безопаснее localStorage для MVP |
| Route groups `(auth)` / `(app)` | публичный login vs protected shell |
| Placeholder pages без API fetch | scope iter 2 — каркас, не dashboard |

## Проблемы

| Проблема | Статус |
|----------|--------|
| `create next-app` в непустой `web/` | обход: временный move `package.json` → init → merge |
| shadcn init network error | pending: ручной setup или retry CLI |
| `pnpm install` ERR_PNPM_IGNORED_BUILDS (sharp) | `pnpm approve-builds` при необходимости build |

## Проверки

| Команда | Результат |
|---------|-----------|
| `make web-dev` | ❌ нет Makefile targets |
| `make web-lint` / `make web-build` | ❌ не настроено |
| Login `akozhin` → `/dashboard` | ❌ auth не реализован |
| DoD iter 2 | ❌ не выполнен |

## Следующий шаг

1. shadcn + design tokens
2. BFF auth + middleware + AppShell + FAB
3. Makefile `web-*`, env, README
4. `make web-lint && make web-build` → закрыть task-02 и iter 2
