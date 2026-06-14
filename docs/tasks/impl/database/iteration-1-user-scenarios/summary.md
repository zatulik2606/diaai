# Итерация database 1: Summary

> **Статус:** ✅ Done

## Сделано

### Task-01: Сценарии и требования к данным ✅

- Продуктовые сценарии и матрица данных в **`docs/spec/`**
- Gap analysis относительно [`001_initial_schema.py`](../../../../../alembic/versions/001_initial_schema.py)
- Детали: [task-01 summary](tasks/task-01-user-scenarios/summary.md)

| Артефакт | Путь |
|----------|------|
| Сценарии | [user-scenarios.md](../../../../spec/user-scenarios.md) |
| Read/write, MVP scope | [data-requirements.md](../../../../spec/data-requirements.md) |
| Индекс | [spec/README.md](../../../../spec/README.md) |
| Домен + gap | [data-model.md](../../../../data-model.md) |

## Ценность

- Основа для **web** (plan iter 5): экраны пациента с диабетом и доктора без привязки к API
- Основа для **аналитики** (plan iter 4): сущности ProgressSnapshot, Recommendation
- Явный список таблиц для iter 2 (ER) и iter 5 (миграция `002_*`)

## Решения

- 11 сценариев (D1–D7, Doc1–Doc4) с read/write
- MVP data: 5 таблиц уже в PG; 4+ сущности — must add (P1/P2)
- Open questions iter 1 → черновые решения в [iteration-2 plan](../iteration-2-schema-design/plan.md)

## Отклонения от плана

- Каталог **`docs/spec/`** вместо `docs/data/` — перенос путей, содержание идентично плану

## Проблемы

Нет.

## DoD итерации

| Кто | Статус |
|-----|--------|
| Self-check (агент) | ✅ сценарии, матрица, gap-list, api-contract v1 |
| User-check | ✅ `user-scenarios.md` + `data-requirements.md`; покрытие plan iter 4–5 |

## Make-команды

Не требовались.

## Следующий шаг

[Итерация 2 — проектирование схемы](../iteration-2-schema-design/plan.md): `schema-er.md`, `schema-review.md`, `postgresql-table-design`.
