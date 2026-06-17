# Task 05: Чат с ассистентом (FAB + `/chat`)

Итерация: [iteration-5-assistant-chat](../../plan.md) · [tasklist-frontend.md](../../../../../tasklist-frontend.md)

**Статус:** ✅ Done · [summary](summary.md)

---

## Цель

BFF + UI: FAB-чат, страница `/chat`, общий `AssistantChatProvider`, history/send/optimistic/errors.

## Состав работ

### Types + server lib

- [x] `web/lib/types/assistant-chat.ts`
- [x] `fetchAssistantHistory`, `sendAssistantMessage` в `backend-client.ts`

### BFF

- [x] `GET web/app/api/assistant/history/route.ts`
- [x] `POST web/app/api/assistant/messages/route.ts`

### UI + provider

- [x] shadcn `scroll-area`
- [x] `components/assistant/*` — message, list, input, panel, provider, root, chat-view
- [x] `chat-fab.tsx` — Sheet, lazy load
- [x] `app/(app)/chat/page.tsx` + `loading.tsx`
- [x] `layout.tsx` — `AssistantChatRoot`

## Затронутые файлы

| Область | Файлы |
|---------|-------|
| Create | `lib/types/assistant-chat.ts`, `app/api/assistant/**`, `app/(app)/chat/**`, `components/assistant/**`, `ui/scroll-area.tsx` |
| Modify | `lib/backend-client.ts`, `components/chat-fab.tsx`, `app/(app)/layout.tsx` |

## Проверка

```bash
make web-lint && make web-build
make backend-run && make web-dev
# ivan_p → /chat или FAB → history + send
curl -s -X POST http://127.0.0.1:3000/api/auth/login -H "Content-Type: application/json" \
  -d '{"username":"ivan_p"}' -c /tmp/c.cookie
curl -s "http://127.0.0.1:3000/api/assistant/history?limit=5" -b /tmp/c.cookie | jq '.total'
```

## Definition of Done

- [x] `/chat` из sidebar (doctor + diabetic)
- [x] History on open; scroll; send → reply
- [x] FAB и `/chat` — одна история (provider)
- [x] Error + retry при сбое загрузки истории
- [x] Service token not in client bundle
