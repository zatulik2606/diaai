# Task 03 summary — GlitchTip Alert receivers → webhook

## Сделано

### GlitchTip UI (пользователь)

- **Telegram:** `http://201.51.4.34:8080/webhook` — проекты `diaai-backend`, `diaai-web`
- **Email:** `http://201.51.4.34:8000/webhooks/glitchtip/email` — второй recipient в alert rule
- Alert rule: **1 event / 1 minute**

### Документация (агент)

- [`devops/glitchtip/alerts-telegram.md`](../../../../../../../devops/glitchtip/alerts-telegram.md) — § 4.1 UI runbook
- [`devops/deploy/README.md`](../../../../../../../devops/deploy/README.md) §9 пункт 3

### E2E smoke (2026-06-26, VPS)

| Шаг | Результат |
|-----|-----------|
| `POST /webhooks/glitchtip/email` (manual) | 200 `{"ok":true}` |
| Debug backend + web | 200, events в GlitchTip |
| Auto `POST /webhook` → bridge | `165.227.159.10` ×2 → 200 |
| Auto `POST /webhooks/glitchtip/email` | `165.227.159.10` ×2 → 200 |

GlitchTip EU worker доставляет оба webhook автоматически (без ручного curl после ingest).

## Verify

- Bridge logs: `165.227.159.10 - "POST /webhook HTTP/1.1" 200`
- Backend logs: `165.227.159.10 - "POST /webhooks/glitchtip/email HTTP/1.1" 200`
- Telegram + email — пользователь подтвердил настройку UI

## Следующая задача

Task 04 — E2E runbook + закрытие acceptance §9 (пункты 1–3).
