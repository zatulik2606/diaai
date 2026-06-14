# diaai

Система ежедневного сопровождения людей с сахарным диабетом — питание, инсулин, динамика состояния.

> Справочная поддержка, **не замена врачу**. Система не назначает дозы инсулина.

## О проекте

Диабет требует постоянного учёта еды, инсулина и контекста дня — это утомляет и легко теряется в голове. diaai помогает осмыслять события, замечать изменения и готовиться к разговору с врачом. Сейчас — Telegram-бот, backend API и каркас веб-клиента (`web/`).

## Архитектура

```mermaid
flowchart LR
    User["Пользователь"]
    Bot["Telegram-бот"]
    Web["Веб-клиент"]
    Backend["Backend ядро"]
    DB["PostgreSQL"]

    User --> Bot
    User -.-> Web
    Bot --> Backend
    Web --> Backend
    Backend --> DB
```

MVP-бот — тонкий клиент backend API (история в PostgreSQL). Подробнее: [vision.md](docs/vision.md).

## Статус

| # | Этап | Статус |
|---|------|--------|
| 1 | MVP Telegram-бота | ✅ Done |
| 2 | Backend-ядро и БД | ✅ Done |
| 3 | Миграция бота на backend | ✅ Done |
| 4 | Аналитика и динамика | 📋 Planned |
| 5 | Веб-интерфейс | 🚧 In Progress |

Дорожная карта: [plan.md](docs/plan.md).

## Документация

- [Идея продукта](docs/idea.md)
- [Архитектурное видение](docs/vision.md)
- [Модель данных](docs/data-model.md)
- [Интеграции](docs/integrations.md)
- [Backend (dev)](backend/README.md)
- [API](docs/api/) — [контракт v1](docs/api/api-contract.md)
- [План](docs/plan.md)
- [Задачи](docs/tasks/)

## Быстрый старт

**Telegram-бот:** токены — [how-to-get-tokens.md](docs/how-to-get-tokens.md); `cp .env.example .env` (`TELEGRAM_BOT_TOKEN`, `BACKEND_URL`, `BACKEND_SERVICE_TOKEN`).

1. Backend + БД: `make db-reset` (PostgreSQL + migrate + seed) → `make backend-run` — подробнее [backend/README.md](backend/README.md)
2. Бот: `make install && make run` (в отдельном терминале)

Проверка данных: `make db-inspect`.

**Web-клиент:** `cp web/.env.example web/.env.local` → `make web-install && make web-dev` (:3000). Нужен `make backend-run`. Подробнее [web/README.md](web/README.md).

## Quality

```bash
make lint    # ruff: src, backend, tests
make test    # 52 tests (37 backend + 15 bot)
```
