# Technical Debt — Frontend (`web/`)

> **Дата аудита:** 2026-06-07  
> **Skills:** [vercel-react-best-practices](../.agents/skills/vercel-react-best-practices/SKILL.md) · [nextjs-app-router-patterns](../.agents/skills/nextjs-app-router-patterns/SKILL.md) · [shadcn](../.agents/skills/shadcn/SKILL.md)  
> **Связанные артефакты:** [frontend-review.md](frontend-review.md) (iter 7) · [tasklist-frontend.md](../tasks/tasklist-frontend.md)

## Легенда приоритетов

| Приоритет | Смысл | Когда брать в работу |
|-----------|--------|----------------------|
| **P0** | Блокер / сломанный UX | Сразу |
| **P1** | Высокий — функциональность, perf, платформа | Ближайшие 1–2 итерации |
| **P2** | Средний — консистентность, поддерживаемость | По мере касания области |
| **P3** | Низкий — polish, инфраструктура | Backlog post-MVP |

**Статусы:** `open` · `partial` (частично закрыто) · `done`

---

## Погашено (iter 7)

| ID | Проблема | Решение | Skill |
|----|----------|---------|-------|
| TD-FE-R01 | Recharts `width(-1) height(-1)` | `ChartContainer`: `min-w-0`, `minHeight={1}` | vercel · rendering |
| TD-FE-R02 | recharts/lucide в bundle без tree-shake hint | `optimizePackageImports` в `next.config.ts` | vercel · bundle |
| TD-FE-R03 | Scatter грузится на первом заходе в leaderboard | `next/dynamic` + mount по табу | vercel · bundle-conditional |

---

## P0 — Критично

*Открытых P0 нет.* Сборка и lint green; основные маршруты работают при поднятом backend.

---

## P1 — Высокий

### TD-FE-001 · Mobile navigation отсутствует `open`

| | |
|---|---|
| **Skill** | shadcn · nextjs-app-router |
| **Файлы** | `web/components/app-sidebar.tsx` (`hidden … md:flex`) |
| **Проблема** | На `< md` sidebar скрыт, альтернативной навигации (Sheet/Drawer/hamburger) нет — пользователь не может перейти между экранами без прямого URL. |
| **Рекомендация** | shadcn `Sheet` + `Button` trigger в header или полноценный `Sidebar` с mobile variant. Backlog с iter 2. |
| **Effort** | M |

### TD-FE-002 · Submissions `detail_url` ведут на несуществующие routes `open`

| | |
|---|---|
| **Skill** | nextjs-app-router |
| **Файлы** | `web/components/dashboard/submissions-list.tsx` · backend `web_patient_service.py` (`/patients/{id}/events|photos/{id}`) |
| **Проблема** | Ссылка «Детали» ведёт на routes, которых нет в `web/app/` → 404. Контракт [frontend-contract.md](../api/frontend-contract.md) предполагает frontend routes. |
| **Рекомендация** | (a) добавить страницы деталей, или (b) modal/Sheet с данными item, или (c) убрать ссылку до реализации (см. [api-contract-review.md](../api/api-contract-review.md) P3). |
| **Effort** | M–L |

### TD-FE-003 · `middleware.ts` deprecated в Next.js 16 `open`

