# Task 06: Чат в основной области — polish

Итерация: [iteration-6-main-chat](../../plan.md) · [tasklist-frontend.md](../../../../../tasklist-frontend.md)

**Статус:** 📋 Planned

---

## Цель

Довести `/chat` до DoD tasklist: error boundary, UX polish, синхронизация с FAB (уже через provider).

## Состав работ

- [ ] `app/(app)/chat/error.tsx` — retry, сообщение про backend
- [ ] Скрыть `ChatFab` на `pathname === '/chat'` (optional)
- [ ] Проверить mobile: sidebar → `/chat`, высота panel
- [ ] `summary.md` + tasklist 7/10

## Затронутые файлы

| Файл | Действие |
|------|----------|
| `web/app/(app)/chat/error.tsx` | create |
| `web/components/chat-fab.tsx` | hide on `/chat` |
| `docs/tasks/impl/frontend/iteration-6-main-chat/summary.md` | create |

## Проверка

```bash
make web-dev
# ivan_p → FAB send → /chat видит сообщение
# остановить backend → /chat error + retry
```

## Definition of Done

- [ ] FAB и `/chat` — одна история (regression)
- [ ] Error state на route level
- [ ] tasklist iter 6 ✅
