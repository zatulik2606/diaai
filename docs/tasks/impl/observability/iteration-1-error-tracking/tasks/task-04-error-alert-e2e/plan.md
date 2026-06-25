# Task 04 — E2E: GlitchTip ingest → Telegram

## Цель

Зафиксировать полный runbook проверки observability iter 1 и закрыть acceptance §9 (пункты 1–3).

## Scope агента

- Runbook в docs (не временный test code в production paths)
- Iteration + task summaries
- Обновление baseline в tasklist

**Не делать:** оставлять публичный unauthenticated endpoint; не коммитить prod tokens.

## E2E сценарий (пользователь)

| # | Шаг | Ожидание |
|---|-----|----------|
| 1 | `curl` backend `/debug/glitchtip-test` + Bearer | 200, issue в GlitchTip backend |
| 2 | `curl` web `/api/debug/glitchtip-test` + Bearer | 200, issue в GlitchTip web |
| 3 | GlitchTip webhook (task 03) | Telegram alert на новый issue |
| 4 | (опционально) Спровоцировать 500 без debug — e.g. невалидный internal call | issue + alert |

## Файлы (агент)

| Файл | Действие |
|------|----------|
| [`devops/monitoring/README.md`](../../../../../../../devops/monitoring/README.md) | секция «E2E iter 1» с командами curl |
| [`devops/deploy/README.md`](../../../../../../../devops/deploy/README.md) | §9 пункты 1–3 → ✅ |
| [`docs/tasks/tasklist-observability.md`](../../../../../../tasklist-observability.md) | baseline iter 1, прогресс 4/10 |
| [iteration summary](../summary.md) | итог iter 1 |
| task-04 `summary.md` | факт проверки |

## Definition of Done

- [ ] Backend + web debug smoke ✅
- [ ] Telegram alert от real GlitchTip issue ✅
- [ ] Все `summary.md` task 01–04 + iteration summary заполнены
- [ ] `make lint` green (если task 01 менял код)

## Skill

`sharp-edges`
