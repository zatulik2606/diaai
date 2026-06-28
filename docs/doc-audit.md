# Аудит документации diaai

**Дата:** 2026-06-23 · **Контекст:** post devops iter 0–1 (local stack + GHCR) · `make test` → **84** · **P0–P2 выполнены** (см. § «Выполнение P0–P2»)

Цель аудита — согласовать docs с реальным состоянием репозитория: статусы этапов, счётчики тестов, карта API, onboarding/smoke, отсутствие «слепых зон» между product-plan и tasklist'ами областей.

---

## Резюме

| Метрика | Было | Стало |
|---------|------|-------|
| Product plan iter 5 | 📋 Planned | ✅ Done (+ post-MVP out-of-scope) |
| Product plan iter 4 vs web | линейная зависимость E4→E5 | параллельность задокументирована |
| Счётчик тестов в top-level docs | 45 / 52 / 21 | **84** в README, backend-structure, tasklists |
| OpenAPI patient dashboard | отсутствовал | 5 routes ✅ |
| Onboarding / smoke | разрозненно | `onboarding.md` + **`smoke-test.md`** ✅ |
| `tasklist-web.md` | дублировал frontend | deprecated → redirect ✅ |
| Spec-слой (scenarios, vision) | «📋 iter 5» | актуальные каналы + post-MVP ✅ |
| Backend iter 4 analytics | «таблиц нет» в plan | контракты task 09 ✅ |

**Остаётся (P3):** исторические summary в `impl/**` (снимки на момент iter); ADR/backend-area plan — counts в закрытых task-блоках; `api-contract.md` — отметка impl analytics после task 10. **DevOps iter 0–1 закрыт** (9/9 ✅) — CD/cloud deploy post-MVP.

---

## Метод

### Runnability checklist (one-session)

Проверка «можно ли поднять проект по docs за одну сессию»:

| # | Шаг | Источник | Статус |
|---|-----|----------|--------|
| 1 | Prerequisites (Python, uv, Docker, Node/pnpm) | [onboarding.md](onboarding.md) | ✅ |
| 2 | `.env` + токены | [how-to-get-tokens.md](how-to-get-tokens.md) | ✅ |
| 3 | DB + backend | [README.md](../README.md), [backend/README.md](../backend/README.md) | ✅ |
| 4 | Web | [web/README.md](../web/README.md) | ✅ |
| 5 | Bot | [src/diaai/README.md](../src/diaai/README.md) | ✅ |
| 6 | Полный smoke (~15 мин) | **[smoke-test.md](smoke-test.md)** | ✅ |
| 7 | Docker stack (build) | `make stack-up && make stack-health` · [docker-compose-local.md](devops/docker-compose-local.md) | ✅ |
| 8 | Docker stack (GHCR) | `make stack-pull-registry && make stack-up-registry && make stack-health` · [ghcr-stack.md](devops/ghcr-stack.md) | ✅ |
| 9 | Quality gate | `make test` → 84 | ✅ |

### Реестр документов (верхний уровень)

| Документ | Назначение | Актуальность |
|----------|------------|--------------|
| [plan.md](plan.md) | product roadmap 1–5 + post-MVP | ✅ обновлён |
| [architecture.md](architecture.md) | компоненты, API, mermaid | ✅ |
| [vision.md](vision.md) | продуктовое видение, стек | ✅ обновлён |
| [onboarding.md](onboarding.md) | пошаговый гайд (6 разделов) | ✅ обновлён |
| [smoke-test.md](smoke-test.md) | one-session чеклист | ✅ |
| [api/api-contract.md](api/api-contract.md) | REST bot + web + analytics contract | ✅ |
| [api/openapi.yaml](api/openapi.yaml) | machine-readable | ✅ patient + analytics paths |
| [api/frontend-contract.md](api/frontend-contract.md) | web DTO | ✅ |
| [tech/api-contracts.md](tech/api-contracts.md) | design review карта | ✅ |
| [spec/user-scenarios.md](spec/user-scenarios.md) | D*/Doc* × каналы | ✅ |
| [spec/data-requirements.md](spec/data-requirements.md) | read/write matrix | ✅ |
| [spec/README.md](spec/README.md) | индекс spec | ✅ voice + text-to-sql |
| [tasks/tasklist-frontend.md](tasks/tasklist-frontend.md) | web 10/10 | ✅ |
| [tasks/tasklist-backend.md](tasks/tasklist-backend.md) | backend 9/12 | ✅ |
| [tasks/tasklist-bot.md](tasks/tasklist-bot.md) | bot + voice | ✅ |
| [tasks/tasklist-database.md](tasks/tasklist-database.md) | database 5/5 ✅ | ✅ |
| [tasks/tasklist-devops.md](tasks/tasklist-devops.md) | devops 9/9 ✅ (iter 0 stack · iter 1 GHCR) | ✅ |
| [devops/docker-compose-local.md](devops/docker-compose-local.md) | local Docker stack (build profile) | ✅ |
| [devops/ghcr-stack.md](devops/ghcr-stack.md) | stack из GHCR (registry profile) | ✅ |
| [devops/ci/README.md](../devops/ci/README.md) | GHA → GHCR, tags, pull | ✅ |
| [tasks/tasklist-web.md](tasks/tasklist-web.md) | — | ✅ deprecated → [frontend](tasks/tasklist-frontend.md) |

