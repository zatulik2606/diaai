# Frontend UI — функциональные требования

Опирается на [user-scenarios.md](user-scenarios.md) · [data-requirements.md](data-requirements.md) · [data-model.md](../data-model.md) · [frontend-contract.md](../api/frontend-contract.md) · [frontend-design-system.md](frontend-design-system.md)

**Статус:** iter 0 ✅ — спецификация для реализации iter 2–6.

---

## Обзор

Web-клиент (`web/`) — тонкий клиент backend REST API. MVP фокус: **роль пациента с диабетом** (`/dashboard`, FAB, D1/D3); **роль доктора** — leaderboard (D3) и post-MVP когорта (Doc1–Doc2).

### Маппинг UI → домен diaai

| # | Зона UI (исходное ТЗ) | Маршрут / размещение | Роль | Сценарии | API (см. [frontend-contract.md](../api/frontend-contract.md)) |
|---|------------------------|----------------------|------|----------|------------------------------------------------------------------|
| 1 | Панель → **панель пациента с диабетом** | `/dashboard` | diabetic | D1, D3 | patient dashboard API *(iter 3; gap: iter 1 — `/doctor/dashboard/*`)* |
| 2 | **Лидерboard** | `/leaderboard` | doctor | D3 | `GET …/leaderboard` |
| 3 | **Глобальный чат** (FAB) | overlay на всех страницах | doctor, diabetic | D2 | `GET …/assistant/history`, `POST /api/v1/assistant/messages` |
| 4 | Периоды × метрики | блок на `/dashboard` | diabetic | D3 | progress matrix *(patient-scoped)* |

Терминология в UI: **доктор** (не «преподаватель»), **пациент с диабетом** (не «диабетик»), **пациенты** в контексте доктора, **периоды/метрики** (не «уроки»).

**Стиль:** единая тёмная тема по [frontend-design-system.md](frontend-design-system.md) — обязательна для всех четырёх зон.

### Роли и доступ

| Роль | MVP экраны | Post-MVP |
|------|------------|----------|
| `diabetic` | `/dashboard`, FAB chat | D4–D6 (рекомендации, консультации) |
| `doctor` | `/leaderboard`, FAB chat | Doc1–Doc4 (когорта, консультации) |

---

## Зона 4 — Матрица прогресса (блок на `/dashboard`)

**Цель (D3):** личный прогресс пациента с диабетом: периоды × метрики (ХЕ, БЖЕ, инсулин).

Отдельная функциональная зона UI; физически — правый нижний блок dashboard пациента.

### Wireframe (блок)

```
┌─────────────────────────────────────────┐
│ Progress matrix          [week ▼]       │
├──────────┬──────┬──────┬──────┬─────────┤
│ Metric   │ W22  │ W23  │ W24  │ W25     │
├──────────┼──────┼──────┼──────┼─────────┤
│ ХЕ       │ 72██ │ 85██ │ 60██ │  —      │
│ БЖЕ      │ 90██ │ 88██ │ 92██ │ 95██    │
└──────────┴──────┴──────┴──────┴─────────┘
  hover → дата snapshot + xe/bje/insulin
```

### Поведение

- **Строки:** метрики (`xe`, `bje`, `insulin`) или периоды — query `columns`
- **Столбцы:** периоды (`week`, `month`) для **текущего пользователя**
- **Ячейка:** `score` / `completion_pct` (0–100); цвет по шкале из design system
- **Tooltip (hover):** `snapshot_date`, значения метрик
- **Empty:** «Нет snapshots за период»
- **API:** patient-scoped progress matrix *(iter 3; см. gap в frontend-contract)*

### Стиль (обязательно)

