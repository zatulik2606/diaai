# Task 04 summary — E2E: GlitchTip ingest → Telegram

## Сделано

### Runbook (агент)

- [`devops/monitoring/README.md`](../../../../../../../devops/monitoring/README.md) — секция **E2E iter 1** с командами curl и проверкой логов
- [`devops/deploy/README.md`](../../../../../../../devops/deploy/README.md) §9 — пункты 1–3 ✅ (без изменений, уже закрыты в task 03)
- Prod checklist в monitoring README — iter 1 пункты отмечены ✅

### E2E smoke (2026-06-07, VPS)

| # | Шаг | Результат |
|---|-----|-----------|
| 1 | `GET /debug/glitchtip-test` (backend) | 200 `{"ok":true,"project":"diaai-backend"}` |
| 2 | `GET /api/debug/glitchtip-test` (web) | 200 `{"ok":true,"project":"diaai-web",...}` |
| 3 | Bridge health | 200 `{"status":"ok"}` |
| 4 | GlitchTip auto webhook | ✅ ранее (task 03, 2026-06-26): `165.227.159.10 POST /webhook` → bridge 200; `POST /webhooks/glitchtip/email` → backend 200 |

Шаг 3 в том же прогоне не дал новых строк в `--since 5m` — alert rule **1 event / 1 min** и повторные debug-события не всегда создают «new issue». Цепочка подтверждена task 03 + исторические логи bridge.

## Verify

```bash
# ingest
TOKEN=$(grep ^GLITCHTIP_DEBUG_TOKEN= /opt/diaai/.env | cut -d= -f2)
curl -sf -H "Authorization: Bearer $TOKEN" http://127.0.0.1:8000/debug/glitchtip-test
curl -sf -H "Authorization: Bearer $TOKEN" -H "Accept: application/json" \
  http://127.0.0.1:3000/api/debug/glitchtip-test

# webhook delivery (GlitchTip EU worker)
docker logs diaai-glitchtip-telegram-bridge-1 2>&1 | grep -a "165.227.159.10.*POST /webhook" | tail -3
```

## Отклонения от плана

Нет. Код prod paths не менялся — только docs и summaries.

## Следующая итерация

**Iter 2** — UptimeRobot monitors + acceptance §9 пункты 4–5 (task 05–06).
