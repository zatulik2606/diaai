# Prompt: генерация tasklist

Контекст для агента при создании или обновлении tasklist'ов областей bot, backend, web.

## Контекст (обязательные ссылки)

| Документ | Назначение |
|----------|------------|
| [plan.md](../plan.md) | итерации 1–5, статусы, критерии |
| [vision.md](../vision.md) | backend-as-core, границы системы |
| [data-model.md](../data-model.md) | доменные сущности |
| [integrations.md](../integrations.md) | MVP vs Future интеграции |
| [templates/tasklist.md](../templates/tasklist.md) | формат tasklist |

## Prompt

```markdown
На основе plan.md и проектной документации (vision, data-model, integrations)
создай или обнови tasklist для области {bot|backend|web}.

Требования:
- следуй шаблону docs/templates/tasklist.md
- одна область = один tasklist в docs/tasks/
- для каждой итерации из plan.md: цель, ценность, критерии, ссылки на plan/summary итерации
- декомпозируй итерацию на задачи task-01, task-02 … с plan.md / summary.md в impl/<область>/iteration-N-*/tasks/
- не выходи за scope vision.md; не дублируй ADR и data-model целиком
- высокий уровень: без мелких технических подзадач

Для backend (docs/tasks/tasklist-backend.md) обязательно:
- секция «Ориентир по последовательности задач» из 8 шагов (стек → каркас → контракты → API → хранение → entry point → docs → локальный запуск)
- итерация 2: task-01 … task-09 по шагам 1–8; task-04-api-conventions (форматы, ошибки, версии); task-10-bot-refactor (если логика в боте)
- секция «Качество и инженерные практики» в конце документа
- итерация 4: 4 задачи (контракты → снимки → рекомендации → docs и запуск)
```

## Ориентир последовательности (backend)

1. Выбор backend-стека и фиксация ключевого архитектурного решения
2. Генерация каркаса / шаблона backend-проекта
3. Проектирование и базовое документирование API-контрактов
4. Реализация API по контрактам с базовыми проверками
5. Подключение хранения и интеграций, если это требуется логикой плана
6. Подготовка backend как единой точки входа для клиентов
7. Актуализация проектной документации и соглашений (vision.md, data-model.md, integrations.md) по факту реализации
8. Команды и сценарии локального запуска всей системы

## Декомпозиция по областям (эталон)

### Bot

**Итерация 1 (Done):** task-01 каркас, task-02 handlers, task-03 photo  
**Итерация 3 (Planned):** task-01 backend-client, task-02 migrate-session

### Backend

**Итерация 2 (Planned):** task-01 stack-adr, task-02 scaffold, task-03 api-contracts, task-04 api-conventions, task-05 api-impl, task-06 storage-integrations, task-07 entry-point, task-08 docs-sync, task-09 local-run, task-10 bot-refactor

**Итерация 4 (Planned):** task-01 analytics-contracts, task-02 progress-snapshots, task-03 recommendations, task-04 docs-and-run

### Web

**Итерация 5 (Planned):** task-01 diabetic dashboard, task-02 consultations (optional doctor)

Эталон backend: [tasklist-backend.md](../tasks/tasklist-backend.md).
