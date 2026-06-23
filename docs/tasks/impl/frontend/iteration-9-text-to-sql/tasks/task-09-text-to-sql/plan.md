# Task 09: Text-to-SQL

Итерация: [iteration-9-text-to-sql](../../plan.md) · [tasklist-frontend.md](../../../../../tasklist-frontend.md)

**Статус:** ✅ Done · [summary](summary.md)

---

## A. Документация ✅

- [x] [adr-004-text-to-sql.md](../../../../../../adr/adr-004-text-to-sql.md)
- [x] [text-to-sql-scenarios.md](../../../../../../spec/text-to-sql-scenarios.md)
- [x] [text-to-sql-architecture.md](../../../../../../spec/text-to-sql-architecture.md)

---

## B. Backend ✅

- [x] `sqlglot` в `pyproject.toml`
- [x] `backend/services/sql_guard.py`
- [x] `backend/services/analytics_query_service.py`
- [x] `backend/schemas/analytics_query.py`
- [x] `backend/api/v1/web/analytics_query.py`
- [x] `prompts/analytics_sql.txt`
- [x] `backend/config.py`
- [x] `backend/tests/test_analytics_query.py`

---

## C. Web ✅

- [x] `web/components/analytics/data-query-panel.tsx`
- [x] `web/app/api/analytics/query/route.ts`
- [x] `web/lib/backend-client.ts` — `queryAnalytics()`
- [x] `/dashboard` + `/leaderboard`

---

## D. Контракты и закрытие ✅

- [x] openapi, api-contracts, frontend-contract, integrations
- [x] tasklist + summary iter 9

---

## Проверки

```bash
make test && make lint && make web-lint && make web-build  # ✅ 84 tests
```
