# Итерация frontend 9: Summary

> **Статус:** ✅ Done

Опирается на [plan.md](plan.md) · [adr-004-text-to-sql.md](../../../../adr/adr-004-text-to-sql.md) · [text-to-sql-scenarios.md](../../../../spec/text-to-sql-scenarios.md) · [text-to-sql-architecture.md](../../../../spec/text-to-sql-architecture.md)

---

## Сделано

### Task-09: Text-to-SQL ✅

**ADR + spec**
- [adr-004-text-to-sql.md](../../../../adr/adr-004-text-to-sql.md) — dedicated endpoint, SqlGuard, out of scope assistant/bot
- [text-to-sql-scenarios.md](../../../../spec/text-to-sql-scenarios.md) — golden 3 + negatives

**Backend**
- `POST /api/v1/web/analytics/query` — LLM → SqlGuard (`sqlglot`) → read-only execute
- `AnalyticsQueryService`, `SqlGuard`, schemas, tests (10 cases)

**Web**
- `DataQueryPanel` — `/dashboard` (patient), `/leaderboard` (doctor)
- BFF `POST /api/analytics/query`
- Table + bar chart по `chart_hint`

| Компонент | Путь |
|-----------|------|
| Query API | `backend/api/v1/web/analytics_query.py` |
| SqlGuard | `backend/services/sql_guard.py` |
| UI | `web/components/analytics/data-query-panel.tsx` |

## Ценность

Ad-hoc вопросы по PG без изменения assistant; patient scoped по `user_id` / `telegram_id`.

## Отклонения от плана

| План | Факт |
|------|------|
| Assistant tool (опция) | Dedicated UI + endpoint (выбор в ADR) |
| LLM summarize rows | Template-based `_format_answer` (KISS, стабильные тесты) |

## Проверки (Self-check ✅)

| Проверка | Результат |
|----------|-----------|
| `make test` (84) | ✅ |
| `make lint` / `make web-lint` / `make web-build` | ✅ |
| Golden 3 + SqlGuard negatives | ✅ |

## User-check

```bash
make db-reset && make backend-run && make web-dev
# patient → /dashboard → «Сколько ХЕ за 7 дней?»
# doctor → /leaderboard → «Сколько ХЕ у Иван П.?»
```

## Следующий шаг

Область frontend **10/10** завершена. Backend iter 4 analytics — отдельный track.
