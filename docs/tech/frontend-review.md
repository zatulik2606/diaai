# Frontend quality review

> Дата: 2026-06-07 · Итерация: [iteration-7-quality-review](../tasks/impl/frontend/iteration-7-quality-review/plan.md)  
> Skills: vercel-react-best-practices · nextjs-app-router-patterns · shadcn

Легенда: **Pass** — соответствует · **Warn** — некритично, backlog · **Fix** — исправлено в iter 7

---

## Сводка

| Категория | Pass | Warn | Fix (iter 7) |
|-----------|------|------|--------------|
| Data fetching / RSC | 6 | 1 | 0 |
| Bundle | 2 | 1 | 2 |
| Re-renders | 4 | 1 | 0 |
| App Router patterns | 5 | 0 | 0 |
| shadcn / a11y | 5 | 2 | 0 |
| **Итого** | **22** | **5** | **2** |

Open **Fix**: нет.

---

## 1. Vercel React Best Practices

### Eliminating waterfalls — Pass

| Проверка | Статус | Комментарий |
|----------|--------|-------------|
| RSC fetch в page, не в layout | Pass | `dashboard/page.tsx`, `leaderboard/page.tsx`, `chat/page.tsx` |
| Нет лишних await в layout | Pass | `(app)/layout.tsx` — только `getSession()` |
| BFF routes | Pass | assistant history/messages — один fetch на handler |

### Bundle size — Fix + Warn

| Проверка | Статус | Комментарий |
|----------|--------|-------------|
| `optimizePackageImports` | **Fix** | `next.config.ts` — lucide-react, recharts |
| Lazy heavy charts | **Fix** | `LeaderboardScatter` — `next/dynamic`, mount только на табе «Карта» |
| ActivityChart на dashboard | Warn | recharts нужен на первом экране diabetic — OK для MVP |
| Barrel imports lucide | Pass | named imports из `lucide-react` (tree-shake + optimize) |

### Re-render optimization — Pass + Warn

| Проверка | Статус | Комментарий |
|----------|--------|-------------|
| `AssistantChatProvider` callbacks | Pass | `useCallback` для load/send |
| Chat history effect | Pass | load только при `active && !loaded` |
| Context value object | Warn | новый object каждый render — OK при текущем размере дерева чата |

### Rendering — Fix

| Проверка | Статус | Комментарий |
|----------|--------|-------------|
| Recharts ResponsiveContainer sizing | **Fix** | `ChartContainer`: `min-w-0`, `min-h-[1px]`, explicit width/height 100% |

---

## 2. Next.js App Router Patterns

| Проверка | Статус | Комментарий |
|----------|--------|-------------|
| Server Components по умолчанию | Pass | pages — async RSC |
| `'use client'` только для интерактива | Pass | charts, chat, tabs, sidebar |
| `loading.tsx` | Pass | dashboard, leaderboard, chat |
| `error.tsx` | Pass | dashboard, leaderboard, chat |
| Auth redirect в layout/page | Pass | middleware + layout session guard |
| Client fetch чата | Warn | assistant — client BFF; оправдано для FAB + shared state MVP |

---

## 3. shadcn / UI consistency & a11y

| Проверка | Статус | Комментарий |
|----------|--------|-------------|
| Компоненты из `components/ui/` | Pass | Button, Card, Tabs, Sheet, Skeleton |
| FAB `aria-label` | Pass | «Открыть чат» |
| Chat errors `role="alert"` | Pass | `assistant-chat-panel.tsx` |
| Sheet title/description | Pass | FAB sheet |
| Logout button | Warn | текст «Выйти» — OK; можно добавить `type="button"` (implicit) |
| Mobile sidebar | Warn | backlog iter 2 — desktop-first nav |

---

## 4. Исправления iter 7

| Файл | Изменение |
|------|-----------|
| `web/components/ui/chart.tsx` | min dimensions + ResponsiveContainer props |
| `web/next.config.ts` | `experimental.optimizePackageImports` |
| `web/components/leaderboard/leaderboard-tabs.tsx` | controlled tab + dynamic scatter |

---

## 5. Backlog (Warn, не блокирует iter 8)

1. **Mobile nav** — hamburger / sheet sidebar (iter 2 backlog).
2. **Chat context memo** — `useMemo` для provider value при росте подписчиков.
3. **Dashboard chart code-split** — optional dynamic ActivityChart если bundle вырастет.
4. **Bundle analyzer** — `@next/bundle-analyzer` в CI (post-MVP).
5. **E2E smoke** — Playwright для login + routes (post-MVP).

---

## 6. Smoke checklist (user)

```bash
make db-reset && make backend-run   # :8000
make web-dev                         # :3000
```

| Маршрут | Проверка |
|---------|----------|
| `/login` | ivan_p / doctor_ivanov |
| `/dashboard` | KPI, chart без console warning width(-1) |
| `/leaderboard` | таблица; таб «Карта» — scatter загружается |
| `/chat` | история, send; FAB скрыт |
| FAB | send → `/chat` — та же история |

---

## 7. Toolchain

```bash
make web-lint   # eslint
make web-build  # next build
```

Оба — green после iter 7.
