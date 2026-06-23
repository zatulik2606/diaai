# Task 07: Ревью качества frontend

Итерация: [iteration-7-quality-review](../../plan.md) · [tasklist-frontend.md](../../../../../tasklist-frontend.md)

**Статус:** ✅ Done · [summary](summary.md)

---

## Цель

Провести audit по skills; исправить критичные замечания; опубликовать `docs/tech/frontend-review.md`.

## Состав работ

### Audit

- [x] [vercel-react-best-practices](../../../../../../.agents/skills/vercel-react-best-practices/SKILL.md) — waterfalls, bundle, rerenders
- [x] [nextjs-app-router-patterns](../../../../../../.agents/skills/nextjs-app-router-patterns/SKILL.md) — RSC/client split, loading/error
- [x] [shadcn](../../../../../../.agents/skills/shadcn/SKILL.md) — consistency, a11y

### Fixes (критичные)

- [x] `ChartContainer` — min-w-0 / minHeight для ResponsiveContainer
- [x] `next.config.ts` — `optimizePackageImports` (lucide-react, recharts)
- [x] `leaderboard-tabs.tsx` — lazy scatter (`next/dynamic` + mount по табу)

### Закрытие

- [x] `docs/tech/frontend-review.md` — pass/warn/fix
- [x] `make web-lint && make web-build`
- [x] summary + tasklist 8/10

## Затронутые файлы

| Файл | Действие |
|------|----------|
| `web/components/ui/chart.tsx` | modify |
| `web/next.config.ts` | modify |
| `web/components/leaderboard/leaderboard-tabs.tsx` | modify |
| `docs/tech/frontend-review.md` | create |

## Проверка

```bash
make web-lint && make web-build
make backend-run && make web-dev
# smoke: /login, /dashboard, /leaderboard (table + scatter), /chat, FAB
```

## Definition of Done

- [x] Review doc без open Fix
- [x] lint + build green
- [x] tasklist iter 7 ✅
