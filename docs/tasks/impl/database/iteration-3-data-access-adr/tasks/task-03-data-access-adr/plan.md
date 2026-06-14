# Task 03: ADR и практика доступа к БД

Опирается на [iteration-3/plan.md](../../plan.md) · [tasklist-database.md](../../../../../tasklist-database.md)

## Цель

ADR-003 + `database-access.md`; обновить связанные docs; self-check make.

## Что делаем

1. [adr-003-data-access-layer.md](../../../../../../adr/adr-003-data-access-layer.md) — альтернативы, решение, соглашения
2. [database-access.md](../../../../../../tech/database-access.md) — карта файлов, 5 шагов, make, troubleshooting
3. Обновить `adr/README.md`, `backend-structure.md`, `backend/README.md`, ссылка в ADR-002
4. Self-check: `make backend-migrate && make backend-test`

## Затронутые файлы

| Файл | Действие |
|------|----------|
| `docs/adr/adr-003-data-access-layer.md` | создать |
| `docs/tech/database-access.md` | создать |
| `docs/adr/README.md` | ADR-003 |
| `docs/tech/backend-structure.md` | слой данных |
| `backend/README.md` | секция «Миграции и БД» |
| `docs/adr/adr-002-backend-stack.md` | ссылка ADR-003 |

## DoD

**Self-check:** ADR + guide; conventions; make green.

**User-check:** 5 шагов; backend README → guide.

## Make-команды

`make backend-migrate`, `make backend-test`
