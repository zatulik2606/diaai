# Task 02: Каркас Next.js + layout + auth

Итерация: [iteration-2-scaffold](../../plan.md)

**Статус:** 🚧 In Progress

---

## Цель

Поднять Next.js App Router в `web/` с shadcn/ui, BFF-auth, app shell и FAB-заглушкой.

## Порядок выполнения

1. Plan-артефакты iter 2 + task 02
2. `pnpm create next-app` в `web/` (merge engines)
3. shadcn init + components + globals.css tokens
4. `lib/backend-client.ts`, `lib/session.ts`, auth Route Handlers, middleware
5. Login page, AppShell, placeholder pages, ChatFab
6. Makefile web-*, env, README
7. lint/build/dev checks → summary

## Затронутые файлы

| Файл | Действие |
|------|----------|
| `web/app/**` | create — layouts, pages, api routes |
| `web/components/**` | create — ui, sidebar, header, fab |
| `web/lib/**` | create — session, backend-client, types |
| `web/middleware.ts` | create |
| `web/components.json` | create (shadcn) |
| `web/.env.example` | create |
| `Makefile` | add web-* targets |
| `README.md` | web quick start |
| `docs/integrations.md` | web env |
| `.env.example` | NEXT_PUBLIC_BACKEND_URL comment |

## Проверки

```bash
make web-install && make web-lint && make web-build
make backend-run   # separate terminal
make web-dev
# curl -X POST http://localhost:3000/api/auth/login -H 'Content-Type: application/json' -d '{"username":"akozhin"}'
```

## Demo credentials

| username | role | redirect |
|----------|------|----------|
| `akozhin` | doctor | `/dashboard` |