---

## Выявленные расхождения (до правок)

### Критичные (вводят в заблуждение)

1. **plan.md iter 5** — `📋 Planned` при закрытом frontend 0–9; цель «консultации» без UI.
2. **plan.md mermaid** — E4→E5 скрывал, что web сделан до analytics REST.
3. **Счётчики тестов** — 21 / 45 / 52 vs фактические 84.
4. **OpenAPI** — нет `/api/v1/web/patient/dashboard/*` при реализованном коде.
5. **tasklist-frontend** — «Backend iter 4 ✅» (web API ≠ analytics REST iter 4).
6. **user-scenarios** — D1/D2/D7 и Doc* помечены «📋 iter 5».

### Средние (слепые зоны)

7. **Database** — 5/5 ✅, но не отражена в product overview.
8. **Bot voice, Text-to-SQL** — закрыты в tasklist'ах, не в product plan.
9. **vision.md** — «стек web на этапе», deploy «на этапе», `bot/` vs `src/diaai/`.
10. **Нет smoke-test.md** — onboarding без one-session path.
11. **Нет src/diaai/README.md** — bot dev guide только в conventions.

### Низкие (исторические артефакты)

12. Self-check в `impl/database/**`, `impl/backend/**` — «52 passed», «21 тест».
13. `tasklist-database.md` — ссылки на deprecated `tasklist-web.md`.
14. `adr-002`, `impl/backend/plan.md` — старые counts.
15. `.cursor/rules/workflow.mdc` — путь `bot/` (исправлено → `src/diaai/`).

---

## Приоритезированный план

Легенда: ✅ выполнено · 🚧 в работе · 📋 запланировано

### P0 — блокеры onboarding и product truth

| # | Задача | Файлы | Статус |
|---|--------|-------|--------|
| P0-1 | Iter 5 → Done; iter 4 vs web — параллельность | [plan.md](plan.md) | ✅ |
| P0-2 | README: web Done, 84 tests, smoke/onboarding links | [README.md](../README.md) | ✅ |
| P0-3 | Deprecated tasklist-web → frontend | [tasks/tasklist-web.md](tasks/tasklist-web.md) | ✅ |
| P0-4 | Bot dev guide | [src/diaai/README.md](../src/diaai/README.md) | ✅ |

### P1 — runnability и синхронизация counts

| # | Задача | Файлы | Статус |
|---|--------|-------|--------|
| P1-1 | One-session smoke чеклист | [smoke-test.md](smoke-test.md) | ✅ |
| P1-2 | Счётчики 84 в top-level docs | README, [api/README.md](api/README.md), [tech/backend-structure.md](tech/backend-structure.md), tasklist-backend, tasklist-database (quick start) | ✅ |
| P1-3 | Onboarding: prerequisites + smoke path | [onboarding.md](onboarding.md) | ✅ |

### P2 — контракты и spec-слой

| # | Задача | Файлы | Статус |
|---|--------|-------|--------|
| P2-1 | OpenAPI patient dashboard (5 routes) | [api/openapi.yaml](api/openapi.yaml) | ✅ |
| P2-2 | api-contracts: patient routes | [tech/api-contracts.md](tech/api-contracts.md) | ✅ |
| P2-3 | backend/README: STT, ANALYTICS env, curl | [backend/README.md](../backend/README.md) | ✅ |
| P2-4 | web/README: voice, analytics BFF, web-build | [web/README.md](../web/README.md) | ✅ |
| P2-5 | spec/README: voice, text-to-sql | [spec/README.md](spec/README.md) | ✅ |
| P2-6 | user-scenarios: каналы × статусы | [spec/user-scenarios.md](spec/user-scenarios.md) | ✅ |
| P2-7 | vision.md: web stack, deploy, repo layout | [vision.md](vision.md) | ✅ |
| P2-8 | data-requirements: 002 done, post-MVP | [spec/data-requirements.md](spec/data-requirements.md) | ✅ |
| P2-9 | tasklist-frontend: deps backend iter 4 | [tasks/tasklist-frontend.md](tasks/tasklist-frontend.md) | ✅ |
| P2-10 | workflow.mdc: `src/diaai/` | [.cursor/rules/workflow.mdc](../.cursor/rules/workflow.mdc) | ✅ |

### Выполнение P0–P2 (2026-06-07, финализация)

| # | Задача | Файлы | Статус |
|---|--------|-------|--------|
| P0–P2 | Все пункты таблиц выше | см. § P0–P2 | ✅ |
| NEW | Архитектурный документ | [architecture.md](architecture.md) | ✅ |
| NEW | README: prerequisites, env, make, architecture link | [README.md](../README.md) | ✅ |
| NEW | Onboarding: 6 разделов + smoke/API checks | [onboarding.md](onboarding.md) | ✅ |
| NEW | api/README: analytics scenarios | [api/README.md](api/README.md) | ✅ |

