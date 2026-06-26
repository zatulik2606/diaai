# Observability Tasklist

Опирается на [plan.md](../plan.md) · [architecture.md](../architecture.md) · [ADR-005](../adr/adr-005-observability.md) · [devops/monitoring/README.md](../../devops/monitoring/README.md)

## Обзор

Рабочий план области **observability**: довести до prod стек из ADR-005 — **GlitchTip EU** (ошибки, Sentry-compatible SDK), **UptimeRobot** (доступность), **Dozzle** (логи), **Prometheus + Grafana** (метрики и дашборды).

| Итерация | Фокус | Инструменты |
|----------|-------|-------------|
| **1** | Отслеживание ошибок + алерты в Telegram | GlitchTip, `sentry-sdk`, `@sentry/nextjs`, `@diaaialarm_bot`, bridge |
| **2** | Мониторинг доступности | UptimeRobot (SaaS) |
| **3** | Логи и метрики | Dozzle, Prometheus, Grafana |
| **3.1** | Справочник ключевых метрик | docs |

**Текущее состояние (baseline):**

| Компонент | Локально | Prod |
|-----------|----------|------|
| GlitchTip ingest (backend/web) | ✅ `GLITCHTIP_*` | ✅ debug smoke |
| `@diaaialarm_bot` + `TELEGRAM_ALARM_*` | ✅ | ✅ |
| `glitchtip-telegram-bridge` + Dozzle | ✅ `make monitoring-up` | ✅ `:8080` + `:8888` localhost |
| GlitchTip → webhook → Telegram | ✅ UI `:8080/webhook` | ✅ auto POST GlitchTip EU |
| UptimeRobot monitors | 📋 | 📋 |
| Prometheus + Grafana + dashboards | 📋 | 📋 |

**Прогресс:** **3 / 10** задач · iter 1 🚧

> **Scope MVP:** без self-hosted GlitchTip, ELK, Loki. Prometheus/Grafana — в profile `monitoring` на prod-VPS (см. ADR-005 «отложено» — осознанное расширение iter 3 по запросу на дашборды).

## Легенда статусов

- 📋 Planned — запланирован
- 🚧 In Progress — в работе
- ✅ Done — завершён

## Skills

Подбор через `/find-skills`, если skill не найден в репозитории.

| Skill | Когда | Фокус |
|-------|-------|-------|
| `sharp-edges` | **iter 1** | секреты `GLITCHTIP_*`, `TELEGRAM_ALARM_*` — не в git, не в логах |
| `docker-expert` | **iter 1**, **iter 3** | compose profile `monitoring`, порты, healthchecks, RAM на 4 GB VPS |
| `grafana-dashboards` | **iter 3**, task 09 | JSON dashboards FastAPI (RED) + host/container metrics |

## Итерации

| # | Название | Задачи | Статус | Документы |
|---|----------|--------|--------|-----------|
| 1 | Отслеживание ошибок + алерты | 01–04 | 🚧 In Progress | [plan](impl/observability/iteration-1-error-tracking/plan.md) · [summary](impl/observability/iteration-1-error-tracking/summary.md) |
| 2 | Мониторинг доступности | 05–06 | 📋 Planned | [plan](impl/observability/iteration-2-uptime/plan.md) · [summary](impl/observability/iteration-2-uptime/summary.md) |
| 3 | Логи и метрики | 07–09 | 📋 Planned | [plan](impl/observability/iteration-3-logs-metrics/plan.md) · [summary](impl/observability/iteration-3-logs-metrics/summary.md) |
| 3.1 | Ключевые метрики (docs) | 10 | 📋 Planned | [plan](impl/observability/iteration-3-metrics-guide/plan.md) · [summary](impl/observability/iteration-3-metrics-guide/summary.md) |

## Список задач

