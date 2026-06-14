# Task 02: Каркас Next.js + layout + auth

Итерация: [iteration-2-scaffold](../../plan.md)

**Статус:** 📋 Planned → 🚧 In Progress · [summary](summary.md)

---

## Цель

Завершить каркас `web/`: shadcn + tbench theme, BFF-auth, app shell, FAB, make-команды.

## Текущее состояние (baseline)

| Готово | Не готово |
|--------|-----------|
| Next.js 16.2.9, React 19, Tailwind 4, ESLint | shadcn, auth, shell, FAB |
| `app/layout.tsx`, `app/page.tsx` (default) | route groups, middleware |
| `.nvmrc`, `package.json` engines | Makefile `web-*`, `web/.env.example` |

## Порядок выполнения

### ✅ Фаза 0–1: Plan + Next.js init

- [x] Plan iter 2 + task 02
- [x] `pnpm create next-app` в `web/`; merge `diaai-web`, pnpm 11.6, `.nvmrc`

### 📋 Фаза 2: shadcn/ui + тема

```bash
cd web && pnpm dlx shadcn@latest init -y
pnpm dlx shadcn@latest add button card input table chart sheet avatar skeleton separator sidebar
```

**Fallback (CLI fail):**

```bash
pnpm add clsx tailwind-merge class-variance-authority lucide-react \
  @radix-ui/react-slot @radix-ui/react-dialog @radix-ui/react-avatar \
  @radix-ui/react-separator @radix-ui/react-label recharts
```

- `lib/utils.ts` — `cn()`
- `globals.css` — tokens из [frontend-design-system.md](../../../../../../spec/frontend-design-system.md):
  - `--background: 222 47% 6%`, `--primary: 142 76% 45%`, chart-1..5, `--radius: 0.5rem`
- `app/layout.tsx`: `<html className="dark">`, `Inter` + `JetBrains_Mono`, metadata `diaai`
- Удалить default welcome `page.tsx` content → redirect logic

### 📋 Фаза 3: Auth BFF + session

**Types** — `lib/types/auth.ts`:

```typescript
export type SessionUser = {
  user_id: string
  telegram_id: number | null
  role: string
  display_name: string | null
}
```

**`lib/backend-client.ts`** (server-only):

- `resolveUsername(username: string): Promise<SessionUser>`
- `POST ${BACKEND_URL}/api/v1/web/auth/resolve`
- Header: `Authorization: Bearer ${BACKEND_SERVICE_TOKEN}`
- Errors: 404 → user not found; network → service unavailable

**`lib/session.ts`:**

- Cookie name: `diaai_session`
- Options: `httpOnly`, `sameSite: 'lax'`, `path: '/'`, `maxAge: 7d`
- `getSession()`, `setSession()`, `clearSession()`

**Route Handlers:**

| Route | Method | Поведение |
|-------|--------|-----------|
| `/api/auth/login` | POST | `{ username }` → normalize → resolve → set cookie → `{ ok, role }` |
| `/api/auth/logout` | POST | clear cookie → `{ ok }` |

Normalize: `trim().replace(/^@/, '').toLowerCase()`

**`middleware.ts`:**

| Path | Правило |
|------|---------|
| `/login`, `/api/auth/*`, `/_next/*`, `/favicon.ico` | public |
| no session | redirect `/login` |
| session + `/login` | redirect: `diabetic` → `/dashboard`, `doctor` → `/leaderboard` |
| `doctor` + `/dashboard` | redirect `/leaderboard` |
| `diabetic` + `/leaderboard` | redirect `/dashboard` |

### 📋 Фаза 4: Login UI

`app/(auth)/login/page.tsx` — `"use client"`:

- Card centered (S11), Input, Button
- `fetch('/api/auth/login', { method: 'POST', body: JSON.stringify({ username }) })`
- Error state under form
- Hint: «Demo doctor: akozhin · patient: см. seed»

