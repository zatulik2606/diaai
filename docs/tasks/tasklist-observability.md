# Observability Tasklist

Опирается на [plan.md](../plan.md) · [architecture.md](../architecture.md) · [ADR-005](../adr/adr-005-observability.md) · [devops/monitoring/README.md](../../devops/monitoring/README.md)

## Обзор

Рабочий план области **observability**: довести до prod стек из ADR-005 — **GlitchTip EU** (ошибки), **Uptime Kuma** (доступность, self-hosted), **Dozzle** (логи), **Prometheus + Grafana** (метрики и дашборды).

| Итерация | Фокус | Инструменты |
|----------|-------|-------------|
| **1** | Отслеживание ошибок + алерты в Telegram | GlitchTip, `sentry-sdk`, `@sentry/nextjs`, `@diaaialarm_bot`, bridge |
| **2** | Мониторинг доступности | Uptime Kuma (compose `monitoring`) |
| **3** | Логи и метрики | Dozzle, Prometheus, Grafana |
| **3.1** | Справочник ключевых метрик | docs |

**Текущее состояние (baseline):**

| Компонент | Локально | Prod |
|-----------|----------|------|
| GlitchTip ingest (backend/web) | ✅ `GLITCHTIP_*` | ✅ debug smoke |
| `@diaaialarm_bot` + `TELEGRAM_ALARM_*` | ✅ | ✅ |
| `glitchtip-telegram-bridge` + Dozzle | ✅ `make monitoring-up` | ✅ `:8080` + `:8888` localhost |
| GlitchTip → webhook → Telegram | ✅ UI `:8080/webhook` | ✅ auto POST GlitchTip EU |
| Uptime Kuma monitors | ✅ | ✅ 3 monitor + bridge alerts |
| Prometheus + Grafana + dashboards | ✅ compose + prod | ✅ |
| Loki + Grafana alerts | ✅ compose + prod | ✅ |
| Runbook key-metrics | ✅ | ✅ |

**Прогресс:** **10 / 10** задач · observability MVP ✅ (prod verified 2026-06-26)

**Prod-стратегия (2026-06-28, вариант 1):** app + monitoring stack на **одном VPS** `201.51.4.34` (2 vCPU / 4 GB). Отдельный VPS или managed Grafana у Timeweb **не** используем. Запас по RAM — **swap 2 GB** (`devops/server/bootstrap.sh`, `SWAP_GB=2`); UI monitoring — только SSH tunnel. GlitchTip — **hosted EU** (SaaS), bridge на VPS. Snapshot RAM: app ~680 MB, monitoring ~450 MB, host ~1.4/3.8 GB до swap — [monitoring/README.md](../../devops/monitoring/README.md) · [key-metrics.md](../../devops/monitoring/key-metrics.md).

> **Scope MVP:** без self-hosted GlitchTip и ELK. На prod-VPS в profile `monitoring`: Dozzle, **Loki**, Prometheus, Grafana (dashboards + **alerting**), Kuma, bridge — см. [ADR-005](../adr/adr-005-observability.md).

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
| 1 | Отслеживание ошибок + алерты | 01–04 | ✅ Done | [plan](impl/observability/iteration-1-error-tracking/plan.md) · [summary](impl/observability/iteration-1-error-tracking/summary.md) |
| 2 | Мониторинг доступности | 05–06 | ✅ Done | [plan](impl/observability/iteration-2-uptime/plan.md) · [summary](impl/observability/iteration-2-uptime/summary.md) |
| 3 | Логи и метрики | 07–09 | ✅ Done | [plan](impl/observability/iteration-3-logs-metrics/plan.md) · [summary](impl/observability/iteration-3-logs-metrics/summary.md) |
| 3.1 | Ключевые метрики (docs) | 10 | ✅ Done | [plan](impl/observability/iteration-3-metrics-guide/plan.md) · [summary](impl/observability/iteration-3-metrics-guide/summary.md) |

## Список задач

