# Task 06: Чат в основной области — polish

Итерация: [iteration-6-main-chat](../../plan.md) · [tasklist-frontend.md](../../../../../tasklist-frontend.md)

**Статус:** ✅ Done · [summary](summary.md)

---

## Цель

Polish `/chat`: скрыть FAB, error boundary, layout; regression FAB ↔ page.

## Состав работ

### Из iter 5 (уже ✅)

- [x] Route `/chat` — `ChatView` + `AssistantChatPanel`
- [x] Shared components с FAB
- [x] Единая история — `AssistantChatProvider`

### iter 6

- [x] `ChatFab` — `usePathname()`, hide on `/chat`
- [x] `app/(app)/chat/error.tsx`
- [x] RSC guard в `chat/page.tsx` (`telegram_id`)
- [x] Layout polish — `ChatView` flex min-h-0
- [x] summary + tasklist 7/10

## Затронутые файлы

| Файл | Действие |
|------|----------|
| `web/components/chat-fab.tsx` | modify |
| `web/app/(app)/chat/error.tsx` | create |
| `web/app/(app)/chat/page.tsx` | modify |
| `web/components/assistant/chat-view.tsx` | modify |

## Проверка

```bash
make web-lint && make web-build
make backend-run && make web-dev
# ivan_p → FAB send → /chat → same message, no FAB on /chat
```

## Definition of Done

- [x] FAB hidden on `/chat`
- [x] error.tsx + panel retry (backend down)
- [x] tasklist iter 6 ✅
