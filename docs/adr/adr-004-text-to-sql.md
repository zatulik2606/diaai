# ADR-004: Text-to-SQL для ad-hoc аналитики (read-only)

| | |
|---|---|
| **Статус** | Принято |
| **Дата** | 2026-06-07 |
| **Контекст** | Frontend iter 9 — вопросы по данным БД в web UI |

## Контекст

Пользователь (пациент или доктор) задаёт вопрос на естественном языке («сколько ХЕ за неделю у пациента X»). Ответ должен опираться на **PostgreSQL**, а не на галлюцинации LLM.

Assistant (D2) остаётся plain chat без tools. Backend iter 4 (REST `/analytics/progress`) — отдельный track; web dashboard уже агрегирует KPI через fixed repos.

## Рассмотренные альтернативы

### 1. Assistant tool `query_analytics` ❌

LLM в чате вызывает tool → SQL → ответ в thread.

**Минусы:** сложнее guardrails в dialog flow; UI таблицы/графика в чате; iter 9 scope — dedicated UI.

**Вердикт:** out of scope iter 9.

### 2. Semantic layer (fixed functions) ❌

LLM выбирает из каталога `sum_xe_in_window`, `top_patients` и т.д.

**Минусы:** не Text-to-SQL; каждый новый вопрос = новая функция.

**Вердикт:** отложить как fallback при росте рисков SQL injection.

### 3. LLM → SQL + SqlGuard + read-only execute ✅

Dedicated endpoint `POST /api/v1/web/analytics/query` + web panel «Вопрос по данным».

**Плюсы:** гибкие ad-hoc вопросы; SQL не отдаётся клиенту; единый guard для всех ролей.

**Минусы:** риск невалидного SQL; нужен parse/validate (`sqlglot`).

## Решение

- **Endpoint:** `POST /api/v1/web/analytics/query` — `{ question }` → `{ answer, columns, rows, chart_hint }`
- **Pipeline:** LLM генерирует SQL → `SqlGuard` → execute через SQLAlchemy `text()` → format ответа
- **Auth:** как dashboard — `patient_telegram_id` / `doctor_telegram_id` + service token (BFF)
- **Scope:** diabetic — SQL обязан фильтровать `user_id` текущего пользователя; doctor — когорта без авто-filter

### Guardrails

| Правило | Значение |
|---------|----------|
| Тип запроса | только `SELECT`, один statement |
| Таблицы (allowlist) | `users`, `food_events`, `insulin_events`, `progress_snapshots`, `dialog_requests`, `photo_analyses` |
| Колонки `users` | `id`, `display_name`, `role`, `telegram_id`, `telegram_username` |
| Row limit | ≤ 100 (принудительно) |
| Query timeout | 5 s (`ANALYTICS_QUERY_TIMEOUT_SECONDS`) |
| SQL в response | **не отдаётся** клиенту |

### Out of scope

- INSERT/UPDATE/DELETE, DDL, `EXPLAIN`, system catalogs
- Bot / Telegram data questions
- Assistant function calling
- Backend iter 4 REST analytics (параллельно, не дублировать)

## Последствия

- Зависимость `sqlglot` в backend
- Prompt [`prompts/analytics_sql.txt`](../../prompts/analytics_sql.txt) с DDL-контекстом
- Golden scenarios: [`docs/spec/text-to-sql-scenarios.md`](../spec/text-to-sql-scenarios.md)
- Архитектура и roadmap: [`docs/spec/text-to-sql-architecture.md`](../spec/text-to-sql-architecture.md)
- При росте нагрузки — semantic layer или materialized views (backend iter 4) без смены UI контракта