| | |
|---|---|
| **Skill** | nextjs-app-router |
| **Файлы** | `web/middleware.ts` |
| **Проблема** | `make web-build` предупреждает: convention `middleware` → `proxy`. Риск поломки при апгрейде Next. |
| **Рекомендация** | Миграция на [proxy](https://nextjs.org/docs/messages/middleware-to-proxy) по документации Next 16. |
| **Effort** | S |

### TD-FE-004 · `TooltipProvider` на каждый `ProductChip` `open`

| | |
|---|---|
| **Skill** | vercel · rerender / js |
| **Файлы** | `web/components/leaderboard/product-chip.tsx` |
| **Проблема** | В таблице лидерборда создаётся N экземпляров `TooltipProvider` (по числу продуктов × пациентов) — лишние контексты и дерево React. |
| **Рекомендация** | Поднять один `TooltipProvider` на уровень `LeaderboardTable` или `leaderboard/page`. |
| **Effort** | S |

### TD-FE-005 · Дублирование `getSession()` без dedup `open`

| | |
|---|---|
| **Skill** | vercel · server-cache-react |
| **Файлы** | `web/lib/session.ts` · `(app)/layout.tsx` + каждая `page.tsx` |
| **Проблема** | Layout и page независимо парсят cookie сессии в одном request (layout уже редиректит неавторизованных, page снова вызывает `getSession`). |
| **Рекомендация** | Обернуть `getSession` в `React.cache()`; передавать session из layout через props/context server-side где возможно. |
| **Effort** | S |

---

## P2 — Средний

### TD-FE-006 · Dashboard — монолитный fetch, нет streaming `open`

| | |
|---|---|
| **Skill** | vercel · async-suspense-boundaries · nextjs |
| **Файлы** | `web/app/(app)/dashboard/page.tsx` · `lib/backend-client.ts` (`fetchPatientDashboard` — 5 parallel, но один await) |
| **Проблема** | Страница блокируется до загрузки всех блоков; `loading.tsx` показывается целиком, без progressive streaming по секциям. |
| **Рекомендация** | Разбить на server components + `<Suspense>` per card (KPI, chart, tables). |
| **Effort** | M |

### TD-FE-007 · `AssistantChatProvider` — context value без `useMemo` `open`

| | |
|---|---|
| **Skill** | vercel · rerender-memo |
| **Файлы** | `web/components/assistant/assistant-chat-provider.tsx` |
| **Проблема** | Новый object value на каждый render → лишние re-renders потребителей (`ChatFab`, `ChatView`, panel). |
| **Рекомендация** | `useMemo` для value; при росте чата — split context (state / actions). |
| **Effort** | S |

### TD-FE-008 · Форма login — не shadcn Field pattern `open`

| | |
|---|---|
| **Skill** | shadcn · forms |
| **Файлы** | `web/app/(auth)/login/page.tsx` |
| **Проблема** | `div` + `Label` + `Input` вместо `FieldGroup`/`Field`; ошибки — `<p>`, без `data-invalid` / `aria-invalid`. |
| **Рекомендация** | Добавить shadcn Field-компоненты или `Alert` для ошибки; Server Action как альтернатива client fetch. |
| **Effort** | S |

### TD-FE-009 · Empty / error states — кастомная разметка `open`

| | |
|---|---|
| **Skill** | shadcn · composition |
| **Файлы** | `questions-table.tsx`, `submissions-list.tsx`, `leaderboard-table.tsx`, `assistant-chat-panel.tsx`, `*/error.tsx` |
| **Проблема** | Пустые списки и ошибки — `<p className="text-muted-foreground">` вместо `Empty` / `Alert`. Нет единого паттерна feedback. |
| **Рекомендация** | `npx shadcn add alert empty` (или sonner для toast); унифицировать error UI. |
| **Effort** | S–M |

### TD-FE-010 · Raw hex-цвета медалей `open`

| | |
|---|---|
| **Skill** | shadcn · styling |
| **Файлы** | `product-chip.tsx`, `bje-top5-legend.tsx` (`#FFD700`, `#C0C0C0`, …) |
| **Проблема** | Нарушение правила semantic colors; медали не адаптируются к теме через CSS variables. |
| **Рекомендация** | Токены в `globals.css` (`--medal-gold`, …) или `Badge` variants. |
| **Effort** | S |

### TD-FE-011 · `space-y-*` в loading skeletons `open`

| | |
|---|---|
| **Skill** | shadcn · styling |
| **Файлы** | `dashboard/loading.tsx`, `leaderboard/loading.tsx`, `chat/loading.tsx` |
| **Проблема** | Skill shadcn: spacing через `flex flex-col gap-*`, не `space-y-*`. |
| **Рекомендация** | Заменить на `flex flex-col gap-*`. |
| **Effort** | XS |

### TD-FE-012 · Нет `not-found.tsx` `open`

| | |
|---|---|
| **Skill** | nextjs-app-router |
| **Файлы** | `web/app/` |
| **Проблема** | Нет кастомной 404 для app routes; дефолт Next без брендинга diaai. |
| **Рекомендация** | `app/not-found.tsx` + при необходимости route-group variants. |
| **Effort** | XS |

### TD-FE-013 · Metadata только в root layout `open`

| | |
|---|---|
| **Skill** | nextjs-app-router |
| **Файлы** | `web/app/layout.tsx` · pages без `generateMetadata` |
| **Проблема** | Title «diaai» для всех вкладок; нет template `%s | diaai` per route. |
| **Рекомендация** | `export const metadata` / `generateMetadata` в `(app)/dashboard`, `leaderboard`, `chat`, `login`. |
| **Effort** | XS |

### TD-FE-014 · `ActivityChart` — recharts в initial dashboard bundle `open`

| | |
|---|---|
| **Skill** | vercel · bundle-dynamic-imports |
| **Файлы** | `dashboard/page.tsx` → `activity-chart.tsx` |
| **Проблема** | recharts (~heavy) грузится с первым экраном diabetic; scatter уже lazy (iter 7). |
| **Рекомендация** | `next/dynamic` для `ActivityChart` с Skeleton; acceptable для MVP если bundle в норме. |
| **Effort** | S |

### TD-FE-015 · Custom sidebar вместо shadcn Sidebar `open`

| | |
|---|---|
| **Skill** | shadcn · composition |
| **Файлы** | `web/components/app-sidebar.tsx` |
| **Проблема** | Hand-rolled nav; shadcn рекомендует `Sidebar` + `SidebarProvider` для responsive/mobile. |
| **Рекомендация** | Рефактор при закрытии TD-FE-001. |
| **Effort** | M |

### TD-FE-016 · Login page — полностью Client Component `open`

| | |
|---|---|
| **Skill** | nextjs-app-router · vercel |
| **Файлы** | `web/app/(auth)/login/page.tsx` |
| **Проблема** | `"use client"` на всей странице; форма могла бы быть Server Action + минимальный client island. |
| **Рекомендация** | Server Action `loginAction` + `useActionState` (React 19). |
| **Effort** | M |

### TD-FE-017 · Иконки с явным `size-4` в Button `open`

| | |
|---|---|
| **Skill** | shadcn · icons |
| **Файлы** | `chat-input.tsx`, `assistant-chat-panel.tsx`, `app-sidebar.tsx`, `chat-fab.tsx` |
| **Проблема** | Skill: sizing через CSS компонента + `data-icon`, не `className="size-4"`. |
| **Рекомендация** | `data-icon="inline-start|inline-end"` на иконках в Button. |
| **Effort** | XS |

### TD-FE-018 · Inline `ScatterTooltip` в файле chart `open`

| | |
|---|---|
| **Skill** | vercel · rerender-no-inline-components |
| **Файлы** | `web/components/leaderboard/leaderboard-scatter.tsx` |
| **Проблема** | Компонент tooltip объявлен в том же модуле и передаётся как `<ScatterTooltip />` — новая функция при hot reload; мелкий antipattern. |
| **Рекомендация** | Вынести в отдельный файл или module-level const. |
| **Effort** | XS |

### TD-FE-019 · Chat — client fetch через BFF `open`

| | |
|---|---|
| **Skill** | nextjs-app-router · vercel · client-swr-dedup |
| **Файлы** | `assistant-chat-provider.tsx` · `/api/assistant/*` |
| **Проблема** | История/отправка только client-side; оправдано FAB + shared state MVP, но без dedup/SWR при множественных panel instances. |
| **Рекомендация** | Оставить до refactor; при необходимости — SWR/React Query или initial history SSR на `/chat`. |
| **Effort** | M |

### TD-FE-020 · FAB — ручной `z-50` `open`

| | |
|---|---|
| **Skill** | shadcn · styling |
| **Файлы** | `web/components/chat-fab.tsx` |
| **Проблема** | Skill: не задавать z-index overlay-компонентам вручную; FAB — fixed button, не overlay lib. |
| **Рекомендация** | Проверить stacking с Sheet; при конфликтах — CSS variable `--fab-z` в theme. |
| **Effort** | XS |

---

## P3 — Низкий

### TD-FE-021 · Нет E2E smoke tests `open`

| | |
|---|---|
| **Skill** | nextjs · vercel |
| **Проблема** | Регрессии FAB↔/chat, auth, routes — только manual smoke ([frontend-review.md §6](frontend-review.md)). |
| **Рекомендация** | Playwright: login → dashboard → leaderboard → chat. |
| **Effort** | M |

### TD-FE-022 · Нет bundle analyzer в CI `open`

| | |
|---|---|
| **Skill** | vercel · bundle |
| **Проблема** | Нет автоматического контроля роста JS после iter 7 fixes. |
| **Рекомендация** | `@next/bundle-analyzer` в CI или periodic `pnpm build` + analyze. |
| **Effort** | S |

### TD-FE-023 · Длинные списки без `content-visibility` `open`

| | |
|---|---|
| **Skill** | vercel · rendering-content-visibility |
| **Файлы** | `chat-message-list.tsx`, `questions-table.tsx`, `leaderboard-table.tsx` |
| **Проблема** | При большом числе сообщений/строк — полный paint DOM. |
| **Рекомендация** | `content-visibility: auto` на row/item; virtual list при >100 items. |
| **Effort** | M |

### TD-FE-024 · Preload scatter при hover на таб `open`

| | |
|---|---|
| **Skill** | vercel · bundle-preload |
| **Файлы** | `leaderboard-tabs.tsx` |
| **Проблема** | Scatter грузится только после click; можно улучшить perceived perf. |
| **Рекомендация** | `onMouseEnter` на TabsTrigger «Карта» → `import()` prefetch. |
| **Effort** | XS |

### TD-FE-025 · `LogoutButton` без явного `type="button"` `open`

| | |
|---|---|
| **Skill** | shadcn · forms |
| **Файлы** | `web/components/logout-button.tsx` |
| **Проблема** | Minor a11y/consistency (default submit внутри form — здесь вне form, OK). |
| **Рекомендация** | `type="button"`. |
| **Effort** | XS |

### TD-FE-026 · `scrollIntoView` на каждое изменение messages `open`

| | |
|---|---|
| **Skill** | vercel · rerender |
| **Файлы** | `chat-message-list.tsx` |
| **Проблема** | Effect на весь массив `messages` — scroll при loadMore тоже. |
| **Рекомендация** | Scroll только при send / last message id change. |
| **Effort** | XS |

---

## Сводка

| Приоритет | Open | Partial | Done |
|-----------|------|---------|------|
| P0 | 0 | 0 | — |
| P1 | 5 | 0 | — |
| P2 | 15 | 0 | 3 (iter 7) |
| P3 | 6 | 0 | — |

**Рекомендуемый порядок:** TD-FE-001 (mobile) → TD-FE-002 (detail routes) → TD-FE-003 (proxy) → TD-FE-004/005 (quick wins) → iter 8 scope.

---

## История изменений

| Дата | Изменение |
|------|-----------|
| 2026-06-07 | Первичный аудит по skills; 26 open items + 3 done (iter 7) |