| Задача | Описание | Статус | Документы |
|--------|----------|--------|-----------|
| 01 | GlitchTip на prod: env, ingest backend + web | ✅ | [план](impl/observability/iteration-1-error-tracking/tasks/task-01-glitchtip-prod/plan.md) · [summary](impl/observability/iteration-1-error-tracking/tasks/task-01-glitchtip-prod/summary.md) |
| 02 | Monitoring stack на prod: bridge + alarm bot | ✅ | [план](impl/observability/iteration-1-error-tracking/tasks/task-02-bridge-prod/plan.md) · [summary](impl/observability/iteration-1-error-tracking/tasks/task-02-bridge-prod/summary.md) |
| 03 | GlitchTip Alert receivers → webhook | ✅ | [план](impl/observability/iteration-1-error-tracking/tasks/task-03-glitchtip-webhook/plan.md) · [summary](impl/observability/iteration-1-error-tracking/tasks/task-03-glitchtip-webhook/summary.md) |
| 04 | E2E: ошибка → GlitchTip → Telegram | ✅ | [план](impl/observability/iteration-1-error-tracking/tasks/task-04-error-alert-e2e/plan.md) · [summary](impl/observability/iteration-1-error-tracking/tasks/task-04-error-alert-e2e/summary.md) |
| 05 | `/health` + DB probe; Uptime Kuma compose | ✅ | [план](impl/observability/iteration-2-uptime/tasks/task-05-health-kuma/plan.md) · [summary](impl/observability/iteration-2-uptime/tasks/task-05-health-kuma/summary.md) |
| 06 | Kuma monitors + Telegram; acceptance §9 п.4–5 | ✅ | [план](impl/observability/iteration-2-uptime/tasks/task-06-uptime-verify/plan.md) · [summary](impl/observability/iteration-2-uptime/tasks/task-06-uptime-verify/summary.md) |
| 07 | Dozzle на prod + SSH tunnel | ✅ | [план](impl/observability/iteration-3-logs-metrics/tasks/task-07-dozzle-prod/plan.md) · [summary](impl/observability/iteration-3-logs-metrics/tasks/task-07-dozzle-prod/summary.md) |
| 08 | Prometheus + Grafana (compose monitoring) | ✅ | [план](impl/observability/iteration-3-logs-metrics/tasks/task-08-prometheus-grafana/plan.md) · [summary](impl/observability/iteration-3-logs-metrics/tasks/task-08-prometheus-grafana/summary.md) |
| 09 | Grafana dashboards: FastAPI + VPS | ✅ | [план](impl/observability/iteration-3-logs-metrics/tasks/task-09-grafana-dashboards/plan.md) · [summary](impl/observability/iteration-3-logs-metrics/tasks/task-09-grafana-dashboards/summary.md) |
| 10 | Документ «ключевые метрики» | ✅ | [план](impl/observability/iteration-3-metrics-guide/tasks/task-10-key-metrics-doc/plan.md) · [summary](impl/observability/iteration-3-metrics-guide/tasks/task-10-key-metrics-doc/summary.md) |

Задачи выполняются **последовательно** (01 → 10). Итерация N — после закрытия N−1.

---

## Итерация 1 — Отслеживание ошибок + алерты ✅

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

## Задача 04: E2E — GlitchTip → Telegram ✅

✅ [План](impl/observability/iteration-1-error-tracking/tasks/task-04-error-alert-e2e/plan.md) · [Summary](impl/observability/iteration-1-error-tracking/tasks/task-04-error-alert-e2e/summary.md)

