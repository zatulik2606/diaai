# Task 02 summary — Monitoring stack на prod

## Сделано

### VPS (201.51.4.34)

- `git stash` локальных правок → `git pull --ff-only` до `697951c`
- `compose.override.yml` из [`compose.server.override.yml`](../../../../../../../devops/deploy/compose.server.override.yml)
- Остановлен orphan `python3` на `:8080`
- `make stack-pull-registry && make stack-up-registry` — backend/web из GHCR
- `make monitoring-up` — **Dozzle** + **glitchtip-telegram-bridge**
- Добавлен `DOZZLE_BIND=127.0.0.1:8888` в `.env`

### Smoke (2026-06-26)

| Проверка | Результат |
|----------|-----------|
| `GET :8080/health` | `{"status":"ok"}` |
| `POST :8080/webhook` | `{"ok":true}` → Telegram |
| `GET :8888/` (localhost) | HTTP 200 |
| `make monitoring-ps` | bridge + dozzle Up |

### Документация

- [`devops/monitoring/README.md`](../../../../../../../devops/monitoring/README.md) — § Prod sequence task 02, primary webhook `:8080`
- [`devops/deploy/README.md`](../../../../../../../devops/deploy/README.md) §9 — sequence + checklist пункт 2 ✅
- [`devops/glitchtip/alerts-telegram.md`](../../../../../../../devops/glitchtip/alerts-telegram.md) — bridge primary для task 03
- [`.env.example`](../../../../../../../.env.example) — комментарий monitoring-up

## Отклонения

- CD [`deploy.yml`](../../../../../../../.github/workflows/deploy.yml) не меняли — monitoring вручную (KISS, по plan)
- Backend `:8000/webhooks/glitchtip` остаётся как альтернатива (email через `/webhooks/glitchtip/email`)

## Пользователь

- [ ] `sudo ufw allow 8080/tcp` — если ufw enabled (GlitchTip EU → bridge)
- [ ] Подтвердить Telegram после smoke POST
- [ ] Task 03: GlitchTip alert recipient → `http://201.51.4.34:8080/webhook`

## Следующая задача

Task 03 — GlitchTip Alert receivers → webhook в UI.
