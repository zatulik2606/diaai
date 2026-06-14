# API diaai

Контракты backend REST API. Стек: [ADR-002](../adr/adr-002-backend-stack.md).

**Главный документ:** [api-contract.md](api-contract.md) — полное описание контракта v1 (endpoint'ы, схемы, ошибки).

**Сводка и design review:** [docs/tech/api-contracts.md](../tech/api-contracts.md).

**Реализация:** [`backend/`](../../backend/) ✅; **45** тестов (`make test`: 30 backend + 15 bot).

**Runtime docs:** после `make backend-run` — [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) (Swagger), `/openapi.json`. Контракт в репо: [openapi.yaml](openapi.yaml). Сверка: `make backend-openapi-export` → diff с yaml.

| Документ | Содержание |
|----------|------------|
| [api-contract.md](api-contract.md) | **API-контракт v1** — endpoint'ы, request/response, правила |
| [conventions.md](conventions.md) | коды ошибок, auth, формат ответов, версионирование |
| [openapi.yaml](openapi.yaml) | OpenAPI 3.1 (machine-readable) |
| [scenarios/assistant-question.md](scenarios/assistant-question.md) | сценарий A — вопрос ассистенту |
| [scenarios/event-record.md](scenarios/event-record.md) | сценарий B — фиксация события |

Базовый префикс: `/api/v1`.
