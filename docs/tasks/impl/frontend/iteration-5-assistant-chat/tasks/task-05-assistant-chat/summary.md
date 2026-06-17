# Task 05: Чат с ассистентом (FAB + `/chat`) — Summary

> **Статус:** ✅ Done

Итерация: [iteration-5-assistant-chat](../../plan.md) · [plan](plan.md)

---

## Сделано

### Types + server lib

- `web/lib/types/assistant-chat.ts`
- `fetchAssistantHistory`, `sendAssistantMessage` в `backend-client.ts`

### BFF

- `GET web/app/api/assistant/history/route.ts`
- `POST web/app/api/assistant/messages/route.ts`

### UI + shared state

- shadcn `scroll-area`
- `assistant-chat-provider.tsx` + `assistant-chat-root.tsx` в layout
- `assistant-chat-panel.tsx`, `chat-message*`, `chat-input.tsx`, `chat-view.tsx`
- `chat-fab.tsx` — Sheet + lazy load
- `app/(app)/chat/page.tsx`, `loading.tsx`

## Отклонения от плана

| Отклонение | Причина |
|------------|---------|
| `/chat` в iter 5 | проверка навигации и единой истории с FAB |
| Provider вместо локального hook | синхронизация FAB ↔ page |

## Проверки

| Команда / сценарий | Результат |
|--------------------|-----------|
| `make web-lint && make web-build` | ✅ |
| BFF history `ivan_p` | ✅ 8+ seed messages |
| POST send + reply | ✅ |
| `/chat` HTTP 200, sidebar nav | ✅ |
| FAB ↔ `/chat` same history | ✅ provider |

## Skills review

| Skill | Verdict |
|-------|---------|
| shadcn | ✅ Sheet, ScrollArea, Input, Skeleton |
| vercel-react-best-practices | ✅ BFF server-only token; client chat island |
| nextjs-app-router-patterns | ✅ route handlers, loading, shared provider |
