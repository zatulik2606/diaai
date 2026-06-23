# Итерация frontend 9: Text-to-SQL

Опирается на [tasklist-frontend.md](../../../tasklist-frontend.md) · [impl/frontend/plan.md](../plan.md) · [adr-004-text-to-sql.md](../../../../adr/adr-004-text-to-sql.md) · [text-to-sql-scenarios.md](../../../../spec/text-to-sql-scenarios.md) · [text-to-sql-architecture.md](../../../../spec/text-to-sql-architecture.md)

Skills: [shadcn](../../../../.agents/skills/shadcn/SKILL.md) · [vercel-react-best-practices](../../../../.agents/skills/vercel-react-best-practices/SKILL.md)

**Статус:** ✅ Done · [summary](summary.md)

---

## Цель

Ad-hoc вопросы по данным PostgreSQL в web: dedicated UI «Вопрос по данным» + guarded Text-to-SQL на backend.

## Ценность

- Ответы из реальных данных (ХЕ, события, прогресс), не галлюцинации LLM
- Patient видит только свои данные; doctor — когорту
- Завершение области frontend (10/10)

---

## Архитектура

→ [ADR-004](../../../../adr/adr-004-text-to-sql.md): LLM → SQL → SqlGuard → read-only PG → `{ answer, columns, rows, chart_hint }`

**Не в scope:** assistant tool, bot, backend iter 4 REST `/analytics/*`.

---

## Gap analysis

| Блок | Было | Целевое iter 9 |
|------|------|----------------|
| NL → data | только fixed dashboard API | `POST /web/analytics/query` |
| Web UI | KPI/charts fixed | + DataQueryPanel |
| Guardrails | — | SqlGuard + role scope |
| Docs | out of scope | ADR-004, scenarios |

---

## Задачи

| Task | Описание | Документ |
|------|----------|----------|
| 09 | Text-to-SQL backend + web UI | [task-09 plan](tasks/task-09-text-to-sql/plan.md) |

---

## Definition of Done

**Self-check:** ADR принят; 3 golden + negatives; `make test`; `make web-build`.

**User-check:** doctor «ХЕ за неделю у [patient]»; patient «ХЕ за 7 дней» — число из PG.

## Out of scope

Write SQL, bot, assistant tools, streaming.
