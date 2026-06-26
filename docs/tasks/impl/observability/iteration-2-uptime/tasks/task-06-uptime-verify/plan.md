# Task 06 — Uptime Kuma monitors + acceptance §9

## Цель

Закрыть observability iter 2: два monitor'а в Kuma, Telegram-уведомления, acceptance [deploy/README.md §9](../../../../../devops/deploy/README.md#9-observability-mvp) пункты **4–5** ✅.

## Подготовка (пользователь)

- [ ] Kuma UI доступен (task 05): `ssh -L 3002:127.0.0.1:3002 deploy@201.51.4.34`
- [ ] Settings → Notifications → **Telegram** — bot token + chat_id
- [ ] Monitor **`diaai-backend-health`**
  - Type: HTTP(s)
  - URL prod: `http://172.18.0.1:8000/health`
  - Keyword: `"status":"ok"`
  - Interval: 60 s (или 300 s)
- [ ] Monitor **`diaai-web`**
  - URL: `http://web:3000/` (из контейнера Kuma) или `http://172.18.0.1:3000/`
  - Accept 200 / 307
- [ ] Тест: **Pause** monitor → alert в Telegram → **Resume**

## Состав работ (агент)

| Файл | Действие |
|------|----------|
| [`devops/monitoring/uptime-kuma.md`](../../../../../../../../devops/monitoring/uptime-kuma.md) | пошаговый UI runbook (§ Monitors, § Telegram, § Smoke) |
| [`devops/deploy/README.md`](../../../../../../../../devops/deploy/README.md) §9 | пункты 4–5: Uptime Kuma вместо UptimeRobot; таблица monitors |
| [`devops/monitoring/README.md`](../../../../../../../../devops/monitoring/README.md) | prod checklist iter 2 ✅ |
| [`docs/architecture.md`](../../../../../../../architecture.md) | Observability: Uptime Kuma |
| [`docs/adr/adr-005-observability.md`](../../../../../../../adr/adr-005-observability.md) | примечание: iter 2 — Kuma (или короткий ADR-amendment) |
| [`docs/tasks/tasklist-observability.md`](../../../../../../../tasklist-observability.md) | iter 2 ✅, прогресс 6/10 |
| [iteration summary](../../summary.md) | итог iter 2 |
| task-06 `summary.md` | факт проверки (без секретов) |

**Не делать:** хранить Telegram token Kuma в git; не открывать `:3002` в ufw.

## Verify

```bash
# на VPS
curl -sf http://127.0.0.1:8000/health
curl -sf -o /dev/null http://127.0.0.1:3000/
docker compose … ps uptime-kuma   # Up
```

Kuma dashboard: оба monitor **Up** (green). Pause → Telegram within 1–2 intervals.

## Definition of Done

- [ ] 2 monitor'а Up 24/7
- [ ] Down-тест → Telegram получен
- [ ] deploy §9 п.4–5 ✅
- [ ] iteration + task summaries
- [ ] `make lint` green (если task 05 не прогнали)

## Skill

—
