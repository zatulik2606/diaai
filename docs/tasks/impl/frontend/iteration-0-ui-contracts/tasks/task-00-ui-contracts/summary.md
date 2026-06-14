# Task 00: Summary — UI-требования и API-контракты

Опирается на [plan.md](plan.md) · [iteration-0/summary.md](../../summary.md)

## Что сделано

1. **`docs/spec/frontend-requirements.md`** — 4 зоны UI (dashboard, leaderboard, FAB chat, matrix), wireframes, MVP auth, сверка D*/Doc* → сущности
2. **`docs/spec/frontend-design-system.md`** — tbench dark tokens, компоненты shadcn, layout, a11y
3. **`docs/api/frontend-contract.md`** — 8 web endpoint'ов + reuse `POST /assistant/messages`; JSON examples, PG mapping, curl smoke
4. **`docs/api/openapi.yaml`** — tag `web`, paths `/api/v1/web/*`, schemas
5. Обновлены: `docs/spec/README.md`, `docs/integrations.md`, `docs/api/api-contract.md`, `docs/api/api-contract-review.md`, `docs/tasks/tasklist-frontend.md`, `impl/frontend/plan.md`, `iteration-0/plan.md`
6. Переименование: `frontend-ui-requirements.md` → **`frontend-requirements.md`**

## Отклонения от плана

- Нет. Документ «frontend contract v1» использует `/api/v1/web/` вместо отдельного `/api/v2/` — согласовано с [conventions.md](../../../../../../api/conventions.md).

## Принятые решения

| Решение | Обоснование |
|---------|-------------|
| Префикс `/api/v1/web/` | non-breaking; отделение от bot endpoint'ов |
| KPI: active_patients, total_xe, questions, food_events | покрывает Doc1/Doc2 и доступные таблицы PG |
| «Сдачи» → food_event + photo_analysis | маппинг tbench → diaai |
| Auth resolve через POST | action endpoint; JWT — iter 2 client-side |
| `detail_url` в submissions — frontend routes | backend не знает Next routes |

## Open questions → iter 1

| Вопрос | Рекомендация |
|--------|--------------|
| `telegram_username` отсутствует в `users` | seed-map + опционально миграция `003` |
| Привязка patient → doctor cohort | все diabetics в seed на MVP; фильтр через consultations post-MVP |

## api-design-principles review

Полный review **[api-contract-review.md](../../../../../../api/api-contract-review.md)** (14 pass · 9 warn · 0 fix) — после интеграции web в api-contract.

Кратко (frontend-contract, iter 0):

| Критерий | Статус | Комментарий |
|----------|--------|-------------|
| Resource-oriented URLs | **pass** | `/web/doctor/dashboard/*`, `/web/leaderboard` |
| HTTP semantics GET/POST | **pass** | reads GET; auth resolve POST |
| Consistent naming snake_case | **pass** | aligned with api v1 |
| Pagination on lists | **pass** | `limit`/`offset` + `total` |
| Error format ErrorBody | **pass** | documented per endpoint |
| Examples in contract | **pass** | JSON + curl |
| Versioning | **pass** | v1 extensions, no breaking v2 |
| Username lookup without DB column | **warn** | MVP seed-map; fix in iter 1 |
| `doctor_telegram_id` in query vs header | **warn** | acceptable for MVP BFF |
| Leaderboard combined table+scatter | **warn** | convenience DTO |
| `POST /auth/resolve` RPC-style | **warn** | MVP login |
| Bot GET food unpaginated | **warn** | backlog |
| Dual 422 format | **warn** | backlog |

## Проблемы

Нет блокеров. Код не менялся — make-команды не применялись.
