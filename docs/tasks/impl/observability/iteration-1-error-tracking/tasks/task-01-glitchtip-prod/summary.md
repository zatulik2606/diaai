# Task 01 summary — GlitchTip ingest + debug endpoint

## Сделано

### Код (уже был в main)

- [`backend/debug_glitchtip.py`](../../../../../../../backend/debug_glitchtip.py) — `GET /debug/glitchtip-test`, Bearer, 404 без token
- [`backend/main.py`](../../../../../../../backend/main.py) — `include_debug_routes`
- [`web/app/api/debug/glitchtip-test/route.ts`](../../../../../../../web/app/api/debug/glitchtip-test/route.ts) — server route
- [`web/middleware.ts`](../../../../../../../web/middleware.ts) — bypass `/api/debug`
- [`backend/tests/test_debug_glitchtip.py`](../../../../../../../backend/tests/test_debug_glitchtip.py) — 3 теста
- [`.env.example`](../../../../../../../.env.example), [`web/.env.example`](../../../../../../../web/.env.example)

### Документация (эта сессия)

- [`backend/README.md`](../../../../../../../backend/README.md) — `GLITCHTIP_DEBUG_TOKEN`, smoke curl
- [`devops/monitoring/README.md`](../../../../../../../devops/monitoring/README.md) — § GlitchTip smoke
- [`docs/architecture.md`](../../../../../../architecture.md) — строка smoke ingest
- [`devops/deploy/README.md`](../../../../../../../devops/deploy/README.md) §9 — prod env + curl checklist

### CI

- [`.github/workflows/docker-publish.yml`](../../../../../../../.github/workflows/docker-publish.yml) — build-args `NEXT_PUBLIC_GLITCHTIP_DSN`, `GLITCHTIP_DSN`, `GLITCHTIP_URL` для matrix `web`
- GitHub secrets `GLITCHTIP_DSN`, `GLITCHTIP_WEB_DSN`, `NEXT_PUBLIC_GLITCHTIP_DSN` — уже заданы

### Prod (VPS 201.51.4.34)

- `/opt/diaai/.env`: `GLITCHTIP_DSN`, `GLITCHTIP_WEB_DSN`, `NEXT_PUBLIC_GLITCHTIP_DSN`, `GLITCHTIP_DEBUG_TOKEN`, `GLITCHTIP_ENVIRONMENT=production`, `DIAAI_WEB_IMAGE=ghcr.io/zatulik2606/diaai-web:main`
- Исправлен `compose.override.yml` (убрана битая секция `dozzle` без image)
- Smoke 2026-06-26:
  - `GET /debug/glitchtip-test` → `{"ok":true,"project":"diaai-backend"}`
  - `GET /api/debug/glitchtip-test` → `{"ok":true,"project":"diaai-web","eventId":"..."}`

## Отклонения от plan

| Plan | Факт |
|------|------|
| Web `captureMessage` | `captureException` — error-level issue, лучше для alert rules |
| Deploy после CI | `workflow_dispatch` не триггерит Deploy; web обновлён вручную `docker pull` |

## Verify

- `make lint` ✅
- `uv run pytest backend/tests/test_debug_glitchtip.py` — 3 passed ✅
- Prod curl smoke — ✅

## Пользователь

- Просмотреть новые issues в [eu.glitchtip.com](https://eu.glitchtip.com) (backend + web)
- После push в main — новый web image с `NEXT_PUBLIC_*` в CI (browser ingest)

## Следующая задача

Task 02 — monitoring stack на prod (bridge + alarm bot).
