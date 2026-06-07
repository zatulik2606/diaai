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
| 3 | Миграция на backend | Бот как тонкий клиент, без локального состояния | 📋 Planned | [план](impl/bot/iteration-2-backend-client/plan.md) · [summary](impl/bot/iteration-2-backend-client/summary.md) |

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

## Итерация 3: Миграция на backend 📋

### Цель

Перевести бота на backend API: история и LLM — через ядро системы.

### Ценность

Единый контекст пользователя для bot и будущего web.

### Критерии завершения

- [ ] бот не использует SessionStore в RAM
- [ ] запросы к LLM идут через backend
- [ ] история сохраняется между перезапусками

### Артефакты

- `bot/` или обновлённый `src/diaai/` — тонкий клиент
- интеграция с backend API

### Документы

- 📋 [План](impl/bot/iteration-2-backend-client/plan.md)
- 📝 [Summary](impl/bot/iteration-2-backend-client/summary.md)
