# Frontend Design System

Опирается на [frontend-requirements.md](frontend-requirements.md) · [vision.md](../vision.md)

**Статус:** iter 0 ✅ — tokens и guidelines для iter 2 (Next.js + shadcn/ui).

**Визуальный ориентир:** [tbench.ai](https://www.tbench.ai/) — тёмная dev-эстетика, высокий контраст, моноширинные акценты для метрик и KPI.

---

## Стилевые требования (обязательные)

| # | Требование | Значение / правило | Зоны |
|---|------------|-------------------|------|
| S1 | Тема | **только dark** на MVP; переключателя light нет | все |
| S2 | Фон приложения | `--background` (`222 47% 6%`) | все |
| S3 | Акцент / CTA | `--primary` tbench-green (`142 76% 45%`) | FAB, кнопки, active nav |
| S4 | KPI и числа | `--font-mono`, `text-3xl` value, `text-sm` delta | зона 1 |
| S5 | Карточки | `--card`, border `1px solid hsl(var(--border))`, `border-radius: var(--radius)`, `p-6` | зона 1 |
| S6 | Графики | `--chart-1` primary, `--chart-2` secondary; подписи осей `--muted-foreground` | зона 1 |
| S7 | Медали топ-3 | gold `#FFD700`, silver `#C0C0C0`, bronze `#CD7F32` | зона 2 |
| S8 | Progress bar | track `hsl(var(--muted))`, fill `hsl(var(--primary))`, height 8px | зона 2 |
| S9 | FAB чат | 56×56px, `rounded-full`, `shadow-lg`, fixed bottom-right 1.5rem | зона 3 |
| S10 | Heatmap ячейки | шкала 0–33 / 34–66 / 67–100 → см. § Heatmap | зона 4 |
| S11 | Login | центрированная Card на `--background`, Input `--input` border | auth |
| S12 | Контраст текста | WCAG AA ≥ 4.5:1 `--foreground` на `--background` | все |
| S13 | Focus | ring 2px `hsl(var(--ring))` на focus-visible | все |

---

## Принципы

1. **Dark-first** — единственная тема на MVP; light mode — backlog
2. **Data-dense** — dashboard показывает много информации без clutter; whitespace через `--muted` surfaces
3. **Dev aesthetic** — monospace для чисел/KPI; sans для текста
4. **shadcn/ui** — компоненты из Radix + Tailwind; кастомизация через CSS variables

---

## Design tokens

Значения для `globals.css` (iter 2). Формат: HSL без `hsl()` для shadcn compatibility.

### Base

| Token | HSL | Назначение |
|-------|-----|------------|
| `--background` | `222 47% 6%` | page background (#0a0e17 approx) |
| `--foreground` | `210 40% 96%` | primary text |
| `--card` | `222 47% 9%` | card/panel surface |
| `--card-foreground` | `210 40% 96%` | text on card |
| `--popover` | `222 47% 9%` | dropdowns, chat widget |
| `--popover-foreground` | `210 40% 96%` | |
| `--muted` | `217 33% 14%` | secondary surfaces |
| `--muted-foreground` | `215 20% 55%` | secondary text |
| `--border` | `217 33% 18%` | borders, dividers |
| `--input` | `217 33% 18%` | input borders |
| `--ring` | `142 76% 45%` | focus ring (accent green) |

### Accent

| Token | HSL | Назначение |
|-------|-----|------------|
| `--primary` | `142 76% 45%` | CTA, FAB, active nav (tbench green) |
| `--primary-foreground` | `222 47% 6%` | text on primary |
| `--secondary` | `217 33% 14%` | secondary buttons |
| `--secondary-foreground` | `210 40% 96%` | |
| `--accent` | `217 33% 18%` | hover states |
| `--accent-foreground` | `210 40% 96%` | |
| `--destructive` | `0 72% 51%` | errors |
| `--destructive-foreground` | `210 40% 96%` | |

### Charts (recharts / shadcn chart)

| Token | HSL | Series |
|-------|-----|--------|
| `--chart-1` | `142 76% 45%` | primary line (activity) |
| `--chart-2` | `199 89% 48%` | secondary line |
| `--chart-3` | `262 83% 58%` | tertiary |
| `--chart-4` | `32 95% 55%` | warnings |
| `--chart-5` | `340 75% 55%` | highlights |

### Typography

| Token | Value | Usage |
|-------|-------|-------|
| `--font-sans` | `Inter, system-ui, sans-serif` | UI text, tables |
| `--font-mono` | `JetBrains Mono, ui-monospace, monospace` | KPI values, ranks, codes |

### Typography scale

| Token / class | Size | Usage |
|---------------|------|-------|
| `text-3xl` | 30px | KPI values |
| `text-xl` | 20px | section headings |
| `text-base` | 16px | body, table cells |
| `text-sm` | 14px | delta, labels, timestamps |
| `text-xs` | 12px | badges, chart axis |

### Spacing

| Token | Value | Usage |
|-------|-------|-------|
| page padding | `p-6` / `1.5rem` | main content |
| card gap | `gap-4` / `1rem` | KPI grid |
| section gap | `gap-6` / `1.5rem` | dashboard blocks |
| FAB offset | `1.5rem` | from viewport edge |

---

## Компоненты (shadcn iter 2)

| Компонент | Экран | Примечание |
|-----------|-------|------------|
| `Button` | global | primary = FAB, CTA |
| `Card` | dashboard KPI | с delta badge |
| `Table` | questions, leaderboard | sticky header |
| `Tabs` | leaderboard toggle | Table / Scatter |
| `Badge` | metrics icons | ХЕ, БЖЕ, insulin |
| `Chart` | activity, scatter | recharts wrapper |
| `Dialog` / `Sheet` | FAB chat | bottom-right sheet preferred |
| `Skeleton` | loading states | KPI, chart, table |
| `Input` | login username | monospace optional |
| `Avatar` | header user | initials from display_name |
| `Progress` | leaderboard bar | shadcn Progress |
| `Tooltip` | matrix cells | date + metrics |

### FAB (глобальный чат)

```css
/* Guideline — iter 2 implementation */
.fab-chat {
  position: fixed;
  bottom: 1.5rem;
  right: 1.5rem;
  z-index: 50;
  /* primary button, rounded-full, shadow-lg */
}
```

---

## Layout

### App shell (iter 2)

```
┌──────────────────────────────────────────┐
│ Sidebar (240px) │ Main content           │
│ · Dashboard     │                        │
│ · Leaderboard   │                        │
│ · Chat          │                        │
│                 │                        │
│ [user footer]   │                        │
└──────────────────────────────────────────┘
```

- Sidebar collapsible на mobile → Sheet
- Header: breadcrumb optional; user menu + logout

### Breakpoints (Tailwind default)

| Breakpoint | Layout |
|------------|--------|
| `< md` | single column; matrix scroll horizontal |
| `md+` | 2-column dashboard grid |
| `lg+` | full wireframe layout |

---

## Accessibility

- Конtrast ratio ≥ **4.5:1** для `--foreground` на `--background` (WCAG AA)
- Focus visible: `--ring` 2px on interactive elements
- Chart: не только цвет — подписи осей, table fallback для leaderboard
- FAB: `aria-label="Open assistant chat"`; keyboard Esc closes widget

---

## Heatmap / matrix colors

| Score range | Token usage |
|-------------|-------------|
| 0–33% | `--muted` + low opacity primary |
| 34–66% | `--chart-2` at 50% |
| 67–100% | `--primary` at 80% |

Tooltip: `--popover` background, `--foreground` text.

---

## Связанные документы

| Документ | Назначение |
|----------|------------|
| [frontend-requirements.md](frontend-requirements.md) | функциональные блоки |
| [tasklist-frontend.md](../tasks/tasklist-frontend.md) iter 2 | scaffold + shadcn init |
