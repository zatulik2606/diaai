# Iteration 1 summary — отслеживание ошибок + алерты

## Результат

Prod-цепочка **GlitchTip EU → webhook → Telegram + email** работает. Acceptance [deploy/README.md §9](../../../../devops/deploy/README.md#9-observability-mvp) пункты **1–3** ✅.

| Компонент | Prod |
|-----------|------|
| Backend ingest + `/debug/glitchtip-test` | ✅ `diaai-backend` |
| Web ingest + `/api/debug/glitchtip-test` | ✅ `diaai-web` |
| Bridge `:8080/webhook` | ✅ `@diaaialarm_bot` |
| Email `:8000/webhooks/glitchtip/email` | ✅ Mail.ru SMTP |
| GlitchTip alert recipients | ✅ оба проекта, rule 1 event/min |

## Задачи

| Task | Summary |
|------|---------|
| 01 GlitchTip ingest | [summary](tasks/task-01-glitchtip-prod/summary.md) |
| 02 Bridge + monitoring | [summary](tasks/task-02-bridge-prod/summary.md) |
| 03 Alert receivers | [summary](tasks/task-03-glitchtip-webhook/summary.md) |
| 04 E2E runbook | [summary](tasks/task-04-error-alert-e2e/summary.md) |

## Runbook

Единая процедура проверки: [monitoring/README.md § E2E iter 1](../../../../devops/monitoring/README.md#e2e-iter-1-task-04--ingest--alert).

## Решения и нюансы

- **Backend `network_mode: host`** на prod — SMTP через IPv6 (Timeweb); web ходит на backend через `172.18.0.1:8000`.
- **Debug endpoints** — только с `Authorization: Bearer GLITCHTIP_DEBUG_TOKEN`; без token маршруты 404.
- **Два канала алертов:** bridge `:8080` (Telegram) + backend email webhook; оба настроены как GlitchTip recipients.
- **Deploy workflow:** CD использует `git fetch + reset --hard origin/main + clean -fd` (fix 2026-06-28); раньше падал на `git pull` из‑за локальных правок на VPS.

## Out of scope (iter 2+)

- UptimeRobot (§9 п. 4–5)
- Dozzle SSH tunnel как acceptance (§9 п. 6)
- Prometheus + Grafana
