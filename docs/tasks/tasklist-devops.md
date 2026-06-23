# DevOps Tasklist

Опирается на [plan.md](../plan.md) · [vision.md](../vision.md) · [architecture.md](../architecture.md) · [onboarding.md](../onboarding.md) · [integrations.md](../integrations.md)

## Обзор

Рабочий план области **DevOps**: подготовка к production deploy без полноценного CI/CD на первом этапе.

| Итерация | Фокус |
|----------|-------|
| **0** | Локальный полный стек — один корневой `docker-compose.yml`, Dockerfile'ы, `make stack-*` |
| **1** | Сборка и публикация образов в GHCR — тот же compose, режим `image:` |

Deploy в облако, secrets management и полный pipeline — post-MVP (после iter 0–1).

**Текущее состояние:** полный stack в [`docker-compose.yml`](../../docker-compose.yml) — `postgres` (:5433) · `backend` (:8000) · `web` (:3000) · `bot` (profile). Host dev: `make db-*`, `backend-run`, `web-dev`. Guide: [docker-compose-local.md](../devops/docker-compose-local.md).

**Прогресс:** **9 / 9** задач · **iter 0 ✅** · **iter 1 ✅**

> **Scope:** containerization + локальный orchestration + build/publish образов. **Не в scope** iter 0–1: Kubernetes, Terraform, staging/prod окружения, автодеплой, мониторинг, секреты в GitHub Environments.

## Правило: один корневой compose

**Единственный файл orchestration полного стека — [`docker-compose.yml`](../../docker-compose.yml) в корне репозитория.**

| Режим | Как включается | Файлы |
|-------|----------------|-------|
| Локальная сборка (iter 0) | `build:` в сервисах backend, web, bot | только корневой `docker-compose.yml` |
| Образы из GHCR (iter 1) | env (`IMAGE_TAG`) или compose **profiles** в том же файле | тот же `docker-compose.yml` |
| Только PostgreSQL (dev) | `docker compose up -d postgres` или `make db-up` | тот же `docker-compose.yml`, подмножество сервисов |

**Не создавать:** `docker-compose.db.yml`, `docker-compose.full.yml`, `docker-compose.registry.yml` и другие параллельные compose-файлы полного стека. Допустим локальный `compose.override.yml` (gitignore) для машин-специфичных правок — не часть репозитория.

Текущий compose — **полный stack** (iter 0 ✅). Iter 1 добавил режим `image:` через env/profiles **в этом же файле** (iter 1 ✅).

## Итерации

Сводный план: [impl/devops/plan.md](impl/devops/plan.md)

| # | Название | Задачи | Статус | Документы |
|---|----------|--------|--------|-----------|
| 0 | Локальный полный стек | 01–06 | ✅ Done | [plan](impl/devops/iteration-0-local-stack/plan.md) · [summary](impl/devops/iteration-0-local-stack/summary.md) |
| 1 | Сборка образов и публикация в GHCR | 07–09 | ✅ Done | [plan](impl/devops/iteration-1-registry-ci/plan.md) · [summary](impl/devops/iteration-1-registry-ci/summary.md) |

## Связь с plan.md и architecture

