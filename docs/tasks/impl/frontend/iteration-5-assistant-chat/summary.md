# Итерация frontend 5: Summary

> **Статус:** ✅ Done

Опирается на [plan.md](plan.md) · [tasklist-frontend.md](../../../tasklist-frontend.md)

---

## Сделано

### Task-05: FAB + `/chat` ✅

- BFF `/api/assistant/history` и `/api/assistant/messages` (service token на сервере)
- `AssistantChatProvider` — единая история FAB ↔ `/chat`
- `AssistantChatPanel` (variants `fab` / `page`): history, send, optimistic UI, pagination, retry при ошибке загрузки
- `ChatFab` — Sheet ~380px, lazy load при открытии
- `/chat` — `ChatView` + `loading.tsx`, навигация из sidebar (doctor + diabetic)
- Детали: [task-05 summary](tasks/task-05-assistant-chat/summary.md)

| Компонент | Путь |
|-----------|------|
| Provider | `web/components/assistant/assistant-chat-provider.tsx`, `assistant-chat-root.tsx` |
| Types | `web/lib/types/assistant-chat.ts` |
| Server lib | `web/lib/backend-client.ts` |
| BFF | `web/app/api/assistant/*` |
| UI | `web/components/assistant/*`, `chat-fab.tsx` |
| Page | `web/app/(app)/chat/` |

## Ценность

Диалог с ассистентом (D2) через FAB и пункт меню **Chat**; история из PG; отправка через OpenRouter; синхронное состояние между виджетом и страницей.

## Отклонения от плана

| Отклонение | Причина |
|------------|---------|
| `/chat` реализован в iter 5 (раньше iter 6) | навигация + согласованность с FAB |
| `AssistantChatProvider` в layout | общая история без дублирования state |

## Проверки (Self-check ✅)

| Проверка | Результат |
|----------|-----------|
| `make web-lint && make web-build` | ✅ |
| BFF history + send без mock | ✅ |
| Service token не в client bundle | ✅ |
| `/chat` из sidebar + FAB | ✅ |
| Scroll списка сообщений | ✅ layout fix |
| Ошибка при остановленном backend | ✅ «Сервис недоступен» |

## User-check

```bash
make backend-run && make web-dev
# ivan_p → Chat в sidebar ИЛИ FAB → seed history (борщ, банан…)
# отправить вопрос → ответ (OPENROUTER_API_KEY)
# сообщение из FAB видно на /chat без reload
# doctor_ivanov → FAB / chat от своего telegram_id
```

## Следующий шаг

[iteration-6-main-chat](../iteration-6-main-chat/plan.md) — polish: `error.tsx`, скрытие FAB на `/chat`, закрытие tasklist iter 6.
