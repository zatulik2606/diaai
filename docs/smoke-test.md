# Smoke test — one session

Проверка, что локальное окружение работает end-to-end. Время: **~15–20 мин**.

Опирается на [onboarding.md](onboarding.md) · [how-to-get-tokens.md](how-to-get-tokens.md)

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

> `/api/v1/analytics/progress` — contract only (impl task 10); не включать в smoke до impl.

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
make format && make lint && make test    # 84 tests
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
