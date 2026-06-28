# Smoke test — one session

Проверка, что локальное окружение работает end-to-end. Время: **~15–20 мин**.

Опирается на [onboarding.md](onboarding.md) · [how-to-get-tokens.md](how-to-get-tokens.md)

> **Альтернатива — Docker stack:** `make stack-init` (build) или `make stack-pull-registry && make stack-up-registry` ([ghcr-stack.md](devops/ghcr-stack.md)); далее §4 Web smoke на :3000 без `make backend-run` / `make web-dev`.

> **Production VPS:** см. [§ Production VPS](#production-vps-timeweb-cloud) ниже.

---

## 0. Системные зависимости

| Инструмент | Версия | Проверка |
|------------|--------|----------|
| Docker | Desktop или engine | `docker compose version` |
| Python | 3.12+ | `python3 --version` |
| [uv](https://docs.astral.sh/uv/) | latest | `uv --version` |
| Node | 20+ (рекоменд. 24) | `node --version` |
| pnpm | 11.6 | `corepack enable && pnpm --version` |

---

## 1. Окружение

```bash
cp .env.example .env
cp web/.env.example web/.env.local
```

Заполнить в **обоих** env одинаковый `BACKEND_SERVICE_TOKEN` (любая случайная строка, не `change-me`).

| Переменная | Обязательно для smoke | Где |
|------------|----------------------|-----|
| `BACKEND_SERVICE_TOKEN` | да | `.env` + `web/.env.local` |
| `OPENROUTER_API_KEY` | да (assistant, analytics, STT) | `.env` |
| `TELEGRAM_BOT_TOKEN` | только bot smoke | `.env` |

Подробнее: [how-to-get-tokens.md](how-to-get-tokens.md)

```bash
make install          # uv sync
make web-install      # pnpm в web/
```

---

## 2. База + backend

```bash
make db-reset         # PG :5433 + migrate + seed
make backend-run      # :8000 (отдельный терминал)
```

**Проверки:**

```bash
curl -s http://127.0.0.1:8000/health
# {"status":"ok","version":"1.0.0"}

make db-inspect       # users, food_events > 0
```

Если `Address already in use :8000`: `lsof -nP -iTCP:8000 -sTCP:LISTEN` → kill PID.

---

## 3. API smoke (curl)

```bash
export TOKEN="$(grep '^BACKEND_SERVICE_TOKEN=' .env | cut -d= -f2- | tr -d '"')"
export BASE=http://127.0.0.1:8000
```

| # | Проверка | Команда | OK |
|---|----------|---------|-----|
| 1 | Auth resolve | `curl -s -X POST "$BASE/api/v1/web/auth/resolve" -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{"username":"ivan_p"}'` | `role: diabetic` |
| 2 | Patient dashboard | `curl -s "$BASE/api/v1/web/patient/dashboard/summary?patient_telegram_id=900000001" -H "Authorization: Bearer $TOKEN"` | `kpis` |
| 3 | Leaderboard | `curl -s "$BASE/api/v1/web/leaderboard?doctor_telegram_id=162684825" -H "Authorization: Bearer $TOKEN"` | `table` |
| 4 | Assistant | `curl -s -X POST "$BASE/api/v1/assistant/messages" -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{"telegram_id":900000001,"text":"Привет"}'` | `reply` |
| 5 | Analytics NL (doctor) | `curl -s -X POST "$BASE/api/v1/web/analytics/query?doctor_telegram_id=162684825" -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{"question":"Сколько ХЕ за 7 дней у пациентов?"}'` | HTTP 200, `answer` |
| 6 | Analytics progress | `curl -s "$BASE/api/v1/analytics/progress?telegram_id=900000001&period=week" -H "Authorization: Bearer $TOKEN"` | `period`, `metrics` |
| 7 | Analytics signals | `curl -s "$BASE/api/v1/analytics/signals?telegram_id=900000001&period=week" -H "Authorization: Bearer $TOKEN"` | `signals` array |
| 8 | Analytics recommendations | `curl -s "$BASE/api/v1/analytics/recommendations?telegram_id=900000001&limit=5" -H "Authorization: Bearer $TOKEN"` | `items` array |

Demo users: `@ivan_p` (900000001), `@doctor_ivanov` (162684825).

---

## 4. Web smoke

```bash
make web-dev          # :3000 (отдельный терминал)
```

| # | Действие | OK |
|---|----------|-----|
| 1 | http://localhost:3000/login → `ivan_p` | redirect `/dashboard` |
| 2 | Dashboard — KPI, charts | данные без ошибок |
| 3 | Sidebar Chat → send message | ответ ассистента |
| 4 | Logout → login `doctor_ivanov` | redirect `/leaderboard` |
| 5 | Leaderboard → «Запрос к данным» → «Сколько ХЕ за 7 дней?» | ответ (не ошибка) |

---

## 5. Bot smoke (опционально)

```bash
make run              # нужен TELEGRAM_BOT_TOKEN + backend :8000
```

| # | Действие | OK |
|---|----------|-----|
| 1 | `/start` в Telegram | приветствие |
| 2 | Текст «Сколько ХЕ в яблоке?» | ответ |
| 3 | Voice message | transcribe → ответ |

---

## 6. Quality gate

```bash
make format && make lint && make test    # 109 tests
make web-lint && make web-build
```

---

## Troubleshooting

| Симптом | Решение |
|---------|---------|
| 401 на API | `BACKEND_SERVICE_TOKEN` в `.env` и curl `-H Authorization` |
| 502 assistant/analytics | `OPENROUTER_API_KEY` в `.env` |
| Web «Сервис недоступен» | backend :8000; token в `web/.env.local` |
| Analytics «Не удалось выполнить запрос» | `prompts/analytics_sql.txt` существует; backend reload |
| Seed пустой | `make db-reset` |

---

## Production VPS (Timeweb Cloud)

Stack на VPS: [devops/deploy/README.md](devops/deploy/README.md). Доступ по **IP** (без custom domain): web `:3000`, API `:8000`. После `make stack-up-registry` и `make db-seed` (нужен `uv` на сервере):

| Проверка | Команда / URL |
|----------|----------------|
| Backend health | `curl -sf http://201.51.4.34:8000/health` |
| Web | http://201.51.4.34:3000/login → `ivan_p` → `/dashboard` |
| Login API | `curl -sf -X POST http://201.51.4.34:3000/api/auth/login -H 'Content-Type: application/json' -d '{"username":"ivan_p"}'` → `{"ok":true,"role":"diabetic"}` |
| Postgres снаружи | порт 5433 **не** в ufw; bind `127.0.0.1` only |
| Monitoring UI | SSH tunnel only — [monitoring/README.md](../devops/monitoring/README.md) |
| GlitchTip | hosted EU (SaaS); bridge на VPS `:8080` |

На сервере: `cd /opt/diaai && make stack-health`. Ресурсы (snapshot 2026-06-28): app ~680 MB RAM, monitoring ~450 MB, swap 2 GB — см. [devops/monitoring/README.md](../devops/monitoring/README.md).