Runbook: [monitoring/README.md § E2E iter 1](../../devops/monitoring/README.md#e2e-iter-1-task-04--ingest--alert). Smoke VPS 2026-06-07 (debug 200); webhook delivery — task 03 + логи `165.227.159.10`.

### Документы

- ✅ [План](impl/observability/iteration-1-error-tracking/tasks/task-04-error-alert-e2e/plan.md)
- ✅ [Summary](impl/observability/iteration-1-error-tracking/tasks/task-04-error-alert-e2e/summary.md)

---

## Итерация 2 — Мониторинг доступности ✅

**Ценность:** алерт при недоступности backend (в т.ч. БД) или web; история проверок в UI Kuma.

**План итерации:** [impl/observability/iteration-2-uptime/plan.md](impl/observability/iteration-2-uptime/plan.md)

**Отклонение от ADR-005:** Uptime **Kuma** (self-hosted, `:3002`) вместо UptimeRobot SaaS.

**Результат итерации:**
- `GET /health` — `SELECT 1` → 200 или 503
- Uptime Kuma в `make monitoring-up`; UI `127.0.0.1:3002` (SSH tunnel)
- мониторы: backend `/health` (keyword `"status":"ok"`), web `/`
- Telegram — **пользователь** в UI Kuma (token + chat_id)
- acceptance §9 пункты 4–5 ✅

**Skill:** `docker-expert` (task 05)

→ [iteration-2-uptime/plan.md](impl/observability/iteration-2-uptime/plan.md)

---

## Задача 05: `/health` + Uptime Kuma ✅

✅ [План](impl/observability/iteration-2-uptime/tasks/task-05-health-kuma/plan.md) · [Summary](impl/observability/iteration-2-uptime/tasks/task-05-health-kuma/summary.md)

`/health` с `SELECT 1`; `uptime-kuma` в compose (`:3002`). Runbook: [uptime-kuma.md](../../devops/monitoring/uptime-kuma.md).

### Документы

- ✅ [План](impl/observability/iteration-2-uptime/tasks/task-05-health-kuma/plan.md)
- ✅ [Summary](impl/observability/iteration-2-uptime/tasks/task-05-health-kuma/summary.md)

---

## Задача 06: Kuma monitors + acceptance ✅

✅ Telegram через bridge подтверждён пользователем. §9 п.4–5 ✅.

---

## Итерация 3 — Логи и метрики ✅

**Ценность:** при инциденте — логи всех контейнеров в одном UI; дашборды RED для FastAPI и ресурсов VPS.

**Результат итерации:**
- Dozzle на prod (localhost + SSH tunnel)
- Prometheus + Grafana в profile `monitoring`
- dashboards FastAPI + host/container
- документ ключевых метрик (iter 3.1)

**Skills:** `docker-expert` · **`grafana-dashboards`**

→ [iteration-3-logs-metrics/plan.md](impl/observability/iteration-3-logs-metrics/plan.md)

---

## Задача 07: Dozzle на prod + SSH tunnel ✅

✅ [План](impl/observability/iteration-3-logs-metrics/tasks/task-07-dozzle-prod/plan.md) · [Summary](impl/observability/iteration-3-logs-metrics/tasks/task-07-dozzle-prod/summary.md)

Tunnel (prod, порт **18888** — не конфликтует с local Dozzle):

```bash
ssh -i ~/.ssh/diaai-deploy -L 18888:127.0.0.1:8888 deploy@201.51.4.34
# http://127.0.0.1:18888
```

### Документы

- ✅ [План](impl/observability/iteration-3-logs-metrics/tasks/task-07-dozzle-prod/plan.md)
- ✅ [Summary](impl/observability/iteration-3-logs-metrics/tasks/task-07-dozzle-prod/summary.md)

---

## Задача 08: Prometheus + Grafana (compose monitoring) ✅

✅ [План](impl/observability/iteration-3-logs-metrics/tasks/task-08-prometheus-grafana/plan.md) · [Summary](impl/observability/iteration-3-logs-metrics/tasks/task-08-prometheus-grafana/summary.md)

Tunnel (prod):

```bash
ssh -i ~/.ssh/diaai-deploy -L 13001:127.0.0.1:3001 -L 19090:127.0.0.1:9090 deploy@201.51.4.34
# Grafana → http://127.0.0.1:13001
# Prometheus targets → http://127.0.0.1:19090/targets
```

### Документы

- ✅ [План](impl/observability/iteration-3-logs-metrics/tasks/task-08-prometheus-grafana/plan.md)
- ✅ [Summary](impl/observability/iteration-3-logs-metrics/tasks/task-08-prometheus-grafana/summary.md)

---

## Задача 09: Grafana dashboards — FastAPI + VPS ✅

✅ [План](impl/observability/iteration-3-logs-metrics/tasks/task-09-grafana-dashboards/plan.md) · [Summary](impl/observability/iteration-3-logs-metrics/tasks/task-09-grafana-dashboards/summary.md)

Grafana → **Dashboards → diaai**:
- `diaai Backend RED` — RPS, 5xx %, p50/p95
- `diaai FastAPI Observability` — totals, 2xx/5xx %, p99, RPS, CPU/RAM (Grafana.com #22676)
- `diaai VPS Host` — CPU, RAM, disk, cgroup top

**Grafana alerting:** rules 5xx rate >5% · p95 >2s → **diaai-telegram** → bridge `[Grafana]`. Smoke: `/debug/error-test` — см. [monitoring/README § alerting](../../devops/monitoring/README.md#grafana-alerting-5xx--latency).

Tunnel: `ssh -i ~/.ssh/diaai-deploy -L 13001:127.0.0.1:3001 -L 19090:127.0.0.1:9090 deploy@201.51.4.34`

### Документы

- ✅ [План](impl/observability/iteration-3-logs-metrics/tasks/task-09-grafana-dashboards/plan.md)
- ✅ [Summary](impl/observability/iteration-3-logs-metrics/tasks/task-09-grafana-dashboards/summary.md)

---

## Итерация 3.1 — Ключевые метрики (docs) ✅

**Ценность:** при инциденте понятно, **какие** графики смотреть первым и какие пороги тревожные.

→ [iteration-3-metrics-guide/plan.md](impl/observability/iteration-3-metrics-guide/plan.md)

---

## Задача 10: Документ «ключевые метрики» ✅

✅ [План](impl/observability/iteration-3-metrics-guide/tasks/task-10-key-metrics-doc/plan.md) · [Summary](impl/observability/iteration-3-metrics-guide/tasks/task-10-key-metrics-doc/summary.md)

Runbook: [devops/monitoring/key-metrics.md](../../devops/monitoring/key-metrics.md)

### Документы

- ✅ [План](impl/observability/iteration-3-metrics-guide/tasks/task-10-key-metrics-doc/plan.md)
- ✅ [Summary](impl/observability/iteration-3-metrics-guide/tasks/task-10-key-metrics-doc/summary.md)

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

## Prod acceptance (post-close)

Полный чеклист: [devops/deploy/README.md §9](../../devops/deploy/README.md#9-observability-mvp) · runbook: [key-metrics.md](../../devops/monitoring/key-metrics.md).

| # | Критерий | Статус |
|---|----------|--------|
| 1–6 | GlitchTip · bridge · Kuma · Dozzle | ✅ |
| 7–8 | Prometheus/Grafana · dashboards (RED + FastAPI + VPS) | ✅ 2026-06-26 |
| 9 | Loki Explore `{service="backend"} \|= "500 Internal Server Error"` | ✅ |
| 10 | Grafana alert 5xx → Telegram `[Grafana]` | ✅ |
