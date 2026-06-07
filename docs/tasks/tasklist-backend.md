# Backend Tasklist

Опирается на [plan.md](../plan.md) · [vision.md](../vision.md) · [data-model.md](../data-model.md)

## Обзор

Итерации backend-ядра: персистентность, доменная логика, аналитика и рекомендации.

## Легенда статусов

- 📋 Planned — запланирован
- 🚧 In Progress — в работе
- ✅ Done — завершён

## Итерации

| Итерация | Название | Цель | Статус | Документы |
|----------|----------|------|--------|-----------|
| 2 | Backend-ядро и БД | API, PostgreSQL, базовые сущности | 📋 Planned | [план](impl/backend/iteration-1-core-db/plan.md) · [summary](impl/backend/iteration-1-core-db/summary.md) |
| 4 | Аналитика и динамика | Прогресс, тренды, рекомендации | 📋 Planned | [план](impl/backend/iteration-2-analytics/plan.md) · [summary](impl/backend/iteration-2-analytics/summary.md) |

---

## Итерация 2: Backend-ядро и БД 📋

### Цель

Создать единое ядро: API + PostgreSQL + сохранение событий питания и инсулина.

### Ценность

Данные не теряются между сессиями; основа для bot, web и аналитики.

### Критерии завершения

- [ ] backend принимает и возвращает данные через API
- [ ] PostgreSQL: пользователи, диалоги, запросы, события питания/инсулина
- [ ] LLM и анализ фото — через backend
- [ ] миграции БД работают

### Артефакты

- `backend/` — код сервера
- схема БД (миграции)
- ADR: [adr-001-database.md](../adr/adr-001-database.md)

### Документы

- 📋 [План](impl/backend/iteration-1-core-db/plan.md)
- 📝 [Summary](impl/backend/iteration-1-core-db/summary.md)

---

## Итерация 4: Аналитика и динамика 📋

### Цель

Агрегировать события, формировать снимки прогресса и справочные рекомендации.

### Ценность

Пользователь видит динамику ХЕ / БЖЕ / БЖУ / инсулина, а не только текущий момент.

### Критерии завершения

- [ ] снимки прогресса за день / неделю / месяц
- [ ] сигналы изменений (улучшение / ухудшение)
- [ ] рекомендации на основе истории (без назначения доз)
- [ ] API для клиентов (bot, web)

### Артефакты

- модули аналитики в `backend/`
- сущности: Снимок прогресса, Рекомендация (см. [data-model.md](../data-model.md))

### Документы

- 📋 [План](impl/backend/iteration-2-analytics/plan.md)
- 📝 [Summary](impl/backend/iteration-2-analytics/summary.md)
