# Итерация frontend 6: Чат в основной области (polish)

Опирается на [tasklist-frontend.md](../../../tasklist-frontend.md) · [impl/frontend/plan.md](../plan.md) · [iteration-5-assistant-chat](../iteration-5-assistant-chat/plan.md)

Skills: [shadcn](../../../../.agents/skills/shadcn/SKILL.md) · [vercel-react-best-practices](../../../../.agents/skills/vercel-react-best-practices/SKILL.md) · [nextjs-app-router-patterns](../../../../.agents/skills/nextjs-app-router-patterns/SKILL.md)

**Статус:** 📋 Planned

---

## Цель

Закрыть остаток [tasklist iter 6](../../../tasklist-frontend.md): полноэкранный `/chat` как first-class экран. **Ядро уже в iter 5** — здесь polish и DoD tasklist.

## Что уже сделано (iter 5)

| Пункт tasklist | Статус |
|----------------|--------|
| Route `/chat` — full-page chat | ✅ `chat-view.tsx` + `page.tsx` |
| Shared components с FAB | ✅ `AssistantChatPanel` |
| Единая история | ✅ `AssistantChatProvider` |

## Gap analysis (iter 5 → iter 6)

| Блок | Сейчас | Целевое iter 6 |
|------|--------|----------------|
| `/chat` error boundary | нет | `error.tsx` + retry |
| FAB на `/chat` | дублирует UI | скрыть FAB на `/chat` (optional UX) |
| Mobile layout | базовый | проверить Sheet vs full page |
| Docs / tasklist | iter 6 «Next» | закрыть iter 6, 7/10 |

## Задачи

| Task | Описание | Документ |
|------|----------|----------|
| 06 | Polish `/chat` + FAB UX | [task-06 plan](tasks/task-06-main-chat/plan.md) |

## Definition of Done

**Self-check:** FAB скрыт на `/chat` (или осознанно оставлен); `error.tsx`; `make web-build` green.

**User-check:** сообщение FAB ↔ `/chat` синхронно; навигация Chat в sidebar стабильна.

## Out of scope

- Новые API, фото, streaming
