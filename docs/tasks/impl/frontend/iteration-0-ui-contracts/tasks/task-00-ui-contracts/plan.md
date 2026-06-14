# Task 00: UI-требования и API-контракты frontend

Опирается на [iteration-0/plan.md](../../plan.md) · [tasklist-frontend.md](../../../../../tasklist-frontend.md)

## Цель

Описать 4 зоны UI, design system, MVP auth и REST-контракты `/api/v1/web/*` для dashboard, leaderboard и chat.

## Что делаем

1. `docs/spec/frontend-requirements.md` — wireframes, маппинг UI → домен, auth, сверка D*/Doc*
2. `docs/spec/frontend-design-system.md` — tbench dark, CSS tokens, компоненты
3. `docs/api/frontend-contract.md` — endpoint'ы, JSON, PG mapping
4. Расширить `docs/api/openapi.yaml` — tag `web`
5. Обновить `docs/spec/README.md`, `docs/integrations.md`, tasklist-frontend
6. Skill review api-design-principles → summary

## Затронутые файлы

| Файл | Действие |
|------|----------|
| `docs/spec/frontend-requirements.md` | создать |
| `docs/spec/frontend-design-system.md` | создать |
| `docs/api/frontend-contract.md` | создать |
| `docs/api/openapi.yaml` | расширить |
| `docs/spec/README.md` | дополнить |
| `docs/integrations.md` | секция web client |
| `docs/tasks/tasklist-frontend.md` | статус iter 0 |

## Согласование

- [user-scenarios.md](../../../../../../spec/user-scenarios.md), [data-requirements.md](../../../../../../spec/data-requirements.md)
- [api-contract.md](../../../../../../api/api-contract.md) v1 — без изменений bot endpoint'ов
- [data-model.md](../../../../../../data-model.md) — 9 таблиц ✅

## DoD

- 4 зоны UI + auth описаны
- frontend-contract с примерами JSON для всех web endpoint'ов
- openapi.yaml tag `web`
- api-design-principles review в summary

## Make-команды

Не требуются (документы only).
