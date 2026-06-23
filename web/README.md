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
make web-build                      # production build (CI gate)
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
- BFF voice: `POST /api/assistant/transcribe` → backend `/api/v1/media/transcribe`
- BFF analytics: `POST /api/analytics/query` → backend `/api/v1/web/analytics/query`
- Cookie `diaai_session` (httpOnly)
- Backend: `POST /api/v1/web/auth/resolve` + `BACKEND_SERVICE_TOKEN` (только server-side)

Подробнее: [docs/integrations.md](../docs/integrations.md) · [frontend-contract.md](../docs/api/frontend-contract.md)

## Dashboard smoke (iter 3)

```bash
make web-dev
# login ivan_p → /dashboard — KPI, chart, questions, submissions, matrix
```

## FAB + `/chat` smoke (iter 5–6)

```bash
make db-reset && make backend-run && make web-dev
# ivan_p → FAB или sidebar Chat → history + send
# /chat — FAB скрыт; та же история через AssistantChatProvider
# нужен OPENROUTER_API_KEY для ответа LLM
```

## Voice input (iter 8)

```bash
make web-dev
# ivan_p → /chat → mic button → Web Speech API + backend STT fallback
# нужен OPENROUTER_API_KEY (STT через OpenRouter)
```

Ограничения: [docs/spec/voice-limitations.md](../docs/spec/voice-limitations.md).

## Analytics NL (iter 9, doctor)

```bash
make web-dev
# doctor_ivanov → /leaderboard → панель «Запрос к данным»
# или curl через backend/README.md
```

Spec: [text-to-sql-architecture.md](../docs/spec/text-to-sql-architecture.md).

## Полный smoke (~15 мин)

[docs/smoke-test.md](../docs/smoke-test.md) — bot + web + API в одной сессии.

Архитектура: [docs/architecture.md](../docs/architecture.md) · onboarding: [docs/onboarding.md](../docs/onboarding.md).
