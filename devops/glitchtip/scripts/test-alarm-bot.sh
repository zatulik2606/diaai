#!/usr/bin/env bash
# Verify @diaaialarm_bot token and optionally send a test message.
#
# Usage:
#   export TELEGRAM_ALARM_BOT_TOKEN=...
#   export TELEGRAM_ALARM_CHAT_ID=...   # optional; from getUpdates after /start
#   bash devops/glitchtip/scripts/test-alarm-bot.sh

set -euo pipefail

TOKEN="${TELEGRAM_ALARM_BOT_TOKEN:-}"
CHAT_ID="${TELEGRAM_ALARM_CHAT_ID:-}"
API="https://api.telegram.org/bot${TOKEN}"

if [[ -z "${TOKEN}" ]]; then
  echo "Set TELEGRAM_ALARM_BOT_TOKEN (see devops/glitchtip/alerts-telegram.md)" >&2
  exit 1
fi

echo "=== getMe ==="
ME=$(curl -sf "${API}/getMe")
echo "${ME}" | python3 -m json.tool
echo "${ME}" | python3 -c "import json,sys; r=json.load(sys.stdin)['result']; print(f\"Bot: @{r['username']} ({r['first_name']})\")"

echo ""
echo "=== getUpdates (last chats — need /start in @diaaialarm_bot) ==="
UPDATES=$(curl -sf "${API}/getUpdates?limit=5")
echo "${UPDATES}" | python3 -m json.tool

CHAT_FROM_UPDATES=$(echo "${UPDATES}" | python3 -c "
import json, sys
data = json.load(sys.stdin)
ids = []
for u in data.get('result', []):
    chat = u.get('message', {}).get('chat') or u.get('my_chat_member', {}).get('chat')
    if chat and chat.get('id'):
        ids.append((chat['id'], chat.get('username') or chat.get('first_name', '?')))
for cid, name in ids:
    print(f'  chat_id={cid} ({name})')
if not ids:
    print('  (empty — open https://t.me/diaaialarm_bot and press Start)')
" 2>/dev/null || true)
echo "${CHAT_FROM_UPDATES}"

if [[ -z "${CHAT_ID}" ]]; then
  echo ""
  echo "TELEGRAM_ALARM_CHAT_ID not set — skip sendMessage"
  echo "After /start, re-run with TELEGRAM_ALARM_CHAT_ID from getUpdates"
  exit 0
fi

echo ""
echo "=== sendMessage to chat_id=${CHAT_ID} ==="
TEXT="diaai GlitchTip alarm bot: test OK"
RESP=$(curl -sf -X POST "${API}/sendMessage" \
  -H "Content-Type: application/json" \
  -d "$(python3 -c "import json; print(json.dumps({'chat_id': '${CHAT_ID}', 'text': '''${TEXT}'''}))")")
echo "${RESP}" | python3 -m json.tool
echo "OK: message sent"