| Источник | Связь | Зависимости |
|----------|-------|-------------|
| [plan.md — Post-MVP](../plan.md#post-mvp-не-в-таблице-этапов) | Production deploy (bot + backend + web) | backend ✅ · frontend ✅ · database ✅ |
| [architecture.md](../architecture.md) | compose diagram, `devops/`, GHCR | ✅ iter 0–1 |
| [onboarding.md](../onboarding.md) | Docker stack «одной командой» (build + GHCR) | ✅ iter 0–1 |
| [tasklist-backend.md](tasklist-backend.md) task-06 | `docker-compose.yml` только PG | iter 0 **расширяет** тот же корневой compose |
| [tasklist-database.md](tasklist-database.md) | `make db-*`, миграции, seed | compose: migrate/seed при старте backend или init hook |

## Легенда статусов

- 📋 Planned — запланирован
- 🚧 In Progress / Next — в работе или следующий
- ✅ Done — завершён

## Skills

Подбор через `/find-skills`, если skill не найден в репозитории.

| Skill | Когда | Фокус |
|-------|-------|-------|
| `docker-expert` | **iter 0**, task 05 | multi-stage builds, .dockerignore, healthchecks, compose networking, secrets |
| `github-actions-templates` | **iter 1**, task 07 | build matrix, GHCR login, tags, cache |
| `sharp-edges` | iter 0–1 | env/secrets в compose и CI, не коммитить `.env` |

## Целевая структура `devops/`

Обоснование (task 01): единая база для Docker/CI-артефактов без размазывания по `backend/`, `web/`, `src/`; **orchestration — только корневой `docker-compose.yml`** (см. § «Правило: один корневой compose»).

```
devops/
├── README.md                 # карта артефактов, naming, теги образов
├── docker/
│   ├── backend/
│   │   ├── Dockerfile
│   │   └── .dockerignore
│   ├── bot/
│   │   ├── Dockerfile
│   │   └── .dockerignore
│   └── web/
│       ├── Dockerfile
│       └── .dockerignore
├── compose/
│   └── .env.compose.example  # шаблон env для stack (без секретов)
└── ci/
    └── README.md             # GHCR tags, workflow, локальный pull
```

Корень репозитория:

- **`docker-compose.yml`** — полный stack (iter 0 ✅); iter 1 добавил режим `image:` **в этом же файле** (iter 1 ✅)
- `.github/workflows/` — workflow iter 1 (см. `devops/ci/README.md`)

## Make-команды (iter 0–1 ✅)

| Команда | Действие |
|---------|----------|
| `make stack-up` | полный stack (build + up) |
| `make stack-up-bot` | stack + profile `bot` |
| `make stack-up-registry` | stack из GHCR (без build) |
| `make stack-pull-registry` | pull образов из GHCR |
| `make stack-up-registry-bot` | registry + bot |
| `make stack-down` | остановить stack |
| `make stack-ps` | статус контейнеров |
| `make stack-logs` | логи (`follow`) |
| `make stack-logs-tail` | последние 100 строк |
| `make stack-logs SVC=backend` | логи одного сервиса |
| `make stack-health` | pg + `/health` + web :3000 |
| `make stack-init` | `db-reset` + `stack-up` |
| `make db-up` / `make db-reset` | только postgres / migrate+seed с хоста |

## Список задач

| Задача | Описание | Статус | Документы |
|--------|----------|--------|-----------|
| 01 | Структура `devops/` и обоснование | ✅ Done | [план](impl/devops/iteration-0-local-stack/tasks/task-01-devops-layout/plan.md) · [summary](impl/devops/iteration-0-local-stack/tasks/task-01-devops-layout/summary.md) |
| 02 | Dockerfile + .dockerignore (backend, bot, web) | ✅ Done | [план](impl/devops/iteration-0-local-stack/tasks/task-02-dockerfiles/plan.md) · [summary](impl/devops/iteration-0-local-stack/tasks/task-02-dockerfiles/summary.md) |
| 03 | Корневой `docker-compose.yml` — полный стек | ✅ Done | [план](impl/devops/iteration-0-local-stack/tasks/task-03-compose-full-stack/plan.md) · [summary](impl/devops/iteration-0-local-stack/tasks/task-03-compose-full-stack/summary.md) |
| 04 | Makefile: stack-up/down/ps/logs/health | ✅ Done | [план](impl/devops/iteration-0-local-stack/tasks/task-04-makefile-stack/plan.md) · [summary](impl/devops/iteration-0-local-stack/tasks/task-04-makefile-stack/summary.md) |
| 05 | Ревью Docker-конфигурации (`docker-expert`) | ✅ Done | [план](impl/devops/iteration-0-local-stack/tasks/task-05-docker-review/plan.md) · [summary](impl/devops/iteration-0-local-stack/tasks/task-05-docker-review/summary.md) |
| 06 | Инструкция compose + обновление docs | ✅ Done | [план](impl/devops/iteration-0-local-stack/tasks/task-06-docs-compose/plan.md) · [summary](impl/devops/iteration-0-local-stack/tasks/task-06-docs-compose/summary.md) |
| 07 | GitHub Actions → GHCR | ✅ Done | [план](impl/devops/iteration-1-registry-ci/tasks/task-07-gha-ghcr/plan.md) · [summary](impl/devops/iteration-1-registry-ci/tasks/task-07-gha-ghcr/summary.md) |
| 08 | Compose на образах registry + ревью | ✅ Done | [план](impl/devops/iteration-1-registry-ci/tasks/task-08-compose-registry/plan.md) · [summary](impl/devops/iteration-1-registry-ci/tasks/task-08-compose-registry/summary.md) |
| 09 | Локальная проверка stack из GHCR + docs | ✅ Done | [план](impl/devops/iteration-1-registry-ci/tasks/task-09-registry-verify/plan.md) · [summary](impl/devops/iteration-1-registry-ci/tasks/task-09-registry-verify/summary.md) |

Задачи выполняются **последовательно** (01 → 09). Итерация 1 — после закрытия iter 0.

---

## Итерация 0 — Локальный полный стек ✅

**Ценность:** один сценарий «поднять всё» для onboarding, smoke и демо без четырёх терминалов.

**Критерии итерации:** ✅
- `make stack-up` → postgres + backend + web (+ bot: `make stack-up-bot`)
- `make stack-health` green; login `@ivan_p` → dashboard
- `make db-reset` / `make db-up` — без full stack
- [docker-compose-local.md](../devops/docker-compose-local.md); docker-expert review ✅

→ [iteration-0-local-stack/plan.md](impl/devops/iteration-0-local-stack/plan.md) · [summary](impl/devops/iteration-0-local-stack/summary.md)

---

## Задача 01: Структура `devops/` и обоснование ✅

### Цель

Зафиксировать layout DevOps-артефактов и правила именования до написания Dockerfile'ов.

### Состав работ

- [x] Создать `devops/` по целевой схеме (см. выше); `devops/README.md` — карта, связь с корневым compose
- [x] Обоснование: почему не `backend/Dockerfile` в корне сервиса (monorepo build context, uv/pnpm, shared `prompts/`, `alembic/`)
- [x] `devops/compose/.env.compose.example` — переменные stack без секретов (ссылка на `.env.example`)
- [x] При необходимости — короткий ADR `docs/adr/adr-00N-devops-layout.md` или раздел в `devops/README.md`

### Артефакты

- `devops/README.md`, `devops/compose/.env.compose.example`
- каталоги `devops/docker/{backend,bot,web}/`

### Definition of Done

**Агент:** структура создана; README объясняет пути Dockerfile → compose build; второй compose-файл полного стека не появился.

**Пользователь:** по `devops/README.md` понятно, где лежат Docker/CI артефакты и как они связаны с корневым `docker-compose.yml`.

### Документы

- 📋 [План](impl/devops/iteration-0-local-stack/tasks/task-01-devops-layout/plan.md)
- 📝 [Summary](impl/devops/iteration-0-local-stack/tasks/task-01-devops-layout/summary.md)

---

## Задача 02: Dockerfile + .dockerignore ✅

### Цель

Образы для backend, bot и web — reproducible build из monorepo.

### Состав работ

- [x] **backend:** Python 3.12, `uv sync`, Alembic; context — корень repo; entrypoint migrate
- [x] **bot:** `src/diaai/`, uv; env `BACKEND_URL`, `TELEGRAM_BOT_TOKEN`
- [x] **web:** Node 24 / pnpm 11.6, multi-stage; production `next start`
- [x] `.dockerignore` — root + `web/`; reference lists в `devops/docker/*`
- [x] Локальная проверка: `docker build` для трёх образов

### Артефакты

- `devops/docker/*/Dockerfile`, `devops/docker/*/.dockerignore`

### Definition of Done

**Агент:** три образа собираются без ошибок; размер и слои разумны (multi-stage где нужно).

**Пользователь:** `docker images` показывает три локальных тега; README в `devops/docker/` или `devops/README.md` — команды build.

### Документы

- 📋 [План](impl/devops/iteration-0-local-stack/tasks/task-02-dockerfiles/plan.md)
- 📝 [Summary](impl/devops/iteration-0-local-stack/tasks/task-02-dockerfiles/summary.md)

---

## Задача 03: Корневой `docker-compose.yml` — полный стек ✅

### Цель

Расширить **корневой** [`docker-compose.yml`](../../docker-compose.yml) (сейчас postgres :5433) сервисами backend, web, bot. Отдельный compose-файл не создавать.

### Состав работ

- [x] Сохранить сервис `postgres` (volume, healthcheck, порт **5433**)
- [x] `backend`: build, `DATABASE_URL` internal, depends_on, healthcheck, :8000
- [x] `web`: build, `BACKEND_URL`, depends_on backend, healthcheck, :3000
- [x] `bot`: profile `bot`, depends_on backend
- [x] Env: `env_file: .env`; prompts baked in image
- [x] Migrate в entrypoint; seed — `make db-reset` / `stack-init`

### Артефакты

- [`docker-compose.yml`](../../docker-compose.yml) — полный стек
- `devops/compose/.env.compose.example` — дополнен

### Definition of Done

**Агент:** `docker compose config` валиден; postgres+backend+web поднимаются; backend `/health` 200; web открывается.

**Пользователь:** скопировать `.env`, `make stack-up` — dashboard на :3000 без ручного `backend-run`/`web-dev`.

### Документы

- 📋 [План](impl/devops/iteration-0-local-stack/tasks/task-03-compose-full-stack/plan.md)
- 📝 [Summary](impl/devops/iteration-0-local-stack/tasks/task-03-compose-full-stack/summary.md)

---

## Задача 04: Makefile — stack-up/down/ps/logs/health ✅

### Цель

Единые команды orchestration; совместимость с существующими `db-*`.

### Состав работ

- [x] `stack-up`, `stack-down`, `stack-ps`, `stack-logs`, `stack-logs-tail`, `stack-health`, `stack-init`, `stack-up-bot`
- [x] `db-up` → `docker compose up -d postgres`; `db-reset` с хоста
- [x] `.PHONY`; упоминание в `README.md`

### Артефакты

- [`Makefile`](../../Makefile)

### Definition of Done

**Агент:** все `stack-*` и `db-*` targets исполняются; `stack-health` проверяет PG + backend + web.

**Пользователь:** `make stack-up && make stack-health` — зелёный вывод; `make stack-logs SVC=backend` показывает логи API.

### Документы

- 📋 [План](impl/devops/iteration-0-local-stack/tasks/task-04-makefile-stack/plan.md)
- 📝 [Summary](impl/devops/iteration-0-local-stack/tasks/task-04-makefile-stack/summary.md)

---

## Задача 05: Ревью Docker (`docker-expert`) ✅

### Цель

Проверить Dockerfile'ы и compose по best practices; устранить findings до документирования.

> Skill: **`docker-expert`** (через `/find-skills` если нет локально)

### Состав работ

- [x] Review: build context, non-root, healthchecks
- [x] Review: secrets via env; `.dockerignore`
- [x] Review: networking, migrate/seed; 2 раунда fixes
- [x] Findings → [task-05 summary](impl/devops/iteration-0-local-stack/tasks/task-05-docker-review/summary.md)

### Артефакты

- правки в `devops/docker/*`, `docker-compose.yml`
- checklist findings → [summary](impl/devops/iteration-0-local-stack/tasks/task-05-docker-review/summary.md)

### Definition of Done

**Агент:** review checklist пройден; критичные issues закрыты; `make stack-up` после правок.

**Пользователь:** прочитать summary § «Review findings» — понятно, что сознательно отложено (post-MVP).

### Документы

- 📋 [План](impl/devops/iteration-0-local-stack/tasks/task-05-docker-review/plan.md)
- 📝 [Summary](impl/devops/iteration-0-local-stack/tasks/task-05-docker-review/summary.md)

---

## Задача 06: Инструкция compose + обновление docs ✅

### Цель

Отдельный гайд локального stack и синхронизация проектной документации.

### Состав работ

- [x] `docs/devops/docker-compose-local.md`
- [x] [onboarding.md](../onboarding.md), [architecture.md](../architecture.md)
- [x] [README.md](../../README.md), [backend/README.md](../../backend/README.md), [plan.md](../plan.md)
- [x] [summary iter 0](impl/devops/iteration-0-local-stack/summary.md) ✅

### Артефакты

- `docs/devops/docker-compose-local.md`
- правки onboarding, architecture, README, plan

### Definition of Done

**Агент:** гайд самодостаточен; ссылки из onboarding/architecture ведут на актуальные команды; iter 0 summary ✅.

**Пользователь:** по `docs/devops/docker-compose-local.md` поднять stack с нуля на чистой машине (clone → `.env` → `make stack-up`).

### Документы

- 📋 [План](impl/devops/iteration-0-local-stack/tasks/task-06-docs-compose/plan.md)
- 📝 [Summary](impl/devops/iteration-0-local-stack/tasks/task-06-docs-compose/summary.md)

**Проверка итерации 0 (после 06):**  
**Агент:** `make stack-up && make stack-health`; web smoke login @ivan_p.  
**Пользователь:** пройти [smoke-test.md](../smoke-test.md) на stack-окружении.

---

## Итерация 1 — Сборка образов и публикация в GHCR ✅

**Ценность:** воспроизводимые образы в GitHub Container Registry; локальный запуск без `docker build` — pull из GHCR через **тот же** корневой `docker-compose.yml`.

**Критерии итерации:**
- push в `ghcr.io/<org>/diaai-{backend,bot,web}` на merge/tag (workflow) ✅
- режим `image:` (env/profiles) в корневом compose — без отдельного compose-файла ✅
- локально: `make stack-up-registry` — health green ✅

**Не в scope:** deploy на VPS/K8s, CD, rollback, production secrets.

→ [iteration-1-registry-ci/plan.md](impl/devops/iteration-1-registry-ci/plan.md) · [summary](impl/devops/iteration-1-registry-ci/summary.md)

---

## Задача 07: GitHub Actions → GHCR ✅

### Цель

Workflow сборки и публикации образов трёх сервисов в GitHub Container Registry.

> Skill: **`github-actions-templates`** (через `/find-skills`)

### Состав работ

- [x] `.github/workflows/docker-publish.yml` — build matrix backend/bot/web; context и `file:` из `devops/docker/*`
- [x] Login GHCR (`GITHUB_TOKEN` / `packages: write`); tags: `sha`, `main`, semver optional
- [x] Cache (GHA cache или registry); не публиковать секреты в layers
- [x] `devops/ci/README.md` — naming, pull commands, required permissions
- [ ] Dry-run локально: `act` optional или manual workflow_dispatch

### Артефакты

- `.github/workflows/docker-publish.yml`
- `devops/ci/README.md`

### Definition of Done

**Агент:** workflow green на push; три образа видны в GHCR с ожидаемыми tags.

**Пользователь:** в GitHub Packages — образы backend/bot/web; README объясняет, как pull.

### Документы

- 📋 [План](impl/devops/iteration-1-registry-ci/tasks/task-07-gha-ghcr/plan.md)
- 📝 [Summary](impl/devops/iteration-1-registry-ci/tasks/task-07-gha-ghcr/summary.md)

---

## Задача 08: Compose на образах registry + ревью ✅

### Цель

Запуск stack из опубликованных образов через **корневой** `docker-compose.yml` (profiles/env); ревью parity build vs pull.

### Состав работ

- [x] Режим registry в **том же** `docker-compose.yml`: env `IMAGE_TAG` + profile `registry` — `image: ghcr.io/...` для backend, web, bot
- [x] `postgres` — официальный `postgres:16-alpine` (без изменений)
- [x] `make stack-up-registry` / docs: переключение build ↔ registry без второго compose-файла
- [x] Ревью (docker-expert): parity env между режимами; documented diff
- [x] Обновить `docs/devops/docker-compose-local.md` § Registry mode

### Артефакты

- правки **корневого** [`docker-compose.yml`](../../docker-compose.yml) (profiles/env)
- правки `devops/ci/README.md`, docs

### Definition of Done

**Агент:** `make stack-up-registry` (profile `registry`) поднимает stack без local build — только корневой compose.

**Пользователь:** по docs переключиться build → registry mode одной командой, без `-f` другого файла.

### Документы

- 📋 [План](impl/devops/iteration-1-registry-ci/tasks/task-08-compose-registry/plan.md)
- 📝 [Summary](impl/devops/iteration-1-registry-ci/tasks/task-08-compose-registry/summary.md)

---

## Задача 09: Локальная проверка GHCR + docs ✅

### Цель

E2E: pull образов из registry → stack → health + smoke; закрытие области devops (prep phase).

### Состав работ

- [x] Сценарий: `make stack-up-registry` → `make stack-health`
- [x] Smoke: web login, backend `/health`, optional bot profile
- [x] Обновить onboarding, architecture, [doc-audit.md](../doc-audit.md) при необходимости
- [x] Закрыть iter 1 и область: [impl/devops/summary.md](impl/devops/summary.md)

### Артефакты

- verification log в task-09 summary
- финальные правки docs

### Definition of Done

**Агент:** registry-mode stack verified; iter 1 summary ✅; `make test` по-прежнему green (unit tests без compose).

**Пользователь:** на другой машине — pull GHCR images и поднять stack по инструкции без исходников build.

### Документы

- 📋 [План](impl/devops/iteration-1-registry-ci/tasks/task-09-registry-verify/plan.md)
- 📝 [Summary](impl/devops/iteration-1-registry-ci/tasks/task-09-registry-verify/summary.md)

**Проверка итерации 1 (после 09):**  
**Агент:** CI workflow + local registry stack green.  
**Пользователь:** подтвердить образы в GHCR и один smoke на pull-only окружении.

---

## Post-MVP (не в этом tasklist)

| Тема | Статус |
|------|--------|
| Deploy staging/prod (VPS, Fly, Railway, K8s) | 📋 Planned |
| CD: auto-deploy on tag | 📋 Planned |
| Secrets: GitHub Environments, Vault | 📋 Planned |
| Observability: logs, metrics, alerts | 📋 Planned |
| Full CI: lint/test in GHA on every PR | 📋 Planned |

---

## Связанные документы

| Документ | Назначение |
|----------|------------|
| [docker-compose-local.md](../devops/docker-compose-local.md) | build-режим stack |
| [ghcr-stack.md](../devops/ghcr-stack.md) | stack из GHCR |
| [devops/ci/README.md](../../devops/ci/README.md) | CI, образы, tags |
| [templates/tasklist.md](../templates/tasklist.md) | формат tasklist |
| [templates/workflow.md](../templates/workflow.md) | plan/summary per task |
| [architecture.md](../architecture.md) | компоненты и порты |
| [onboarding.md](../onboarding.md) | ручной dev path |
| [smoke-test.md](../smoke-test.md) | проверка после stack-up |
| [integrations.md](../integrations.md) | внешние сервисы и env |
