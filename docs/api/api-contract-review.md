# API design review — api-contract.md (v1)

Контракт: [api-contract.md](api-contract.md) · Web detail: [frontend-contract.md](frontend-contract.md) · Skill: [api-design-principles](../../.agents/skills/api-design-principles/SKILL.md)

Дата review: после интеграции web `/api/v1/web/*` в api-contract (frontend iter 0).

**Scope:** bot endpoint'ы (реализовано ✅) + web endpoint'ы (контракт ✅, impl 📋).

---

## Итог

| Статус | Количество |
|--------|------------|
| Pass | 14 |
| Warn | 9 |
| Fix | 0 |

Контракт **готов к реализации** frontend iter 1. Блокеров нет; warn — осознанные MVP-deferrals или улучшения post-MVP.

---

## Checklist (api-design-principles)

| # | Тема | Статус | Комментарий |
|---|------|--------|-------------|
| 1 | Resource-oriented URLs | **Pass** | `/events/food`, `/assistant/messages`, `/web/doctor/dashboard/*`, `/web/leaderboard` — существительные и иерархия |
| 2 | HTTP method semantics | **Pass** | GET — read (safe); POST — create message/event; 201 для events, 200 для assistant — задокументировано |
| 3 | Consistent naming | **Pass** | `snake_case`, домен `xe`/`bje`, ISO8601 UTC |
| 4 | API versioning | **Pass** | `/api/v1/`; правила breaking → v2 в §Правила изменений |
| 5 | Stateless requests | **Pass** | `telegram_id` / `doctor_telegram_id` в query/body; Bearer на каждый запрос |
| 6 | HTTP status codes | **Pass** | 200/201/400/401/403/404/422/502/503; таблицы ошибок на bot endpoint'ах |
| 7 | Error format consistency | **Warn** | `ErrorBody` для 4xx/5xx; 422 — dual FastAPI `detail` (backlog единого формата) |
| 8 | Pagination collections | **Warn** | Web lists: `limit`/`offset` + `total` ✅; bot `GET /events/food` — голый array без limit (backlog) |
| 9 | OpenAPI / documentation | **Pass** | [openapi.yaml](openapi.yaml) tags `system`, `assistant`, `events`, `web`; bot — JSON examples; web — [frontend-contract.md](frontend-contract.md) |
| 10 | Auth model clarity | **Pass** | Service Bearer + user id в payload/query; BFF для web; token не в браузере |
| 11 | Rate limiting | **Warn** | Не реализовано; 429 зарезервирован в backlog |
| 12 | Idempotency (POST) | **Warn** | Нет `Idempotency-Key` для events; retry → риск дублей (backlog) |
| 13 | POST creates → 201 | **Warn** | `POST /assistant/messages` → **200** (осознанно: ответ диалога, не pure REST create) |
| 14 | Action-style endpoint | **Warn** | `POST /web/auth/resolve` — RPC; допустимо для MVP login lookup |
| 15 | User context in query | **Warn** | `doctor_telegram_id` на каждом doctor GET; альтернатива — header `X-Doctor-Telegram-Id` post-MVP |
| 16 | UI-aggregated DTOs | **Warn** | `/dashboard/summary`, `/leaderboard` (table+scatter) — UI-oriented, не зеркало PG; OK для BFF-layer |
| 17 | Client coupling | **Warn** | `detail_url` в submissions — frontend routes в API; iter 3 может строить URL на клиенте |
| 18 | Over/under-fetching | **Warn** | Leaderboard отдаёт table и scatter одним GET; при росте payload — split или query `include=scatter` |
| 19 | Security (sharp edges) | **Pass** | Service token; 403 на doctor endpoints; username resolve без JWT — scope MVP документирован |
| 20 | Change management | **Pass** | §Правила изменений: contract → openapi → code → tests |

---

## Review по группам endpoint'ов

### Bot (реализовано ✅)

| Endpoint | Pass | Warn |
|----------|------|------|
| `GET /health` | Минимальный health, no auth | — |
| `POST /assistant/messages` | Чёткий request/response, content rules | 200 vs 201 |
| `POST /events/food`, `/insulin` | 201 + id; FK validation 403/404 | — |
| `GET /events/food` | Фильтры `from`/`to` | Нет pagination |

### Web (контракт 📋)

| Endpoint | Pass | Warn |
|----------|------|------|
| `POST /web/auth/resolve` | Body + 404 NOT_FOUND | Verb `resolve` в path |
| `GET …/dashboard/summary` | KPI DTO, query documented | Aggregate RPC |
| `GET …/dashboard/activity` | Time series, `days` default | — |
| `GET …/questions`, `…/submissions` | Paginated wrapper | — |
| `GET …/progress-matrix` | Matrix DTO для зоны 4 | — |
| `GET /web/leaderboard` | Table + scatter params | Combined response |
| `GET /web/assistant/history` | Paginated chat | — |

---

## Рекомендации (не блокируют iter 1)

| Приоритет | Рекомендация | Когда |
|-----------|--------------|-------|
| P2 | Единый формат 422 → `ErrorBody` | post-MVP / backend task-08 |
| P2 | Pagination `GET /events/food` | bot backlog |
| P2 | Cursor pagination для web lists | при больших объёмах |
| P3 | `POST /web/sessions` вместо `auth/resolve` | v2 или alias |
| P3 | `include=scatter` на leaderboard | если payload > 50KB |
| P3 | Убрать `detail_url` из API, отдавать только `id` + `type` | iter 3 frontend |

---

## Согласованность документов

| Пара | Статус |
|------|--------|
| api-contract ↔ frontend-contract | **Pass** — web paths и поля совпадают |
| api-contract ↔ openapi.yaml | **Pass** — tag `web`, schemas |
| api-contract ↔ conventions.md | **Pass** — versioning, ErrorBody |
| api-contract ↔ frontend-requirements.md | **Pass** — 4 зоны → endpoint map |

---

## Вердикт

**Approve для impl** с учётом warn-списка. Изменения контракта перед iter 1 не требуются; warn фиксируются в backlog §MVP-ограничения.
