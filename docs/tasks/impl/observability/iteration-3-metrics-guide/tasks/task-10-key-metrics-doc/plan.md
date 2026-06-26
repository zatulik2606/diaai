# Task 10 — документ «ключевые метрики»

## Цель

Справочник MVP: что мониторим, где смотреть, типичные симптомы и пороги.

## Файлы

| Файл | Действие |
|------|----------|
| [`devops/monitoring/key-metrics.md`](../../../../../../../devops/monitoring/key-metrics.md) | создать runbook |
| [`devops/monitoring/README.md`](../../../../../../../devops/monitoring/README.md) | ссылка «при инциденте» |
| [`docs/architecture.md`](../../../../../../../docs/architecture.md) | § Observability |
| [`docs/adr/adr-005-observability.md`](../../../../../../../docs/adr/adr-005-observability.md) | связанные документы |
| task-10 `summary.md` | после реализации |

## Разделы key-metrics.md

1. Быстрый чеклист (5 мин)
2. Availability — Uptime Kuma
3. Errors — GlitchTip
4. Backend RED — Grafana `diaai-backend-red`
5. VPS/Host — Grafana `diaai-vps-host`
6. PostgreSQL (post-MVP note)
7. GlitchTip traces — `GLITCHTIP_TRACES_SAMPLE_RATE`
8. Приложение: SSH tunnels

## Definition of Done

- По документу можно провести первичную диагностику без агента
- Ссылки из ADR, architecture, monitoring README
