# Итерация frontend 2: Summary

> **Статус:** 🚧 In Progress

Опирается на [plan.md](plan.md) · [tasklist-frontend.md](../../../tasklist-frontend.md)

---

## Сделано

### Task-02: Каркас Next.js + layout + auth 🚧

- **Планирование:** полный plan iter 2 + task 02; архитектура BFF, структура `web/`, DoD, риски
- **Частичный scaffold:** Next.js 16 + React 19 + Tailwind 4 в `web/` (default template)
- Toolchain сохранён: `diaai-web`, pnpm 11.6, Node ≥20, `.nvmrc` → 24
- Детали: [task-02 summary](tasks/task-02-scaffold/summary.md)

| Артефакт | Путь | Статус |
|----------|------|--------|
| Plan iter 2 | [iteration-2-scaffold/plan.md](plan.md) | ✅ |
| Plan task 02 | [tasks/task-02-scaffold/plan.md](tasks/task-02-scaffold/plan.md) | ✅ |
| Next.js app (default) | `web/app/`, `web/package.json` | 🚧 partial |
| shadcn + theme | `web/components/ui/` | 📋 |
| Auth BFF + session | `web/app/api/auth/`, `web/lib/` | 📋 |
| App shell + FAB | `web/components/`, routes | 📋 |
| Make web-* | `Makefile` | 📋 |

## Ценность (по завершении iter 2)

Runnable web на :3000 с login/logout, навигацией и FAB — база для iter 3–6 без переделки каркаса.

## Отклонения от плана

| Отклонение | Комментарий |
|------------|-------------|
| Iter 2 не закрыт | реализация прервана после `create next-app` |
| shadcn через CLI | network failure; план — manual install |
| Default Next.js welcome page | заменится на diaai shell в продолжении task 02 |

## Skills review

| Skill | Verdict |
|-------|---------|
| shadcn | ⏳ pending — init не выполнен |
| vercel-react-best-practices | ⏳ pending — после AppShell |
| nextjs-app-router-patterns | ⏳ pending — после middleware/routes |

## Проверки (Self-check)

| Проверка | Результат |
|----------|-----------|
| Plan-артефакты | ✅ |
| `pnpm create next-app` в `web/` | ✅ partial |
| `make web-dev` + login/logout | ❌ |
| `make web-lint && make web-build` | ❌ |
| FAB + dark theme tbench | ❌ |

## User-check

Пока **не применимо** — DoD iter 2 не выполнен.

После завершения:

```bash
make db-reset && make backend-run   # :8000
make web-install && make web-dev      # :3000
# login: akozhin → /dashboard; nav; FAB; logout
```

## Следующий шаг

Продолжить [task-02](tasks/task-02-scaffold/plan.md): shadcn → auth BFF → AppShell → Makefile → DoD → ✅ Done.
