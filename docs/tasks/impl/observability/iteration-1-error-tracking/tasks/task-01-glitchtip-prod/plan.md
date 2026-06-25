# Task 01 — GlitchTip ingest + `/debug/glitchtip-test`

## Цель

Backend и web отправляют тестовые события в GlitchTip EU через **защищённый** debug endpoint. DSN задаёт пользователь в `.env`.

## Подготовка (пользователь)

- [ ] DSN `diaai-backend` → `GLITCHTIP_DSN` в `.env`
- [ ] DSN `diaai-web` → `GLITCHTIP_WEB_DSN` + `NEXT_PUBLIC_GLITCHTIP_DSN` (и `web/.env.local` для `pnpm dev`)
- [ ] Сгенерировать `GLITCHTIP_DEBUG_TOKEN` (например `openssl rand -hex 32`) — **не коммитить**
- [ ] После изменения `NEXT_PUBLIC_*` — rebuild web image при docker stack

## Архитектура

```
GET /debug/glitchtip-test
  Authorization: Bearer $GLITCHTIP_DEBUG_TOKEN
  → sentry_sdk.capture_message("diaai glitchtip test: backend")
  → 200 { "ok": true, "project": "diaai-backend" }

GET /api/debug/glitchtip-test   (Next.js Route Handler, server-only)
  Authorization: Bearer $GLITCHTIP_DEBUG_TOKEN
  → Sentry.captureMessage("diaai glitchtip test: web")
  → 200 { "ok": true, "project": "diaai-web" }
```

Если `GLITCHTIP_DEBUG_TOKEN` пуст → маршруты **404** (не 401 без hint).

## Файлы (агент)

| Файл | Действие |
|------|----------|
| [`backend/config.py`](../../../../../../../backend/config.py) | `glitchtip_debug_token: str = ""` |
| [`backend/debug_glitchtip.py`](../../../../../../../backend/debug_glitchtip.py) | **новый** — router + dependency Bearer |
| [`backend/main.py`](../../../../../../../backend/main.py) | mount router `/debug` if token set |
| [`web/app/api/debug/glitchtip-test/route.ts`](../../../../../../../web/app/api/debug/glitchtip-test/route.ts) | **новый** — server route |
| [`.env.example`](../../../../../../../.env.example) | `GLITCHTIP_DEBUG_TOKEN=` |
| [`web/.env.example`](../../../../../../../web/.env.example) | `GLITCHTIP_DEBUG_TOKEN=` |
| [`backend/tests/test_debug_glitchtip.py`](../../../../../../../backend/tests/test_debug_glitchtip.py) | **новый** — 404 без token; 401 wrong; 200 + mock capture |
| [`backend/README.md`](../../../../../../../backend/README.md) | env + smoke curl |
| [`devops/monitoring/README.md`](../../../../../../../devops/monitoring/README.md) | ссылка на debug smoke |
| [`docs/architecture.md`](../../../../../../architecture.md) | observability: debug endpoint |

## Реализация backend

1. `Settings.glitchtip_debug_token` — pydantic, из env `GLITCHTIP_DEBUG_TOKEN`
2. `debug_glitchtip.py`:
   - `APIRouter(prefix="/debug", tags=["debug"], include_in_schema=False)`
   - Dependency: compare Bearer token with `settings.glitchtip_debug_token`
   - `GET /glitchtip-test`: require `settings.glitchtip_dsn`; `capture_message(...)`; return JSON
3. `create_app()`: if `glitchtip_debug_token` → `app.include_router(debug_router)`

## Реализация web

1. Route Handler `GET` only
2. Read `process.env.GLITCHTIP_DEBUG_TOKEN` — if empty → `notFound()`
3. Validate `Authorization: Bearer ...`
4. Require `GLITCHTIP_DSN` or `NEXT_PUBLIC_GLITCHTIP_DSN`
5. `@sentry/nextjs` `captureMessage` on server

## Smoke (пользователь после деплоя env)

```bash
# Backend (local :8000 или prod)
curl -sf -H "Authorization: Bearer $GLITCHTIP_DEBUG_TOKEN" \
  http://127.0.0.1:8000/debug/glitchtip-test

# Web BFF
curl -sf -H "Authorization: Bearer $GLITCHTIP_DEBUG_TOKEN" \
  http://127.0.0.1:3000/api/debug/glitchtip-test
```

Ожидание: issue в GlitchTip EU ≤1 min.

## Definition of Done

**Агент:** `make lint` green; pytest для debug router; docs обновлены.

**Пользователь:** 2 test issues в GlitchTip (backend + web projects).

## Skill

`sharp-edges` — token не в git, не логировать Authorization.
