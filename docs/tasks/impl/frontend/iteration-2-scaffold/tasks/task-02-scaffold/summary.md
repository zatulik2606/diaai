# Task 02: Каркас Next.js + layout + auth — Summary

> **Статус:** ✅ Done

Итерация: [iteration-2-scaffold](../../plan.md) · [plan](plan.md)

---

## Сделано

### shadcn + тема

- Ручная установка shadcn-компонентов (CLI недоступен): Button, Card, Input, Label, Avatar, Separator, Skeleton, Sheet, Table, Chart wrapper
- Design tokens tbench в `globals.css`; `components.json`
- `app/layout.tsx`: dark theme, Inter + JetBrains Mono

### Auth BFF + session

- `lib/types/auth.ts`, `lib/session.ts`, `lib/backend-client.ts`
- `POST /api/auth/login`, `POST /api/auth/logout`
- Cookie `diaai_session` (httpOnly, 7d)
- `middleware.ts`: guard, role redirects (doctor ↔ leaderboard, diabetic ↔ dashboard)

### UI shell

- Login page `(auth)/login`
- App shell: `(app)/layout.tsx`, sidebar, header, logout
- Placeholders: `/dashboard`, `/leaderboard`, `/chat`
- ChatFab (Sheet-заглушка iter 5)
- Root `page.tsx` → redirect по роли

### Infra + docs

- Makefile: `web-install`, `web-dev`, `web-build`, `web-lint`
- `web/.env.example`, `web/README.md`
- Root `README.md`, `docs/integrations.md`, `.env.example`

## Отклонения от плана

| Отклонение | Причина |
|------------|---------|
| shadcn CLI init | network error; ручная установка Radix + компоненты |
| Mobile sidebar Sheet | desktop-only sidebar в iter 2; mobile nav — iter 7 |
| `pnpm-workspace.yaml` в `web/` | artifact create-next-app; не блокирует |

## Решения

| Решение | Обоснование |
|---------|-------------|
| BFF-only auth | `BACKEND_SERVICE_TOKEN` только server-side |
| httpOnly cookie | безопаснее localStorage для MVP |
| Route groups `(auth)` / `(app)` | публичный login vs protected shell |

## Проверки

| Команда | Результат |
|---------|-----------|
| `make web-lint` | ✅ |
| `make web-build` | ✅ |
| `make web-dev` + login `akozhin` | ✅ → `/leaderboard` |
| login `ivan_p` | ✅ → `/dashboard` |
| doctor на `/dashboard` | ✅ 307 → leaderboard |

## Skills review

| Skill | Verdict |
|-------|---------|
| shadcn | ✅ semantic tokens, Sheet с title/description |
| vercel-react-best-practices | ✅ server layout, client только form/FAB/logout |
| nextjs-app-router-patterns | ✅ middleware matcher, route groups |
