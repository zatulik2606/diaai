# diaai web

Next.js App Router frontend для diaai: login по Telegram username, app shell, навигация, FAB чата.

## Требования

- Node 20+ (рекомендуется 24 — см. `.nvmrc`)
- pnpm 11.6 (`corepack enable && corepack prepare pnpm@11.6.0 --activate`)
- Backend на `:8000` с seeded БД

## Быстрый старт

```bash
# из корня репозитория
make db-reset && make backend-run   # :8000

cp web/.env.example web/.env.local  # BACKEND_URL, BACKEND_SERVICE_TOKEN
make web-install && make web-dev    # :3000
```

Demo login:

| username | роль | redirect |
|----------|------|----------|
| `ivan_p` | пациент | `/dashboard` |
| `doctor_ivanov` | доктор | `/leaderboard` |

## Команды

| Команда | Действие |
|---------|----------|
| `make web-install` | `pnpm install` |
| `make web-dev` | dev-сервер :3000 |
| `make web-build` | production build |
| `make web-lint` | ESLint |

## Архитектура auth

- BFF: `POST /api/auth/login`, `POST /api/auth/logout`
- BFF чат: `GET /api/assistant/history`, `POST /api/assistant/messages`
- Cookie `diaai_session` (httpOnly)
- Backend: `POST /api/v1/web/auth/resolve` + `BACKEND_SERVICE_TOKEN` (только server-side)

Подробнее: [docs/integrations.md](../docs/integrations.md) · [frontend-contract.md](../docs/api/frontend-contract.md)

## Dashboard smoke (iter 3)

```bash
make web-dev
# login ivan_p → /dashboard — KPI, chart, questions, submissions, matrix
```

## FAB chat smoke (iter 5)

```bash
make web-dev
# login ivan_p → FAB (правый нижний угол) или /chat — одна история
# отправить вопрос → ответ (нужен OPENROUTER_API_KEY в корневом .env)
# сообщение из FAB видно на /chat и наоборот (общий AssistantChatProvider)
```
