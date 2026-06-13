# Task 06: Документирование backend

Опирается на [iteration-3-delivery/plan.md](../../plan.md) · [task-05-api-impl](../../../iteration-2-core/tasks/task-05-api-impl/plan.md) · [ADR-002](../../../../../../adr/adr-002-backend-stack.md)

Skills: [fastapi-templates](.agents/skills/fastapi-templates/SKILL.md) — Health and Monitoring, Documentation with OpenAPI

## Цель

Онбординг разработчика: воспроизводимый запуск backend + PostgreSQL, полная документация конфигурации и API. Новый участник поднимает stack **только** по `backend/README.md` (или секции корневого README) и `.env.example`.

## Текущее состояние

| Компонент | Статус | Проблема |
|-----------|--------|----------|
| `docker-compose.yml` | только PostgreSQL, порт **5433** | нет healthcheck, не описан в README |
| `Makefile` | `backend-*` targets ✅ | нет export/check OpenAPI |
| Корневой `README.md` | краткий блок backend (5 строк) | недостаточно для онбординга |
| `backend/README.md` | отсутствует | — |
| `.env.example` | базовые переменные | мало комментариев (токен с `:`, порт PG) |
| `docs/api/openapi.yaml` | контракт task-02 | может расходиться с runtime `/openapi.json` |
| FastAPI `/docs` | работает | нет явного `securitySchemes` в app (Authorize в Swagger может быть неочевиден) |
| `docs/api/README.md` | устарело | «17 tests», «impl — task-05» |

## Архитектурное решение

### Dev-стек (KISS)

```mermaid
flowchart LR
    Dev["Разработчик"]
    DC["docker compose\npostgres :5433"]
    UV["uvicorn\nmake backend-run :8000"]
    Docs["/docs Swagger"]

    Dev -->|docker compose up -d| DC
    Dev -->|make backend-migrate| DC
    Dev -->|make backend-run| UV
    UV --> DC
    UV --> Docs
```

- **PostgreSQL** — в Docker (как сейчас, порт 5433 из-за конфликта с локальным 5432).
- **Backend** — локально через `make backend-run` (hot reload, проще отладка). **Не** добавляем backend-сервис в compose на этом этапе — иначе дублирование `.env`, миграций и reload; task-08 не про deploy.
- **OpenAPI:** runtime `/openapi.json` + `/docs` — источник для dev; `docs/api/openapi.yaml` — версионируемый контракт в репо. При расхождении — правим yaml.

### Структура документации

| Документ | Роль |
|----------|------|
| `backend/README.md` | **основной** гайд: quick start, env, команды, API, troubleshooting |
| `README.md` (корень) | краткий обзор + ссылка на `backend/README.md` |
| `docs/plan.md` | статус итерации 2 → ✅ Done после task-06 |
| `docs/api/README.md` | актуальный статус impl (21 тест) |
| `.env.example` | все переменные backend с комментариями |

## Фазы реализации

### 1. `backend/README.md` (новый файл)

Содержание (порядок секций):

