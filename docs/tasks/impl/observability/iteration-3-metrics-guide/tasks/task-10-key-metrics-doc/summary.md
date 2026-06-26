# Task 10 summary — документ «ключевые метрики»

## Сделано

- [`devops/monitoring/key-metrics.md`](../../../../../../../devops/monitoring/key-metrics.md) — runbook: чеклист 5 мин, 6 разделов, SSH tunnels
- Ссылки из [`README.md`](../../../../../../../devops/monitoring/README.md), [`architecture.md`](../../../../../../../docs/architecture.md), [`adr-005`](../../../../../../../docs/adr/adr-005-observability.md)

## Содержание key-metrics.md

| Раздел | Суть |
|--------|------|
| Availability | Kuma 3 monitor, Down, Telegram `[Uptime Kuma]` |
| Errors | GlitchTip issue, bridge, Dozzle |
| Backend RED | пороги 5xx/p95/RPS, PromQL, dashboard uid |
| VPS/Host | CPU/RAM/disk пороги, cAdvisor nuance |
| PostgreSQL | post-MVP, Kuma + health |
| Traces | `GLITCHTIP_TRACES_SAMPLE_RATE` 0.01 → 0.1 |

## Definition of Done

✅ По документу можно провести первичную диагностику без агента.

## Observability area

**10/10** — область observability MVP закрыта.
