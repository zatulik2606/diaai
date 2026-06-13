# API diaai

Контракты backend REST API. Стек: [ADR-002](../adr/adr-002-backend-stack.md).

**Сводка:** [docs/tech/api-contracts.md](../tech/api-contracts.md) — endpoint'ы, cross-cutting, design review, contract tests.

**Реализация:** каркас [`backend/`](../../backend/) (task-03 ✅); 17 contract tests (task-04 ✅); impl — task-05.

| Документ | Содержание |
|----------|------------|
| [conventions.md](conventions.md) | коды ошибок, auth, формат ответов, версионирование |
| [openapi.yaml](openapi.yaml) | OpenAPI 3.1 (machine-readable) |
| [scenarios/assistant-question.md](scenarios/assistant-question.md) | сценарий A — вопрос ассистенту |
| [scenarios/event-record.md](scenarios/event-record.md) | сценарий B — фиксация события |

Базовый префикс: `/api/v1`.
