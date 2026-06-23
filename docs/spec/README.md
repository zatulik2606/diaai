# Spec — продуктовые сценарии и требования к данным

Слой документации области **database** ([tasklist-database.md](../tasks/tasklist-database.md)) и **frontend** ([tasklist-frontend.md](../tasks/tasklist-frontend.md)).

| Документ | Содержание |
|----------|------------|
| [user-scenarios.md](user-scenarios.md) | сценарии пациента с диабетом (D1–D7) и доктора (Doc1–Doc4) |
| [data-requirements.md](data-requirements.md) | read/write, MVP scope, сценарий → сущность |
| [schema-er.md](schema-er.md) | ER + физическая схема *(iter 2 ✅)* |
| [schema-review.md](schema-review.md) | PG design review *(iter 2 ✅)* |
| [frontend-requirements.md](frontend-requirements.md) | 4 зоны UI, wireframes, auth *(frontend iter 0 ✅)* |
| [frontend-design-system.md](frontend-design-system.md) | tbench dark theme, tokens, компоненты *(frontend iter 0 ✅)* |
| [voice-limitations.md](voice-limitations.md) | голосовой ввод (iter 8): STT, ограничения |
| [text-to-sql-scenarios.md](text-to-sql-scenarios.md) | NL-запросы доктора (iter 9): сценарии |
| [text-to-sql-architecture.md](text-to-sql-architecture.md) | Text-to-SQL: LLM → SqlGuard → PG |

Архитектура системы: [architecture.md](../architecture.md). REST v1 bot — [api-contract.md](../api/api-contract.md). Web API — [frontend-contract.md](../api/frontend-contract.md).

**Статус:** database iter 1–2 ✅; frontend iter 0–9 ✅ — UI spec, web API, voice, analytics NL.
