# Task 01: Сценарии пользователя и требования к данным

Опирается на [iteration-1/plan.md](../../plan.md) · [tasklist-database.md](../../../../../tasklist-database.md)

## Цель

Описать сценарии пациента с диабетом (D1–D7) и доктора (Doc1–Doc4); вывести матрицу read/write и gap-analysis MVP schema.

## Что делаем

1. `docs/spec/user-scenarios.md` — narrative по каждому сценарию
2. `docs/spec/data-requirements.md` — read/write, MVP scope, сценарий → сущность
3. `docs/spec/README.md` — индекс
4. Обновить `docs/data-model.md` — «Требования из сценариев», gap analysis
5. Обновить `docs/vision.md` — ссылка на `docs/spec/`

## Затронутые файлы

| Файл | Действие |
|------|----------|
| `docs/spec/user-scenarios.md` | создать |
| `docs/spec/data-requirements.md` | создать |
| `docs/spec/README.md` | создать |
| `docs/data-model.md` | дополнить |
| `docs/vision.md` | ссылка |
| `docs/plan.md` | ссылка на `docs/spec/` |

## Согласование

- [idea.md](../../../../../../idea.md), [vision.md](../../../../../../vision.md)
- [api-contract.md](../../../../../../api/api-contract.md) v1 — без новых endpoint'ов
- [001_initial_schema.py](../../../../../../../alembic/versions/001_initial_schema.py)

## DoD

- 7 + 4 сценария с read/write
- MVP vs backlog разделены
- Open questions для iter 2 зафиксированы в summary

## Make-команды

Не требуются.