`app/(auth)/layout.tsx` — minimal, no sidebar.

### 📋 Фаза 5: App shell + FAB + placeholders

**`(app)/layout.tsx`** — server component:

- Read session → pass to `AppHeader`, `AppSidebar`
- Render `{children}` + `<ChatFab />`

**`components/app-sidebar.tsx`:**

- Links: Dashboard (`/dashboard`, patient only), Leaderboard (`/leaderboard`, doctor only), Chat (`/chat`)
- Desktop: fixed 240px; mobile: Sheet trigger

**`components/app-header.tsx`:**

- Logo «diaai», Avatar initials, display_name, logout button → POST `/api/auth/logout` → `/login`

**`components/chat-fab.tsx`** — client:

- Fixed bottom-right 1.5rem, 56×56, `rounded-full`, primary, `shadow-lg`
- Sheet: «Чат с ассистентом — iter 5»

**Placeholder pages** — Card + title:

| Route | Text |
|-------|------|
| `/dashboard` | Панель пациента с диабетом — iter 3 |
| `/leaderboard` | Лидерboard — iter 4 |
| `/chat` | Чат — iter 5–6 |

**`app/page.tsx`:** redirect по session (middleware может покрыть).

### 📋 Фаза 6: Makefile + env + docs

**Makefile:**

```makefile
.PHONY: web-install web-dev web-build web-lint

web-install:
	cd web && pnpm install

web-dev:
	cd web && pnpm dev

web-build:
	cd web && pnpm build

web-lint:
	cd web && pnpm lint
```

**`web/.env.example`:**

```
BACKEND_URL=http://127.0.0.1:8000
BACKEND_SERVICE_TOKEN=
```

**Docs:** `web/README.md`, root `README.md` (web section), `docs/integrations.md`, `.env.example`.

### 📋 Фаза 7: Проверки + summary

- Skills review: shadcn, vercel-react-best-practices, nextjs-app-router-patterns
- `summary.md` task-02 + iteration-2
- Обновить [tasklist-frontend.md](../../../../../tasklist-frontend.md): iter 2 ✅, 3/10

## Затронутые файлы

| Файл | Действие |
|------|----------|
| `web/app/(auth)/**` | create |
| `web/app/(app)/**` | create |
| `web/app/api/auth/**` | create |
| `web/app/layout.tsx`, `globals.css` | update |
| `web/app/page.tsx` | update → redirect |
| `web/components/**` | create |
| `web/lib/**` | create |
| `web/middleware.ts` | create |
| `web/components.json` | create |
| `web/.env.example` | create |
| `Makefile` | web-* targets |
| `README.md`, `docs/integrations.md`, `.env.example` | update |

## Проверки

```bash
make web-install && make web-lint && make web-build
make db-reset && make backend-run
make web-dev

# BFF smoke
curl -s -X POST http://localhost:3000/api/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"akozhin"}' -c /tmp/diaai.cookie

curl -s http://localhost:3000/dashboard -b /tmp/diaai.cookie -o /dev/null -w '%{http_code}'
```

## Demo credentials

| username | role | redirect |
|----------|------|----------|
| *(patient from seed)* | diabetic | `/dashboard` |
| `akozhin` | doctor | `/leaderboard` |

## Skills

| Skill | Checklist |
|-------|-----------|
| [shadcn](../../../../../../.agents/skills/shadcn/SKILL.md) | semantic colors, Sheet title, no raw color overrides |
| [vercel-react-best-practices](../../../../../../.agents/skills/vercel-react-best-practices/SKILL.md) | server layout, client only for form/FAB |
| [nextjs-app-router-patterns](../../../../../../.agents/skills/nextjs-app-router-patterns/SKILL.md) | middleware matcher, route groups |

## Definition of Done

**Агент:** `make web-dev` :3000; login/logout; nav; FAB; lint/build green.

**Пользователь:** localhost:3000 → `akozhin` → dashboard → menu → FAB → logout.
