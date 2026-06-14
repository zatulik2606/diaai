# Итерация database 3: Summary

> **Статус:** ✅ Done

План: [plan.md](plan.md)

## Сделано

### Task-03: ADR и практика доступа к БД ✅

- ADR-003: SQLAlchemy 2 async + Alembic + repositories — [adr-003-data-access-layer.md](../../../../adr/adr-003-data-access-layer.md)
- Практический guide: 5 шагов «новая таблица», make-команды — [database-access.md](../../../../tech/database-access.md)
- Обновлены: `adr/README.md`, `backend-structure.md`, `backend/README.md`, ссылка в ADR-002
- План итерации сохранён в [plan.md](plan.md)
- Детали: [task-03 summary](tasks/task-03-data-access-adr/summary.md)

| Артефакт | Путь |
|----------|------|
| ADR | [adr-003-data-access-layer.md](../../../../adr/adr-003-data-access-layer.md) |
| Guide | [database-access.md](../../../../tech/database-access.md) |
| План итерации | [plan.md](plan.md) |
| Слой данных в backend-structure | [backend-structure.md](../../../../tech/backend-structure.md) |

## Ценность

- Формализован паттерн **handler → service → repository → `get_db`**
- Единый ответ «почему Alembic + SQLAlchemy async» (дополнение к ADR-001/002)
- Onboarding для миграции `002` (database iter 5) и analytics API (backend iter 4)

## Решения

| Тема | Решение |
|------|---------|
| ORM + миграции | SQLAlchemy 2 async + Alembic (отклонены raw SQL, sync ORM, Django/Tortoise) |
| Driver | `asyncpg`, URL `postgresql+asyncpg://` |
| Транзакция | граница HTTP-запроса: `get_db()` commit / rollback |
| Слои | бизнес-логика в service; repository — только queries; без SQL в handlers |
| Модели | один файл на таблицу в `backend/models/` |
| Generic BaseRepository | не вводим на MVP |
| Тесты backend | sqlite in-memory + override `get_db`; PG — интеграция вручную |
| `make db-*` | defer → database iter 4 |

## Отклонения от плана

Нет.

## Проблемы

Нет.

## DoD итерации

| Кто | Статус | Критерии |
|-----|--------|----------|
| Self-check (агент) | ✅ | ADR принят; guide с copy-paste командами; conventions OK; migrate + test green |
| User-check | ✅ | ADR — «почему»; guide — 5 шагов; backend README → guide |

## Make-команды

| Команда | Результат |
|---------|-----------|
| `make backend-migrate` | ✅ green (PG :5433) |
| `make backend-test` | ✅ 30 passed |

## Следующий шаг

[Итерация 4 — инфраструктура, seed, команды](../iteration-4-db-infra-seed/plan.md): `make db-*`, seed, inspect.
