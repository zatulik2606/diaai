# Task 02 — Monitoring stack на prod (bridge + alarm bot)

## Цель

На VPS после app stack работают `glitchtip-telegram-bridge` и Dozzle; test `POST /webhook` доставляет сообщение в Telegram.

## Подготовка (пользователь)

- [ ] `TELEGRAM_ALARM_BOT_TOKEN`, `TELEGRAM_ALARM_CHAT_ID` в `/opt/diaai/.env`
- [ ] `@diaaialarm_bot` — `/start` (если ещё не сделано)
- [ ] **ufw allow 8080/tcp** — для webhook GlitchTip (Dozzle **не** открывать)
- [ ] Опционально: `GLITCHTIP_WEBHOOK_SECRET`, `DOZZLE_BIND=127.0.0.1:8888`

## Scope агента

Код bridge **уже есть** — [`devops/monitoring/glitchtip-telegram-bridge/`](../../../../../../../devops/monitoring/glitchtip-telegram-bridge/). Задача — конфигурация и документация prod-пути.

## Файлы (агент)

| Файл | Действие |
|------|----------|
| [`devops/deploy/compose.server.override.yml`](../../../../../../../devops/deploy/compose.server.override.yml) | уже: dozzle `127.0.0.1:8888` — проверить |
| [`devops/deploy/README.md`](../../../../../../../devops/deploy/README.md) | § monitoring-up после stack-up-registry |
| [`.env.example`](../../../../../../../.env.example) | `TELEGRAM_ALARM_*`, `GLITCHTIP_BRIDGE_BIND`, `GLITCHTIP_WEBHOOK_SECRET` |
| [`devops/monitoring/README.md`](../../../../../../../devops/monitoring/README.md) | prod sequence, ufw note |

Опционально (если нужен CD):

| Файл | Действие |
|------|----------|
| [`.github/workflows/deploy.yml`](../../../../../../../.github/workflows/deploy.yml) | `make monitoring-up` после `stack-health` — **только если согласовано** |

> **Решение плана:** CD не трогаем в iter 1 — monitoring поднимается **вручную** один раз на prod (KISS). При необходимости — отдельная задача.

## Prod sequence (пользователь)

```bash
ssh deploy@201.51.4.34
cd /opt/diaai
git pull --ff-only
make stack-up-registry
make monitoring-up
make monitoring-ps
curl -sf http://127.0.0.1:8080/health
curl -X POST http://127.0.0.1:8080/webhook \
  -H 'Content-Type: application/json' \
  -d '{"attachments":[{"title":"bridge prod test","title_link":"https://eu.glitchtip.com","text":"manual"}]}'
```

## Definition of Done

**Агент:** deploy docs актуальны; `.env.example` полный.

**Пользователь:** Telegram получил test webhook; `monitoring-ps` — bridge healthy.

## Skill

`docker-expert` · `sharp-edges`
