# API diaai

Контракты backend REST API. Стек: [ADR-002](../adr/adr-002-backend-stack.md).

**Сводка:** [docs/tech/api-contracts.md](../tech/api-contracts.md) — endpoint'ы, cross-cutting, design review, contract tests.

**Реализация:** [`backend/`](../../backend/) ✅ (task-05); **21** contract/impl test (`make backend-test`).

**Runtime docs:** после `make backend-run` — [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) (Swagger), `/openapi.json`. Контракт в репо: [openapi.yaml](openapi.yaml). Сверка: `make backend-openapi-export` → diff с yaml.

| Документ | Содержание |
|----------|------------|
| [conventions.md](conventions.md) | коды ошибок, auth, формат ответов, версионирование |
| [openapi.yaml](openapi.yaml) | OpenAPI 3.1 (machine-readable) |
| [scenarios/assistant-question.md](scenarios/assistant-question.md) | сценарий A — вопрос ассистенту |
| [scenarios/event-record.md](scenarios/event-record.md) | сценарий B — фиксация события |

Базовый префикс: `/api/v1`.
