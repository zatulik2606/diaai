# Task 03 summary — GlitchTip Alert receivers → webhook

## Статус

🚧 **Ожидает:** настройка UI в eu.glitchtip.com пользователем → E2E smoke.

## Агент (docs)

- [`devops/glitchtip/alerts-telegram.md`](../../../../../../../devops/glitchtip/alerts-telegram.md) — § 4.1 пошаговый runbook (alert rule + webhook `:8080`)
- [`devops/deploy/README.md`](../../../../../../../devops/deploy/README.md) §9 пункт 3 — ссылка на runbook

## Пользователь — checklist UI

Для **diaai-backend** и **diaai-web**:

1. Project Settings → **Project Alerts**
2. Rule: **1 event / 1 minute**
3. Recipient: Webhook → `http://201.51.4.34:8080/webhook`
4. Удалить старый `:8000/webhooks/glitchtip` (если есть)
5. Email (опционально): второй recipient → `:8000/webhooks/glitchtip/email`

## E2E smoke (после UI)

```bash
ssh deploy@201.51.4.34
TOKEN=$(grep ^GLITCHTIP_DEBUG_TOKEN= /opt/diaai/.env | cut -d= -f2)
curl -sf -H "Authorization: Bearer $TOKEN" http://127.0.0.1:8000/debug/glitchtip-test
# ≤2 min: Telegram от @diaaialarm_bot
docker logs diaai-glitchtip-telegram-bridge-1 --since 5m | grep 'POST /webhook'
```

## Definition of Done

- [ ] UI настроен (backend + web)
- [ ] Auto webhook → bridge → Telegram (без ручного curl)
- [ ] Tasklist 3/10 ✅
