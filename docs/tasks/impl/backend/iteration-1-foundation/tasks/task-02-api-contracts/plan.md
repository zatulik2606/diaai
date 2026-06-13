# Task 02: API-контракты (2 сценария)

## Цель

REST-контракты для сценариев A (вопрос ассистенту) и B (фиксация события).

## Что делаем

1. `docs/api/scenarios/assistant-question.md` — POST `/api/v1/assistant/messages`
2. `docs/api/scenarios/event-record.md` — POST `/api/v1/events/food`, `/events/insulin`
3. `docs/api/openapi.yaml` — минимальная спецификация + health
4. Дополнить `conventions.md` — auth, X-Request-Id
5. Актуализировать `data-model.md`, `integrations.md`

## Затронутые файлы

- `docs/api/scenarios/*.md`, `docs/api/openapi.yaml`, `docs/api/README.md`
- `docs/data-model.md`, `docs/integrations.md`
- `docs/api/conventions.md`

## DoD

- Контракты покрывают `handlers.py` (A) и сущности питания/инсулина (B)
- OpenAPI согласован со scenarios

## Skills

- `.agents/skills/api-design-principles`
- `.agents/skills/fastapi-templates` (task-03+)
