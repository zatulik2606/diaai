# Итерация frontend 2: Summary

> **Статус:** ✅ Done

Опирается на [plan.md](plan.md) · [tasklist-frontend.md](../../../tasklist-frontend.md)

---

## Сделано

### Task-02: Каркас Next.js + layout + auth ✅

- Next.js 16.2.9 + React 19 + Tailwind 4 + shadcn (manual Radix)
- BFF auth: login/logout, httpOnly cookie `diaai_session`, middleware + role redirects
- App shell: sidebar, header, logout, FAB (Sheet-заглушка)
- Placeholder routes: `/dashboard`, `/leaderboard`, `/chat`
- Makefile `web-*`, env, README
- Детали: [task-02 summary](tasks/task-02-scaffold/summary.md)

| Компонент | Путь |
|-----------|------|
| Root layout + theme | `web/app/layout.tsx`, `web/app/globals.css` |
| Auth routes | `web/app/(auth)/login/page.tsx`, `(auth)/layout.tsx` |
| App shell | `web/app/(app)/layout.tsx`, `dashboard|leaderboard|chat/page.tsx` |
| BFF | `web/app/api/auth/login/route.ts`, `logout/route.ts` |
| Session + client | `web/lib/session.ts`, `web/lib/backend-client.ts`, `web/lib/types/auth.ts` |
| Middleware | `web/middleware.ts` |
| Shell components | `web/components/app-sidebar.tsx`, `app-header.tsx`, `chat-fab.tsx`, `logout-button.tsx` |
| shadcn ui | `web/components/ui/{button,card,input,label,avatar,separator,skeleton,sheet,table,chart}.tsx` |
| Tooling | `web/components.json`, `web/.env.example`, `Makefile` (`web-*`) |
| Docs | `web/README.md`, root `README.md`, `docs/integrations.md`, `.env.example` |

## Маршруты (live)

| Маршрут | Тип | Назначение |
|---------|-----|------------|
| `/login` | page | форма Telegram username |
| `/dashboard` | page | placeholder пациента (iter 3) |
| `/leaderboard` | page | placeholder доктора (iter 4) |
| `/chat` | page | placeholder чата (iter 5–6) |
| `POST /api/auth/login` | BFF | resolve → cookie |
| `POST /api/auth/logout` | BFF | clear cookie |

**Role matrix:** `diabetic` → Dashboard + Chat; `doctor` → Leaderboard + Chat. Cross-access редиректится middleware.

## Ценность

Runnable web на :3000 с login/logout, навигацией по роли и FAB — база для iter 3–6 без переделки каркаса.

## Отклонения от плана

| Отклонение | Причина |
|------------|---------|
| shadcn CLI init | network error; ручная установка Radix + компоненты |
| Mobile sidebar Sheet | desktop-only sidebar в iter 2; mobile nav — iter 7 |
| `pnpm-workspace.yaml` в `web/` | artifact create-next-app; не блокирует |
| Next.js middleware → proxy warning | 16.2.9 deprecation notice; функционально OK |

## Skills review

| Skill | Verdict |
|-------|---------|
| shadcn | ✅ semantic tokens, Sheet с title/description |
| vercel-react-best-practices | ✅ server layout, client только form/FAB/logout |
| nextjs-app-router-patterns | ✅ middleware matcher, route groups |

## Проверки (Self-check ✅)

| Проверка | Результат |
|----------|-----------|
| `make web-lint` | ✅ |
| `make web-build` | ✅ |
| `make web-dev` + login/logout | ✅ |
| `doctor_ivanov` → `/leaderboard` | ✅ |
| `ivan_p` → `/dashboard` | ✅ |
| doctor на `/dashboard` | ✅ 307 → leaderboard |
| FAB + dark theme tbench | ✅ |

## User-check

```bash
make db-reset && make backend-run   # :8000
cp web/.env.example web/.env.local  # BACKEND_SERVICE_TOKEN из корневого .env
make web-install && make web-dev    # :3000

# BFF smoke
curl -s -X POST http://localhost:3000/api/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"ivan_p"}' -c /tmp/diaai.cookie

curl -s -o /dev/null -w '%{http_code}\n' http://localhost:3000/dashboard -b /tmp/diaai.cookie
# → 200

curl -s -X POST http://localhost:3000/api/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"doctor_ivanov"}' -c /tmp/diaai-doctor.cookie

curl -s -o /dev/null -w '%{http_code}\n' http://localhost:3000/leaderboard -b /tmp/diaai-doctor.cookie
# → 200
```

Браузер: login `ivan_p` → dashboard, nav, FAB; `doctor_ivanov` → leaderboard; logout.

## Следующий шаг

[iteration-3-patient-dashboard](../iteration-3-patient-dashboard/plan.md) — панель пациента с диабетом (`/dashboard` + patient API).