| Задача | Описание | Статус | Документы |
|--------|----------|--------|-----------|
| 01 | GlitchTip на prod: env, ingest backend + web | ✅ | [план](impl/observability/iteration-1-error-tracking/tasks/task-01-glitchtip-prod/plan.md) · [summary](impl/observability/iteration-1-error-tracking/tasks/task-01-glitchtip-prod/summary.md) |
| 02 | Monitoring stack на prod: bridge + alarm bot | ✅ | [план](impl/observability/iteration-1-error-tracking/tasks/task-02-bridge-prod/plan.md) · [summary](impl/observability/iteration-1-error-tracking/tasks/task-02-bridge-prod/summary.md) |
| 03 | GlitchTip Alert receivers → webhook | ✅ | [план](impl/observability/iteration-1-error-tracking/tasks/task-03-glitchtip-webhook/plan.md) · [summary](impl/observability/iteration-1-error-tracking/tasks/task-03-glitchtip-webhook/summary.md) |
| 04 | E2E: ошибка → GlitchTip → Telegram | 📋 | [план](impl/observability/iteration-1-error-tracking/tasks/task-04-error-alert-e2e/plan.md) · [summary](impl/observability/iteration-1-error-tracking/tasks/task-04-error-alert-e2e/summary.md) |
| 05 | UptimeRobot: monitors + alert contact | 📋 | [план](impl/observability/iteration-2-uptime/tasks/task-05-uptimerobot/plan.md) · [summary](impl/observability/iteration-2-uptime/tasks/task-05-uptimerobot/summary.md) |
| 06 | Uptime acceptance + prod checklist | 📋 | [план](impl/observability/iteration-2-uptime/tasks/task-06-uptime-verify/plan.md) · [summary](impl/observability/iteration-2-uptime/tasks/task-06-uptime-verify/summary.md) |
| 07 | Dozzle на prod + SSH tunnel | 📋 | [план](impl/observability/iteration-3-logs-metrics/tasks/task-07-dozzle-prod/plan.md) · [summary](impl/observability/iteration-3-logs-metrics/tasks/task-07-dozzle-prod/summary.md) |
| 08 | Prometheus + Grafana (compose monitoring) | 📋 | [план](impl/observability/iteration-3-logs-metrics/tasks/task-08-prometheus-grafana/plan.md) · [summary](impl/observability/iteration-3-logs-metrics/tasks/task-08-prometheus-grafana/summary.md) |
| 09 | Grafana dashboards: FastAPI + VPS | 📋 | [план](impl/observability/iteration-3-logs-metrics/tasks/task-09-grafana-dashboards/plan.md) · [summary](impl/observability/iteration-3-logs-metrics/tasks/task-09-grafana-dashboards/summary.md) |
| 10 | Документ «ключевые метрики» | 📋 | [план](impl/observability/iteration-3-metrics-guide/tasks/task-10-key-metrics-doc/plan.md) · [summary](impl/observability/iteration-3-metrics-guide/tasks/task-10-key-metrics-doc/summary.md) |

Задачи выполняются **последовательно** (01 → 10). Итерация N — после закрытия N−1.

---

## Итерация 1 — Отслеживание ошибок + алерты 🚧

**Ценность:** узнавать о 500 и падениях React **до** пользователей; алерт в Telegram с ссылкой на issue в GlitchTip.

**План итерации:** [impl/observability/iteration-1-error-tracking/plan.md](impl/observability/iteration-1-error-tracking/plan.md)

**Граница:** DSN и prod secrets — **пользователь**; код, compose, docs — **агент**.

**Результат итерации:**
- backend и web шлют события в **GlitchTip EU** (smoke через `/debug/glitchtip-test` + Bearer `GLITCHTIP_DEBUG_TOKEN`)
- новый issue → webhook → **@diaaialarm_bot**
- acceptance из [devops/deploy/README.md §9](../../devops/deploy/README.md) (пункты 1–3) ✅

**Skill:** `sharp-edges` · `docker-expert` (task 02)

→ [iteration-1-error-tracking/plan.md](impl/observability/iteration-1-error-tracking/plan.md)

---

## Задача 01: GlitchTip ingest + debug endpoint ✅

### Цель

Ingest backend/web в GlitchTip EU; безопасная проверка через **`GET /debug/glitchtip-test`** (Bearer `GLITCHTIP_DEBUG_TOKEN`). DSN — у пользователя.

✅ [План](impl/observability/iteration-1-error-tracking/tasks/task-01-glitchtip-prod/plan.md) · [Summary](impl/observability/iteration-1-error-tracking/tasks/task-01-glitchtip-prod/summary.md)

### Подготовка (пользователь)

- [x] DSN → `GLITCHTIP_DSN`, `GLITCHTIP_WEB_DSN`, `NEXT_PUBLIC_GLITCHTIP_DSN` в `.env` / prod
- [x] `GLITCHTIP_DEBUG_TOKEN` в `.env` / prod (не в git)
- [x] Rebuild web — `ghcr.io/zatulik2606/diaai-web:main` на VPS

### Состав работ (агент)