- Таблица/heatmap на `--card`, границы `--border`
- Цвет ячеек: см. [frontend-design-system.md § Heatmap](frontend-design-system.md#heatmap--matrix-colors)
- Шрифт значений в ячейках: `--font-mono`, `text-sm`
- Горизонтальный scroll на `< md`

---

## Экран 1 — Панель пациента с диабетом (`/dashboard`) — зона 1

**Цель (D1 + D3):** личная аналитика: KPI, активность, свои вопросы ассистенту, фиксации, матрица прогресса.

### Стиль (обязательно)

- Фон страницы: `--background`; карточки KPI: `--card`, border `--border`, padding `1.5rem`
- KPI value: `--font-mono`, `text-3xl`, `--foreground`; delta badge: `text-sm`, green/red по `trend`
- Chart: серии `--chart-1`, `--chart-2`; сетка `--border` 20% opacity
- Таблицы: sticky header `--card`, zebra optional через `--muted/50`
- См. [frontend-design-system.md](frontend-design-system.md)

### Wireframe (блоки)

```
┌─────────────────────────────────────────────────────────────────┐
│ Header: logo · nav (Dashboard | Leaderboard | Chat) · user · ⎋  │
├─────────────────────────────────────────────────────────────────┤
│ [KPI 1]      [KPI 2]      [KPI 3]      [KPI 4]                  │
│  Δ vs prev    Δ vs prev    Δ vs prev    Δ vs prev               │
├──────────────────────────────┬──────────────────────────────────┤
│ Activity chart (14 days)     │ Recent questions (table)         │
│ line: requests + food_events │ time · Q · A                     │
├──────────────────────────────┼──────────────────────────────────┤
│ Recent submissions (list)    │ Progress matrix (heatmap/table)  │
│ click → detail link          │ rows=metrics · cols=periods      │
└──────────────────────────────┴──────────────────────────────────┘
                                                      [FAB chat 💬]
```

### 4 KPI с дельтой

Сравнение текущего 7-дневного окна с предыдущим 7-дневным.

| KPI | Описание | Источник PG |
|-----|----------|-------------|
| Сумма ХЕ за 7д | личный агрегат | `food_events.xe` (filter `user_id`) |
| Вопросов за 7д | запросы к ассистенту | `dialog_requests` |
| Событий питания за 7д | записи в дневник | `food_events` |
| Инсулин за 7д | сумма доз | `insulin_events` |

Каждая карточка: `value`, `delta` (число и %), `trend` (`up` | `down` | `flat`).

### График активности (14 дней)

- Тип: line chart (dual series или stacked area)
- Ось X: календарные дни
- Серии: `requests_count`, `food_events_count` по дням
- Источник: агрегат по **текущему** `user_id` / `telegram_id`

### Таблица вопросов

| Колонка | Поле API |
|---------|----------|
| Время | `created_at` |
| Вопрос | `content` |
| Ответ | `reply` |

Сортировка по `created_at` desc. Пагинация: `limit`/`offset`.

### Лента «сдач» → события фиксации

Маппинг «сдачи уроков» → **фиксации в дневнике** (food event или photo analysis).

| Элемент | Содержание | Действие по клику |
|---------|------------|-------------------|
| Food event | описание, ХЕ/БЖЕ, время | ссылка на деталь события |
| Photo analysis | превью, confidence, ХЕ | ссылка на D7-деталь |

Источник: `food_events`, `photo_analyses` (последние N **текущего пользователя**).

### Матрица прогресса

См. **Зона 4** — отдельная секция выше; на dashboard рендерится как вложенный блок.

### UI states

| State | Поведение |
|-------|-----------|
| Loading | skeleton для KPI, chart, tables |
| Empty | «Нет данных за период» + подсказка про seed |
| Error | сообщение + retry; код из ErrorBody |

---

## Экран 2 — Лидерboard (`/leaderboard`) — зона 2

**Цель:** рейтинг прогресса пациентов с диабетом по выбранной метрике и периоду.

### Стиль (обязательно)

- Tabs Table/Scatter: `--muted` inactive, `--primary` active indicator
- Медали топ-3: gold `#FFD700`, silver `#C0C0C0`, bronze `#CD7F32` (иконки или badge)
- Progress bar: track `--muted`, fill `--primary`
- См. [frontend-design-system.md](frontend-design-system.md)

### Wireframe

```
┌─────────────────────────────────────────────────────────────────┐
│ Header                                                          │
├─────────────────────────────────────────────────────────────────┤
│ Period: [30d ▼]   Metric: [xe ▼]    [ Table | Scatter ]         │
├─────────────────────────────────────────────────────────────────┤
│ TABLE MODE:                                                     │
│ # │ Patient      │ ████████░░ 72% │ 🍞 💉 │ badges             │
│ 🥇│ ...          │ ...            │ ...   │                    │
├─────────────────────────────────────────────────────────────────┤
│ SCATTER MODE:                                                   │
│     Y (metric_y)                                                │
│        ·  ·                                                     │
│           ·    ·                                                │
│     ───────────── X (metric_x)                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Режим «Таблица»

| Колонка | Описание |
|---------|----------|
| Rank | место; топ-3 — медали 🥇🥈🥉 |
| Patient | `display_name` |
| Progress | progress bar (% к цели периода) |
| Metrics | иконки: ХЕ / БЖЕ / insulin (badges) |

### Режим «Scatter plot»

- Query: `metric_x`, `metric_y` (`xe`, `bje`, `insulin_dose`, `activity_score`)
- Точка: `{ patient_id, display_name, x, y }`
- Hover tooltip: имя + значения осей

### UI states

Loading, empty (нет пациентов), error — аналогично dashboard.

---

## Глобальный чат (FAB) — зона 3

**Сценарий:** D2 — диалог с ассистентом.

### Стиль (обязательно)

- FAB: `--primary` фон, `rounded-full`, `shadow-lg`, размер 56×56px, иконка `--primary-foreground`
- Виджет: `--popover` фон, ширина 380px (desktop), full-width Sheet на mobile
- Сообщения user: `--muted`; assistant: `--card`; timestamp `--muted-foreground` `text-xs`
- См. [frontend-design-system.md](frontend-design-system.md)

### Поведение

- **FAB** (floating action button) — bottom-right на всех authenticated-страницах
- Клик → виджет чата (Dialog/Sheet): история сообщений + input
- Отправка текста → `POST /api/v1/assistant/messages`
- История → `GET /api/v1/web/assistant/history`
- Фото в чате — **iter 5+** (post-MVP для FAB)

### Содержание сообщения

| Поле | Источник |
|------|----------|
| role | `user` / `assistant` |
| text | `content` / `reply` |
| timestamp | `created_at` |

Для пациента с диабетом: `telegram_id` из сессии. Для доктора в MVP: чат от своего `telegram_id` (demo) или read-only просмотр — **iter 5** уточняет UX.

---

## Вход (MVP auth)

Без OAuth/JWT на MVP.

### Flow

1. Страница `/login`: поле «Telegram @username» (без `@` или с — нормализовать)
2. Next.js Route Handler (BFF) → `POST /api/v1/web/auth/resolve` с Bearer `BACKEND_SERVICE_TOKEN`
3. Backend резолвит username → `user_id`, `telegram_id`, `role`, `display_name`
4. Сессия в cookie / localStorage (iter 2): `{ user_id, telegram_id, role, display_name }`
5. Redirect: `diabetic` → `/dashboard`; `doctor` → `/leaderboard`

### Demo doctor (seed iter 1)

| Поле | Значение |
|------|----------|
| username | `akozhin` |
| telegram_id | `162684825` |
| role | `doctor` |

### Open question → iter 1

В таблице `users` **нет** колонки `telegram_username`. MVP-резолв:

- seed-map username → `telegram_id` в backend
- или match по `display_name` (case-insensitive)
- или миграция `003` + колонка `telegram_username`

Решение фиксируется в iter 1 summary.

### Безопасность

- `BACKEND_SERVICE_TOKEN` **не** попадает в браузер — только на сервере Next (BFF)
- Клиент передаёт username; backend проверяет существование пользователя

---

## Сверка UI → сценарии → сущности

| UI-блок | Сценарий | Read entities | Write |
|---------|----------|---------------|-------|
| KPI cards | Doc1 | User, FoodEvent, DialogRequest | — |
| Activity chart | Doc1 | FoodEvent, DialogRequest | — |
| Questions table | Doc2, D2 | DialogRequest, User | — |
| Submissions feed | D1, D7 | FoodEvent, PhotoAnalysis | — |
| Progress matrix | Doc2, D3 | ProgressSnapshot, User | — |
| Leaderboard | D3 | ProgressSnapshot, FoodEvent, InsulinEvent | — |
| FAB chat | D2 | Dialog, DialogRequest | Dialog, Request (via API) |
| Login | — | User | — |

---

## Out of scope (iter 0–6)

- D5/D6 консультации (запись, история) — отдельные итерации
- JWT, RBAC, OAuth
- Голосовой режим — iter 8
- Text-to-SQL — iter 9
- Diabetic dashboard D3–D4 — post-MVP web screens

---

## Связанные документы

| Документ | Назначение |
|----------|------------|
| [frontend-design-system.md](frontend-design-system.md) | тема, tokens, компоненты |
| [frontend-contract.md](../api/frontend-contract.md) | REST endpoint'ы и JSON |
| [tasklist-frontend.md](../tasks/tasklist-frontend.md) | план реализации |