1. **Назначение** — FastAPI backend, сценарии A/B, ссылки на `docs/api/`.
2. **Prerequisites** — Python 3.12+, [uv](https://docs.astral.sh/uv/), Docker (для PG).
3. **Quick start** — пошагово:
   ```bash
   cp .env.example .env          # заполнить BACKEND_SERVICE_TOKEN, OPENROUTER_API_KEY
   make backend-install          # uv sync
   docker compose up -d          # PostgreSQL на localhost:5433
   make backend-migrate          # alembic upgrade head
   make backend-run              # http://127.0.0.1:8000
   curl http://127.0.0.1:8000/health
   ```
4. **Конфигурация** — таблица env-переменных:

   | Переменная | Обязательна | Описание |
   |------------|-------------|----------|
   | `BACKEND_SERVICE_TOKEN` | да | Bearer для `/api/v1/*`; значения с `:` — в кавычках |
   | `DATABASE_URL` | да | default `postgresql+asyncpg://diaai:diaai@localhost:5433/diaai` |
   | `OPENROUTER_API_KEY` | да (assistant) | LLM; без ключа assistant → 502 |
   | `OPENROUTER_API_KEY` / `LLM_MODEL` / `LLM_MAX_HISTORY` | нет | см. `backend/config.py` |
   | `BACKEND_HOST` / `BACKEND_PORT` | нет | default 127.0.0.1:8000 |

5. **Команды Makefile** — `backend-install`, `backend-run`, `backend-migrate`, `backend-test`, `backend-lint`, `backend-format`.
6. **API и auth** — `/docs`, `/redoc`, `Authorization: Bearer <BACKEND_SERVICE_TOKEN>`, `telegram_id` в body/query; `/health` без auth.
7. **Примеры curl** — assistant (text), food create, food list (с Bearer).
8. **Troubleshooting** — порт 5433 vs 5432; 401 (токен); 502 (OpenRouter key); PG не поднят → 503.
9. **Тесты** — `make backend-test` (21 тест), smoke: `test_health.py`, `test_auth.py`.

### 2. docker-compose.yml

Минимальные улучшения (без backend-сервиса):

```yaml
services:
  postgres:
    ...
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U diaai -d diaai"]
      interval: 5s
      timeout: 5s
      retries: 5
```

- Комментарий в yml: порт 5433 на host, backend запускается отдельно.
- Описать в `backend/README.md`.

### 3. OpenAPI sync

**Процедура сверки:**

1. Запустить backend: `make backend-run`.
2. Сохранить runtime spec: `curl -s http://127.0.0.1:8000/openapi.json > /tmp/openapi.runtime.json`.
3. Сравнить paths и ключевые schemas с `docs/api/openapi.yaml` (ручной diff или `diff` по paths).
4. Обновить `docs/api/openapi.yaml` при расхождениях (поля request/response, коды ошибок, tags).
5. Обновить `docs/tech/api-contracts.md` только если меняется карта endpoint'ов (не ожидается).

**Улучшение Swagger (опционально, если Authorize не работает):**

В `backend/main.py` — явный `openapi_components` / `swagger_ui_init_oauth` не нужен; достаточно задокументировать в README, что в Authorize вводится **только значение** токена (без `Bearer`).

**Makefile (опционально):**

```makefile
backend-openapi-export:
	curl -s http://127.0.0.1:8000/openapi.json | python -m json.tool > docs/api/openapi.generated.json
```

Использовать для diff, **не** коммитить `.generated.json` (добавить в `.gitignore` если создаём).

### 4. `.env.example`

Дополнить комментариями:

```env
# Service token for bot → backend (quote if value contains ':')
BACKEND_SERVICE_TOKEN=change-me

# PostgreSQL (docker compose maps host 5433 → container 5432)
DATABASE_URL=postgresql+asyncpg://diaai:diaai@localhost:5433/diaai
```

Убедиться, что все поля из `backend/config.py` отражены.

### 5. Корневой `README.md`

- Таблица статуса: итерация 2 → ✅ Done (impl + docs), итерация 3 → 🚧 In Progress (task-06).
- Секция «Быстрый старт backend» — 3–4 строки + ссылка на [`backend/README.md`](../../backend/README.md).
- Убрать дублирование длинных инструкций (DRY).

### 6. `docs/plan.md`

- Итерация 2: статус ✅ Done (backend ядро + docs).
- Прогресс: task-06 docs ✅ после реализации.
- Ссылка на `backend/README.md`.

### 7. `docs/api/README.md`

- «21 contract test», impl ✅ (task-05).
- Ссылка: runtime docs → `http://127.0.0.1:8000/docs` после `make backend-run`.

## Затронутые файлы

| Файл | Действие |
|------|----------|
| `backend/README.md` | **создать** |
| `docker-compose.yml` | healthcheck + комментарии |
| `.env.example` | комментарии |
| `README.md` | статус, ссылка на backend README |
| `docs/plan.md` | прогресс итераций |
| `docs/api/README.md` | актуализация |
| `docs/api/openapi.yaml` | sync при расхождении |
| `Makefile` | опционально `backend-openapi-export` |
| `.gitignore` | опционально `openapi.generated.json` |

**Не трогаем:** код handlers/services (кроме openapi metadata в `main.py` — только если нужен security scheme).

## Проверка (DoD)

| # | Критерий | Команда / действие |
|---|----------|-------------------|
| 1 | PG поднимается | `docker compose up -d && docker compose ps` |
| 2 | Миграции | `make backend-migrate` |
| 3 | Backend стартует | `make backend-run` → `/health` 200 |
| 4 | Swagger | `/docs` открывается, Authorize с токеном из `.env` |
| 5 | API smoke | curl assistant/food с Bearer → 200/201 |
| 6 | Тесты | `make backend-test` — 21 passed |
| 7 | OpenAPI | paths в yaml совпадают с `/openapi.json` |
| 8 | Онбординг | прочитать README «с нуля» — все шаги воспроизводимы |

**Агент:** все пункты 1–7 ✅; `summary.md` task-06.

**Пользователь:** поднять stack по README + `.env.example`; OpenAPI совпадает с реализацией.

## Вне scope

- Backend-сервис в docker-compose (production deploy)
- CI/CD, GitHub Actions
- Расширение `/health` (version, DB ping) — task-08
- Structured logging — task-08
- Интеграция бота — task-07

## Риски и mitigations

| Риск | Mitigation |
|------|------------|
| Порт 5432 занят другим PG | Документировать 5433; default в `config.py` уже 5433 |
| Токен с `:` ломает `.env` | Пример в кавычках в README и `.env.example` |
| OpenAPI drift | Процедура сверки в фазе 3; yaml — PR-review при изменении API |
| OpenRouter 502 при онбординге | README: ключ обязателен для assistant; events работают без LLM |

## Следующий шаг

Task-07 — рефакторинг бота на backend API ([plan](../task-07-bot-refactor/plan.md)).