- [x] `backend/debug_glitchtip.py` + mount в `main.py` (404 если token пуст)
- [x] `web/app/api/debug/glitchtip-test/route.ts`
- [x] `GLITCHTIP_DEBUG_TOKEN` в `.env.example`, `web/.env.example`
- [x] pytest `backend/tests/test_debug_glitchtip.py`
- [x] docs: backend README, monitoring README, architecture, deploy §9
- [x] CI: build-args GlitchTip DSN в `docker-publish.yml` (web)

### Smoke (prod)

```bash
curl -H "Authorization: Bearer $GLITCHTIP_DEBUG_TOKEN" http://127.0.0.1:8000/debug/glitchtip-test
curl -H "Authorization: Bearer $GLITCHTIP_DEBUG_TOKEN" http://127.0.0.1:3000/api/debug/glitchtip-test
```

✅ VPS 2026-06-26

### Skill

`sharp-edges`

### Документы

- ✅ [План](impl/observability/iteration-1-error-tracking/tasks/task-01-glitchtip-prod/plan.md)
- ✅ [Summary](impl/observability/iteration-1-error-tracking/tasks/task-01-glitchtip-prod/summary.md)

---

## Задача 02: Monitoring stack на prod — bridge ✅

📋 [План](impl/observability/iteration-1-error-tracking/tasks/task-02-bridge-prod/plan.md) · ✅ [Summary](impl/observability/iteration-1-error-tracking/tasks/task-02-bridge-prod/summary.md)

На VPS: `make monitoring-up` → Dozzle (`127.0.0.1:8888`) + bridge (`:8080/webhook` → Telegram). Smoke POST `/webhook` ✅ 2026-06-26.

**Пользователь:** ufw `8080/tcp`; task 03 — GlitchTip webhook URL.

### Документы

- ✅ [План](impl/observability/iteration-1-error-tracking/tasks/task-02-bridge-prod/plan.md)
- ✅ [Summary](impl/observability/iteration-1-error-tracking/tasks/task-02-bridge-prod/summary.md)

---

## Задача 03: GlitchTip Alert receivers → webhook ✅

✅ [План](impl/observability/iteration-1-error-tracking/tasks/task-03-glitchtip-webhook/plan.md) · [Summary](impl/observability/iteration-1-error-tracking/tasks/task-03-glitchtip-webhook/summary.md)

**Prod recipients (оба проекта):**

| Канал | URL |
|-------|-----|
| Telegram | `http://201.51.4.34:8080/webhook` |
| Email | `http://201.51.4.34:8000/webhooks/glitchtip/email` |

E2E ✅ 2026-06-26 — auto POST от `165.227.159.10` (GlitchTip EU).

### Документы

- ✅ [План](impl/observability/iteration-1-error-tracking/tasks/task-03-glitchtip-webhook/plan.md)
- ✅ [Summary](impl/observability/iteration-1-error-tracking/tasks/task-03-glitchtip-webhook/summary.md)

---

## Задача 04: E2E — GlitchTip → Telegram 📋

📋 [План](impl/observability/iteration-1-error-tracking/tasks/task-04-error-alert-e2e/plan.md) — runbook + summaries; smoke через task 01 debug + task 03 webhook.

### Документы

- 📋 [План](impl/observability/iteration-1-error-tracking/tasks/task-04-error-alert-e2e/plan.md)
- 📝 [Summary](impl/observability/iteration-1-error-tracking/tasks/task-04-error-alert-e2e/summary.md)

---

## Итерация 2 — Мониторинг доступности 📋

**Ценность:** узнать о падении VPS/контейнера/порта **снаружи**, когда `stack-health` уже не поможет.

**Результат итерации:**
- UptimeRobot пингует `:8000/health` и `:3000`
- алерт в Telegram/email при Down
- acceptance §9 пункты 4–5 ✅

→ [iteration-2-uptime/plan.md](impl/observability/iteration-2-uptime/plan.md)

---

## Задача 05: UptimeRobot — monitors + alert contact 📋

### Цель

Два HTTP monitor'а и канал оповещения настроены по [uptimerobot.md](../../devops/monitoring/uptimerobot.md).

### Подготовка (пользователь)