### P3 — backlog (не блокирует; по желанию)

| # | Задача | Файлы | Статус |
|---|--------|-------|--------|
| P3-1 | tasklist-database: tasklist-web → frontend | [tasks/tasklist-database.md](tasks/tasklist-database.md) | ✅ |
| P3-2 | Исторические summary: footnote «снимок на дату iter» или не трогать | `docs/tasks/impl/**/summary.md` | 📋 |
| P3-3 | ADR-002, impl/backend/plan.md — counts 84 | [adr/adr-002-backend-stack.md](adr/adr-002-backend-stack.md), [tasks/impl/backend/plan.md](tasks/impl/backend/plan.md) | ✅ |
| P3-4 | tasklist-backend closed tasks — «45 tests» в тексте задач 07–08 | [tasks/tasklist-backend.md](tasks/tasklist-backend.md) | 📋 |
| P3-5 | api-contract.md MVP table — строка analytics impl после task 10–11 | [api/api-contract.md](api/api-contract.md) | ✅ |
| P3-6 | backend/README analytics curl после impl iter 4 | [backend/README.md](../backend/README.md) | ✅ |
| P3-7 | spec/user-scenarios — link doc-audit | [spec/user-scenarios.md](spec/user-scenarios.md) | ✅ |

---

## Слепые зоны: статус после аудита

| Зона | Было | Сейчас |
|------|------|--------|
| Product plan vs 4 области | только bot/backend/web | + database, post-MVP, footnotes |
| Web до analytics REST | не описано | plan.md + user-scenarios |
| Consultations D5/D6 | «iter 5» | post-MVP явно |
| `/analytics/*` vs `/web/*` | смешение | разделено; contract + **impl ✅** (iter 4 tasks 10–12) |
| Prompt path analytics_sql | runtime bug | fix в коде: `prompts/analytics_sql.txt` ✅ |
| README без architecture.md | ссылка только на vision | [architecture.md](architecture.md) ✅ |

---

## Связь с backend iter 4 (post-audit)

Документация analytics REST вынесена из «вне scope» в контракт:

| Task | Docs | Статус |
|------|------|--------|
| 09 Контракты | scenarios, api-contract, openapi, api-contracts, data-model cross-ref | ✅ |
| 10 Progress impl | backend/README curl, api-contract «impl ✅» | ✅ |
| 11 Signals/recs | scenarios уже описаны | ✅ |
| 12 Close iter 4 | iteration-4 summary, tasklist-backend, plan iter 4 → Done | ✅ |

---

## Проверка 2026-06-23 (devops iter 0–1)

| Проверка | Результат |
|----------|-----------|
| `make stack-up && make stack-health` | ✅ build profile |
| `make stack-pull-registry && make stack-up-registry && make stack-health` | ✅ GHCR |
| `make test` | **84** |

## Проверка 2026-06-07

| Проверка | Результат |
|----------|-----------|
| `make test` | **84** |
| `/api/v1/analytics/*` в коде | ❌ только OpenAPI contract (task 10–11) |
| `/api/v1/web/analytics/query` | ✅ |
| Миграции Alembic | `001`–`003` |
| tasklist-database → frontend | ✅ |
| smoke-test Text-to-SQL | doctor `/leaderboard` ✅ |

Исторические summary в `impl/**` с «45»/«52» — снимки iter; не переписывать без необходимости.

---

## Правило поддержки

После каждой итерации, меняющей scope или тесты:

1. Обновить **один** canonical count: `make test` в [README.md](../README.md) + [tasklist-backend.md](tasks/tasklist-backend.md).
2. Product status — только [plan.md](plan.md); детали — tasklist области.
3. Новый endpoint → [api-contract.md](api/api-contract.md) + [openapi.yaml](api/openapi.yaml) + при необходимости [tech/api-contracts.md](tech/api-contracts.md).
4. Новая фича для onboarding → пункт в [smoke-test.md](smoke-test.md).
5. Исторические `impl/**/summary.md` **не переписывать** без необходимости; актуальное состояние — в tasklist + area summary.
6. После правок API/BFF — subagent **[`.cursor/agents/docs-updater.md`](../.cursor/agents/docs-updater.md)** (hook: `.cursor/hooks.json`).

---

## Связанные документы

- [architecture.md](architecture.md) — компоненты и API
- [plan.md](plan.md) — product roadmap
- [onboarding.md](onboarding.md) · [smoke-test.md](smoke-test.md) — вход разработчика
- [tasks/tasklist-backend.md](tasks/tasklist-backend.md) — backend iter 4 ✅ (09–12)
- [tasks/impl/backend/iteration-4-analytics/plan.md](tasks/impl/backend/iteration-4-analytics/plan.md)
