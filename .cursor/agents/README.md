# Project subagents (diaai)

Custom subagents для Cursor. Формат: `.md` с YAML frontmatter + system prompt.

| Agent | Назначение | Вызов |
|-------|------------|------|
| [docs-updater.md](docs-updater.md) | синхронизация docs после изменений API/BFF/env | `/docs-updater` или авто через hook |

## docs-updater

**Триггер (авто):** `.cursor/hooks.json` → `postToolUse` после правок в `backend/api/`, `backend/schemas/`, `web/app/api/`, migrations, prompts.

**Ручной вызов:**

```text
/docs-updater синхронизируй docs после последних изменений в backend/api/
```

Правила поддержки docs: [docs/doc-audit.md](../../docs/doc-audit.md).