- [ ] Регистрация на [uptimerobot.com](https://uptimerobot.com/)
- [ ] Alert Contact: **Telegram** (рекомендуется) или email
- [ ] Monitor `diaai-backend-health`: `http://201.51.4.34:8000/health`, keyword `"status":"ok"`
- [ ] Monitor `diaai-web`: `http://201.51.4.34:3000/`, interval 5 min

### Состав работ

- [ ] Проверить monitors **Up** с dashboard UptimeRobot
- [ ] Test alert: Pause monitor → уведомление → Resume
- [ ] Дополнить [uptimerobot.md](../../devops/monitoring/uptimerobot.md) при расхождениях

### Артефакты

- UptimeRobot dashboard — 2 monitors green
- скрин или заметка в task summary (без секретов)

### Definition of Done

**Пользователь:** оба monitor Up; тестовый Down → alert получен.

### Skill

—

### Документы

- 📋 [План](impl/observability/iteration-2-uptime/tasks/task-05-uptimerobot/plan.md)
- 📝 [Summary](impl/observability/iteration-2-uptime/tasks/task-05-uptimerobot/summary.md)

---

## Задача 06: Uptime acceptance + prod checklist 📋

### Цель

Закрыть observability acceptance по доступности; response time виден в UptimeRobot как грубая метрика latency.

### Состав работ

- [ ] Обновить [deploy/README.md §9](../../devops/deploy/README.md) — пункты 4–5 ✅
- [ ] Связать UptimeRobot alerts с `@diaaialarm_bot` (если ещё не сделано в task 05)
- [ ] Iteration 2 summary

### Артефакты

- [iteration-2 summary](impl/observability/iteration-2-uptime/summary.md)

### Definition of Done

**Пользователь:** мониторинг доступности работает 24/7 без участия агента.

### Skill

—

### Документы

- 📋 [План](impl/observability/iteration-2-uptime/tasks/task-06-uptime-verify/plan.md)
- 📝 [Summary](impl/observability/iteration-2-uptime/tasks/task-06-uptime-verify/summary.md)

---

## Итерация 3 — Логи и метрики 📋

**Ценность:** при инциденте — логи всех контейнеров в одном UI; дашборды RED для FastAPI и ресурсов VPS.

**Результат итерации:**
- Dozzle на prod (localhost + SSH tunnel)
- Prometheus + Grafana в profile `monitoring`
- dashboards FastAPI + host/container
- документ ключевых метрик (iter 3.1)

**Skills:** `docker-expert` · **`grafana-dashboards`**

→ [iteration-3-logs-metrics/plan.md](impl/observability/iteration-3-logs-metrics/plan.md)

---

## Задача 07: Dozzle на prod + SSH tunnel 📋

### Цель

Dozzle доступен на VPS (`127.0.0.1:8888`); разработчик смотрит логи всех контейнеров через SSH tunnel.

### Подготовка (пользователь)

- [ ] Task 02 выполнен (`make monitoring-up`)
- [ ] **ufw:** порт 8888 **не** открыт наружу

### Состав работ

- [ ] Проверить `DOZZLE_BIND=127.0.0.1:8888` в prod `.env`
- [ ] Документировать tunnel в [monitoring/README.md](../../devops/monitoring/README.md)
- [ ] Smoke: `ssh -L 8888:127.0.0.1:8888 deploy@201.51.4.34` → UI, логи backend/web/postgres

### Артефакты

- deploy §9 пункт 6 ✅

### Definition of Done

**Пользователь:** логи backend видны в Dozzle без `docker logs` по SSH.

### Skill

`docker-expert`

### Документы

- 📋 [План](impl/observability/iteration-3-logs-metrics/tasks/task-07-dozzle-prod/plan.md)
- 📝 [Summary](impl/observability/iteration-3-logs-metrics/tasks/task-07-dozzle-prod/summary.md)

---

## Задача 08: Prometheus + Grafana (compose monitoring) 📋

### Цель

Profile `monitoring` дополнен Prometheus + Grafana (+ cAdvisor/node exporter по RAM); scrape backend metrics endpoint.

### Подготовка (пользователь)

- [ ] Решение по RAM: мониторить `docker stats` после поднятия stack; при OOM — урезать retention/scrape interval
- [ ] Grafana admin password в prod `.env` (`GRAFANA_ADMIN_PASSWORD`, не в git)

### Состав работ

- [ ] Расширить [`devops/monitoring/compose.yml`](../../devops/monitoring/compose.yml): prometheus, grafana, cAdvisor (или node-exporter)
- [ ] FastAPI: `/metrics` (prometheus-fastapi-instrumentator или аналог) — минимальный RED
- [ ] `prometheus.yml` — scrape backend, cAdvisor, self
- [ ] Grafana: datasource Prometheus; bind `127.0.0.1:3001` на prod (SSH tunnel)
- [ ] Makefile targets: без изменения контракта `monitoring-up`

### Артефакты

- `devops/monitoring/prometheus.yml`
- `devops/monitoring/grafana/provisioning/` (datasources)
- backend metrics endpoint

### Definition of Done

**Агент:** Prometheus targets UP; Grafana открывается через tunnel; RAM VPS в норме.

**Пользователь:** в Grafana видны raw metrics backend.

### Skill

`docker-expert`

### Документы

- 📋 [План](impl/observability/iteration-3-logs-metrics/tasks/task-08-prometheus-grafana/plan.md)
- 📝 [Summary](impl/observability/iteration-3-logs-metrics/tasks/task-08-prometheus-grafana/summary.md)

---

## Задача 09: Grafana dashboards — FastAPI + VPS 📋

### Цель

Импортируемые dashboards: **HTTP RED** (rate, errors, duration) для FastAPI и **host/container** (CPU, RAM, disk, network).

### Состав работ

- [ ] Подключить skill **`grafana-dashboards`**
- [ ] Dashboard `diaai-backend-red`: RPS, 5xx rate, p50/p95 latency по route
- [ ] Dashboard `diaai-vps-host`: CPU%, memory, disk, container CPU/RAM (cAdvisor)
- [ ] JSON в `devops/monitoring/grafana/dashboards/` + provisioning
- [ ] README: как открыть Grafana, default dashboards

### Артефакты

- `devops/monitoring/grafana/dashboards/diaai-backend-red.json`
- `devops/monitoring/grafana/dashboards/diaai-vps-host.json`

### Definition of Done

**Пользователь:** после deploy оба dashboard показывают live data ≥15 min.

### Skill

**`grafana-dashboards`** · `docker-expert`

### Документы

- 📋 [План](impl/observability/iteration-3-logs-metrics/tasks/task-09-grafana-dashboards/plan.md)
- 📝 [Summary](impl/observability/iteration-3-logs-metrics/tasks/task-09-grafana-dashboards/summary.md)

---

## Итерация 3.1 — Ключевые метрики (docs) 📋

**Ценность:** при инциденте понятно, **какие** графики смотреть первым и какие пороги тревожные.

→ [iteration-3-metrics-guide/plan.md](impl/observability/iteration-3-metrics-guide/plan.md)

---

## Задача 10: Документ «ключевые метрики» 📋

### Цель

Справочник для MVP: что мониторим, где смотреть, типичные симптомы.

### Состав работ

- [ ] Создать [`devops/monitoring/key-metrics.md`](../../devops/monitoring/key-metrics.md)
- [ ] Разделы:
  - **Availability** — UptimeRobot, что значит Down
  - **Errors** — GlitchTip issue rate, новые regressions
  - **Backend RED** — RPS, error rate %, p95 latency (пороги для MVP)
  - **VPS/Container** — CPU >80%, RAM >85%, disk >90%
  - **PostgreSQL** (post-MVP note) — connections, slow queries
  - **GlitchTip traces** — когда поднять `GLITCHTIP_TRACES_SAMPLE_RATE`
- [ ] Ссылка из [ADR-005](../adr/adr-005-observability.md), [architecture.md](../architecture.md), [monitoring/README.md](../../devops/monitoring/README.md)

### Артефакты

- `devops/monitoring/key-metrics.md`

### Definition of Done

**Пользователь:** по документу можно провести первичную диагностику без агента.

### Skill

**`grafana-dashboards`** (согласование панелей с текстом)

### Документы

- 📋 [План](impl/observability/iteration-3-metrics-guide/tasks/task-10-key-metrics-doc/plan.md)
- 📝 [Summary](impl/observability/iteration-3-metrics-guide/tasks/task-10-key-metrics-doc/summary.md)

---

## Связь с plan.md и architecture

| Источник | Связь |
|----------|-------|
| [plan.md — Post-MVP](../plan.md#post-mvp-не-в-таблице-этапов) | observability после prod deploy ✅ |
| [architecture.md — Observability](../architecture.md) | ADR-005, monitoring compose |
| [tasklist-devops.md](tasklist-devops.md) | VPS, CD, `make stack-health` — prerequisite |
| [ADR-005](../adr/adr-005-observability.md) | принятый стек |

## Make-команды (observability)

| Команда | Действие |
|---------|----------|
| `make monitoring-up` | Dozzle + bridge (+ Prometheus/Grafana после task 08) |
| `make monitoring-down` | остановить monitoring profile |
| `make monitoring-ps` | статус |
| `make monitoring-logs SVC=...` | логи |
