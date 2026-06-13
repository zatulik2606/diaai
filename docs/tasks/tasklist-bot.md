# Bot Tasklist

Опирается на [plan.md](../plan.md) · [vision.md](../vision.md)

## Обзор

Итерации Telegram-бота: от MVP-клиента до тонкого клиента backend.

## Легенда статусов

- 📋 Planned — запланирован
- 🚧 In Progress — в работе
- ✅ Done — завершён

## Итерации

| Итерация | Название | Цель | Статус | Документы |
|----------|----------|------|--------|-----------|
| 1 | MVP Telegram-бота | Диалог, ХЕ/БЖЕ/БЖУ, фото, история в RAM | ✅ Done | [план](impl/bot/iteration-1-mvp/plan.md) · [summary](impl/bot/iteration-1-mvp/summary.md) |
| 3 | Миграция на backend | Бот как тонкий клиент, без локального состояния | ✅ Done | [backend task-07](impl/backend/iteration-3-delivery/tasks/task-07-bot-refactor/plan.md) · [summary](impl/backend/iteration-3-delivery/tasks/task-07-bot-refactor/summary.md) |

---

## Итерация 1: MVP Telegram-бота ✅

### Цель

Запустить первый клиент: текст и фото → LLM → ответ с учётом истории.

### Ценность

Пользователь получает справочную поддержку по питанию и инсулину в Telegram.

### Критерии завершения

- [x] `make run` запускает бота
- [x] ответы на текст и фото
- [x] fallback при ошибках LLM

### Артефакты

- `src/diaai/` — код бота
- `prompts/system.txt` — системный промпт
- `Makefile`, `.env.example`

### Документы

- 📋 [План](impl/bot/iteration-1-mvp/plan.md)
- 📝 [Summary](impl/bot/iteration-1-mvp/summary.md)

---

## Итерация 3: Миграция на backend ✅

### Цель

Перевести бота на backend API: история и LLM — через ядро системы.

Реализовано в рамках [backend task-07](impl/backend/iteration-3-delivery/tasks/task-07-bot-refactor/plan.md).

### Ценность

Единый контекст пользователя для bot и будущего web.

### Критерии завершения

- [x] бот не использует SessionStore в RAM (prod-путь)
- [x] запросы к LLM идут через backend
- [x] история сохраняется между перезапусками бота (PostgreSQL)

### Артефакты

- `src/diaai/backend_client.py` — httpx-клиент backend API
- обновлённые `handlers.py`, `main.py`, `bot.py`, `config.py`

### Документы

- 📋 [План backend task-07](impl/backend/iteration-3-delivery/tasks/task-07-bot-refactor/plan.md)
- 📝 [Summary backend task-07](impl/backend/iteration-3-delivery/tasks/task-07-bot-refactor/summary.md)
