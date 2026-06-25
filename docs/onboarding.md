# Onboarding: новый разработчик

Пошаговый гайд входа в **diaai**. Архитектура: [architecture.md](architecture.md) · быстрый обзор: [README.md](../README.md).

> Продукт: справочная поддержка при диабете. **Не назначаем дозы инсулина**, не заменяем врача.

---

## 1. Клонирование и первичная настройка

### Prerequisites

| Инструмент | Версия | Проверка |
|------------|--------|----------|
| Git | — | `git --version` |
| Python | 3.12+ | `python3 --version` |
| [uv](https://docs.astral.sh/uv/) | latest | `uv --version` |
| Docker | Desktop / engine | `docker compose version` |
| Node | 20+ (рекоменд. 24, см. `web/.nvmrc`) | `node --version` |
| pnpm | 11.6 | `corepack enable && corepack prepare pnpm@11.6.0 --activate` |
| make, curl | — | опционально `jq` для smoke |

### Клонирование

```bash
git clone <repo-url> diaai
cd diaai
```

### Env-файлы

```bash
cp .env.example .env
cp web/.env.example web/.env.local
```

| Переменная | Где | Обязательно |
|------------|-----|-------------|
| `BACKEND_SERVICE_TOKEN` | `.env` + `web/.env.local` | да (одинаковое значение, не `change-me`) |
| `OPENROUTER_API_KEY` | `.env` | да для assistant, STT, Text-to-SQL |
| `TELEGRAM_BOT_TOKEN` | `.env` | только для bot |
| `DATABASE_URL` | `.env` | default OK для local |

Как получить ключи: [how-to-get-tokens.md](how-to-get-tokens.md).

### Зависимости

```bash
make install        # uv sync — bot + backend
make web-install    # pnpm в web/
```

### Docker stack (рекомендуется для demo)

Один сценарий вместо нескольких терминалов — корневой [`docker-compose.yml`](../docker-compose.yml), два режима в **одном** файле (profiles):

| Режим | Команды | Гайд |
|-------|---------|------|
| **Build** (local `docker build`) | `make stack-init` → `make stack-health` | [docker-compose-local.md](devops/docker-compose-local.md) |
| **Registry** (GHCR, без build) | `make stack-pull-registry && make stack-up-registry && make stack-health` | [ghcr-stack.md](devops/ghcr-stack.md) |

```bash
cp .env.example .env   # BACKEND_SERVICE_TOKEN, OPENROUTER_API_KEY
make stack-init        # db-reset + stack-up (build)
make stack-health
# http://localhost:3000/login → ivan_p
```

Host dev (hot reload, pytest): §2 ниже · `make db-up` поднимает **только** postgres.

**Production VPS** (Timeweb Cloud, registry stack): [devops/deploy/README.md](devops/deploy/README.md) · smoke: [smoke-test.md § Production VPS](smoke-test.md#production-vps-timeweb-cloud).

---

## 2. Настройка каждого компонента

### PostgreSQL

```bash
make db-reset       # down -v → up → migrate 001→003 → seed
```

| Параметр | Значение |
|----------|----------|
| Host port | **5433** (не 5432, если занят локальный PG) |
| User/DB | `diaai` / `diaai` |
| Compose | [docker-compose.yml](../docker-compose.yml) |

Дополнительно: `make db-shell`, `make db-migrate`, `make db-seed`.

### Backend (FastAPI)

```bash
make backend-run    # http://127.0.0.1:8000, reload
```

| Что | Где |
|-----|-----|
| Entry | `backend/main.py` |
| Routes | `backend/api/v1/` |
| Config | `backend/config.py`, `.env` |
| Swagger | http://127.0.0.1:8000/docs |

Guide: [backend/README.md](../backend/README.md).

### Web (Next.js)

```bash
make web-dev        # http://localhost:3000
```

| Что | Где |
|-----|-----|
| App | `web/app/` |
| BFF | `web/app/api/` |
| Env | `web/.env.local` |
| UI | shadcn + Tailwind |

Guide: [web/README.md](../web/README.md). Login demo: `ivan_p` / `doctor_ivanov`.

### Telegram bot

```bash
make run            # нужны backend :8000 + TELEGRAM_BOT_TOKEN
```

| Что | Где |
|-----|-----|
| Entry | `src/diaai/main.py` |
| Handlers | `src/diaai/handlers.py` |
| HTTP client | `src/diaai/backend_client.py` |

Guide: [src/diaai/README.md](../src/diaai/README.md).

---

## 3. Проверка, что всё работает

Минимум после шага 2 (backend + DB):

```bash
curl -s http://127.0.0.1:8000/health
```

**Ожидается:** `{"status":"ok","version":"1.0.0"}`

```bash
make db-inspect
```

**Ожидается:** `users` > 0, `food_events` > 0, 9 tables.

### API (curl)

```bash
export TOKEN="$(grep '^BACKEND_SERVICE_TOKEN=' .env | cut -d= -f2- | tr -d '"')"
export BASE=http://127.0.0.1:8000

curl -s -X POST "$BASE/api/v1/web/auth/resolve" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"username":"ivan_p"}'
# → "role":"diabetic", "telegram_id":900000001

curl -s "$BASE/api/v1/web/patient/dashboard/summary?patient_telegram_id=900000001" \
  -H "Authorization: Bearer $TOKEN"
# → JSON с "kpis":[...]
```

### Web

1. http://localhost:3000/login → username `ivan_p`
2. **OK:** redirect на `/dashboard`, KPI без «Сервис недоступен»
3. Sidebar Chat → сообщение → **OK:** ответ ассистента (нужен `OPENROUTER_API_KEY`)

### Bot (опционально)

`/start` → текст «Сколько ХЕ в яблоке?» → **OK:** ответ от backend.

**Полный чеклист (~15 мин):** [smoke-test.md](smoke-test.md).

---

## 4. Куда смотреть в первую очередь

### Архитектурные точки входа

| Тема | Файл / документ |
|------|-----------------|
| Общая схема | [architecture.md](architecture.md) |
| Product + roadmap | [plan.md](plan.md), [vision.md](vision.md) |
| REST контракт | [api/api-contract.md](api/api-contract.md) |
| Web DTO | [api/frontend-contract.md](api/frontend-contract.md) |
| Домен | [data-model.md](data-model.md), [spec/user-scenarios.md](spec/user-scenarios.md) |

### Код по потоку запроса

```text
Telegram → src/diaai/handlers.py → backend_client.py
              → backend/api/v1/assistant.py → services/assistant_service.py
              → repositories/ → PostgreSQL

Web browser → web/app/api/* (BFF) → backend/api/v1/web/*
              → services/web_*.py → repositories/
```

| Компонент | Ключевые пути |
|-----------|---------------|
| Backend routing | `backend/api/v1/router.py`, `backend/api/v1/web/router.py` |
| LLM | `backend/services/llm_service.py`, `prompts/system.txt` |
| Text-to-SQL | `backend/services/analytics_query_service.py`, `prompts/analytics_sql.txt` |
| Web dashboard | `web/app/(app)/dashboard/`, `backend/services/web_patient_service.py` |
| Auth BFF | `web/app/api/auth/login/route.ts` |
| Migrations | `alembic/versions/` |
| Seed | `data/progress-import.v1.json`, `scripts/db/seed_from_progress.py` |

### Demo-данные

| Username | telegram_id | Роль | Web redirect |
|----------|-------------|------|--------------|
| `ivan_p` | 900000001 | diabetic | `/dashboard` |
| `doctor_ivanov` | 162684825 | doctor | `/leaderboard` |

---

## 5. Рабочий процесс

Spec-driven workflow ([templates/workflow.md](templates/workflow.md)):

```text
Область (backend / frontend / bot / database)
  → итерация (plan.md + summary.md)
    → задача (tasks/task-NN/plan.md + summary.md)
      → код + тесты
```

| Область | Tasklist |
|---------|----------|
| backend | [tasks/tasklist-backend.md](tasks/tasklist-backend.md) — сейчас iter 4 🚧 |
| frontend | [tasks/tasklist-frontend.md](tasks/tasklist-frontend.md) — 10/10 ✅ |
| database | [tasks/tasklist-database.md](tasks/tasklist-database.md) — 5/5 ✅ |
| bot | [tasks/tasklist-bot.md](tasks/tasklist-bot.md) |

**Правила:** не начинать итерацию без `plan.md`; не закрывать задачу без `summary.md`. Код: [.cursor/rules/conventions.mdc](../.cursor/rules/conventions.mdc).

---

## 6. Как готовить изменения

### Quality gate

```bash
make format && make lint && make test    # 84 tests
make web-lint && make web-build          # если меняли web/
```

### Чеклист перед PR

- [ ] `.env` не в коммите
- [ ] API изменения → `docs/api/api-contract.md` + `openapi.yaml` + тесты
- [ ] Новая фича для onboarding → пункт в [smoke-test.md](smoke-test.md)
- [ ] Счётчик тестов в [README.md](../README.md) актуален (`make test`)

### Частые проблемы

| Симптом | Действие |
|---------|----------|
| `:8000` busy | `lsof -nP -iTCP:8000 -sTCP:LISTEN` → kill PID |
| 502 assistant | `OPENROUTER_API_KEY` в `.env` |
| Web «Сервис недоступен» | backend running; token в `web/.env.local` |
| Text-to-SQL ошибка | файл `prompts/analytics_sql.txt` в корне репо |
| Пустой dashboard | `make db-reset` |

---

## Дополнительно: маршрут чтения по дням

| День | Тема | Документы |
|------|------|-----------|
| 1 | картина + запуск | idea, vision, architecture, plan, README |
| 2 | домен + данные | data-model, user-scenarios, schema-er |
| 3 | API + интеграции | api-contract, frontend-contract, integrations, ADR |
| 4 | процесс | workflow, tasklist области |

Сводки: [tasks/impl/frontend/summary.md](tasks/impl/frontend/summary.md) · [tasks/impl/backend/summary.md](tasks/impl/backend/summary.md) · [tasks/impl/database/summary.md](tasks/impl/database/summary.md).

Фичи: [voice-limitations.md](spec/voice-limitations.md) · [text-to-sql-architecture.md](spec/text-to-sql-architecture.md).
