#!/usr/bin/env bash
# postToolUse: suggest docs-updater when API-related files change.
# Requires: python3
set -euo pipefail

input=$(cat)

python3 -c "
import json, re, sys

data = json.load(sys.stdin)
tool = data.get('tool_name', '') or data.get('tool', '')
payload = data.get('tool_input') or data.get('arguments') or {}

# Collect candidate paths from common Cursor hook shapes
paths = []
for key in ('path', 'file_path', 'target_file', 'filePath'):
    v = payload.get(key)
    if isinstance(v, str):
        paths.append(v)

command = payload.get('command') or ''
if isinstance(command, str) and command:
    paths.append(command)

text_blob = json.dumps(payload, ensure_ascii=False)

PATTERNS = (
    r'backend/api/',
    r'backend/schemas/',
    r'backend/config\.py',
    r'web/app/api/',
    r'alembic/versions/',
    r'src/diaai/backend_client\.py',
    r'prompts/',
    r'\.env\.example',
    r'web/\.env\.example',
)

def matches(p: str) -> bool:
    p = p.replace('\\\\', '/')
    return any(re.search(pat, p) for pat in PATTERNS)

hit = any(matches(p) for p in paths) or any(re.search(pat, text_blob) for pat in PATTERNS)

if not hit:
    sys.exit(0)

msg = (
    'Изменён код, влияющий на API/контракты или onboarding. '
    'Запусти subagent **docs-updater** (/.cursor/agents/docs-updater.md): '
    'синхронизируй docs/tech/api-contracts.md, docs/api/*, '
    'при необходимости docs/onboarding.md и docs/smoke-test.md. '
    'Сверься с docs/doc-audit.md.'
)
print(json.dumps({'additional_context': msg}, ensure_ascii=False))
" 2>/dev/null || true

exit 0
