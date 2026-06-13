# Task 08: Summary — Качество и инженерные практики

## Сделано

- **Logging audit** — middleware логирует только `request_id`, `method`, `path`, `status`, `duration_ms`; exception handlers при 5xx — `request_id` + `error_code` / class name без body и PII.
- **`GET /health`** — additive field `version` из `app.version` (`"1.0.0"`).
- **`backend/README.md`** — секции Logging и Quality; curl health; `make test` (36).
- **Корневой `README.md`** — блок Quality (`make lint`, `make test`).
- **`docs/tech/api-contracts.md`** — tech debt 422 deferred post-MVP; logging ✅; contract tests 36.
- **`docs/api/conventions.md`** — 422 deferred post-MVP (task-08).

## Код

| Файл | Изменение |
|------|-----------|
| `backend/main.py` | health + version; log on AppError ≥500 и unhandled |
| `backend/tests/test_health.py`, `test_auth.py` | assert `version` |
| `docs/api/openapi.yaml` | schema `/health` + `version` |

## Отклонения от плана

- Unified 422 → ErrorBody не делали (explicit defer в docs).
- `/health/detailed` + DB ping — вне scope.

## Проверки

| Критерий | Статус |
|----------|--------|
| `make lint` | ✅ |
| `make test` (36) | ✅ |
| `curl /health` → status + version | ✅ |
| Логи без Bearer/body/text | ✅ (middleware audit) |

## Следующий шаг

Backend tasklist 01–08 ✅ → [Итерация 4 — Аналитика](../../../../../../plan.md#итерация-4--аналитика-и-динамика-состояния).
