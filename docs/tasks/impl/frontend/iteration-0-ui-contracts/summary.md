# Итерация frontend 0: Summary

> **Статус:** ✅ Done

Опирается на [plan.md](plan.md) · [tasklist-frontend.md](../../../tasklist-frontend.md)

---

## Сделано

### Task-00: UI-требования и API-контракты ✅

- 4 зоны UI, design system, MVP auth, REST `/api/v1/web/*`
- Интеграция web в [api-contract.md](../../../../api/api-contract.md)
- Design review [api-design-principles](../../../../.agents/skills/api-design-principles/SKILL.md) → [api-contract-review.md](../../../../api/api-contract-review.md)
- Детали: [task-00 summary](tasks/task-00-ui-contracts/summary.md)

| Артефакт | Путь |
|----------|------|
| UI-требования (4 зоны) | [frontend-requirements.md](../../../../spec/frontend-requirements.md) |
| Design system (tbench dark) | [frontend-design-system.md](../../../../spec/frontend-design-system.md) |
| Web API contract | [frontend-contract.md](../../../../api/frontend-contract.md) |
| OpenAPI tag `web` | [openapi.yaml](../../../../api/openapi.yaml) |
| API v1 + web-секция | [api-contract.md](../../../../api/api-contract.md) |
| API design review | [api-contract-review.md](../../../../api/api-contract-review.md) |
| Spec index | [spec/README.md](../../../../spec/README.md) |
| Web integration | [integrations.md](../../../../integrations.md) |
| План области | [impl/frontend/plan.md](../plan.md) |

## Ценность

- Единый контракт для **iter 1** (backend `/api/v1/web/*` + seed) и **iter 2–6** (Next.js экраны)
- Маппинг tbench/преподаватель → доктор, пациенты, метрики — без двусмысленности
- 8 web endpoint'ов + reuse `POST /assistant/messages`; openapi и review зафиксированы

## Решения

| Решение | Обоснование |
|---------|-------------|
| Префикс `/api/v1/web/` | non-breaking extensions в v1 |
| KPI: active_patients, total_xe, questions, food_events | Doc1/Doc2 + таблицы PG |
| «Сдачи» → food_event + photo_analysis | маппинг tbench → diaai |
| Auth: `POST /web/auth/resolve` | MVP username lookup через BFF |
| Файл `frontend-requirements.md` | переименован из `frontend-ui-requirements.md` |

## Отклонения от плана

- Нет по scope. Имя spec-файла: `frontend-requirements.md` (не `frontend-ui-requirements.md`) — уточнение naming.

## Open questions → iter 1

| Вопрос | Рекомендация |
|--------|--------------|
| Нет `telegram_username` в `users` | seed-map / миграция `003` |
| Patient → doctor cohort | все diabetics в seed на MVP |

## api-design-principles review

[api-contract-review.md](../../../../api/api-contract-review.md): **14 pass · 9 warn · 0 fix** — approve для impl.

## Проблемы

Нет блокеров. Код `web/` и backend не менялись.

## DoD итерации

| Кто | Статус |
|-----|--------|
| Self-check (агент) | ✅ 4 зоны; tokens; endpoint'ы + JSON; openapi `web`; согласовано с api v1 / data-model; review |
| User-check | 📋 `frontend-requirements.md` + `frontend-contract.md` |

## Make-команды

Не требовались (документы only).

## Следующий шаг

[Итерация 1 — API для frontend](../iteration-1-frontend-api/plan.md): реализация `/api/v1/web/*`, doctor `@akozhin` (`telegram_id: 162684825`), demo seed для dashboard/leaderboard.
