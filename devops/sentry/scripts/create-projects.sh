#!/usr/bin/env bash
# Create diaai-backend + diaai-web in Sentry (self-hosted or sentry.io).
#
# Auth token: Settings → Account → Auth Tokens
#   self-hosted: http://HOST:9000/settings/account/api/auth-tokens/
#   cloud:       https://sentry.io/settings/account/api/auth-tokens/
# Scopes (User Auth Token — Personal Tokens):
#   Minimum: org:read, project:read, project:write
#   If 403 on create: add org:write and team:write (or create projects in UI)
#
# Self-hosted:
#   export SENTRY_URL=http://127.0.0.1:9000
#   export SENTRY_AUTH_TOKEN=sntrys_...
#   bash devops/sentry/scripts/create-projects.sh
#
# sentry.io (cloud):
#   export SENTRY_AUTH_TOKEN=sntrys_...
#   export SENTRY_ORG=your-org-slug
#   bash devops/sentry/scripts/create-projects-cloud.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SENTRY_URL="${SENTRY_URL:-http://127.0.0.1:9000}"
SENTRY_ORG="${SENTRY_ORG:-diaai}"
SENTRY_TEAM="${SENTRY_TEAM:-diaai}"
BACKEND_PROJECT="${BACKEND_PROJECT:-diaai-backend}"
WEB_PROJECT="${WEB_PROJECT:-diaai-web}"
OUT_FILE="${OUT_FILE:-${SCRIPT_DIR}/../dsn.local.env}"

if [[ -z "${SENTRY_AUTH_TOKEN:-}" ]]; then
  echo "Set SENTRY_AUTH_TOKEN" >&2
  echo "  cloud: https://sentry.io/settings/account/api/auth-tokens/" >&2
  echo "  self-hosted: \${SENTRY_URL}/settings/account/api/auth-tokens/" >&2
  exit 1
fi

api() {
  local method=$1 path=$2
  shift 2
  local url="${SENTRY_URL%/}/api/0${path}"
  curl -sf -X "$method" \
    -H "Authorization: Bearer ${SENTRY_AUTH_TOKEN}" \
    -H "Content-Type: application/json" \
    "${url}" "$@"
}

api_or_fail() {
  local method=$1 path=$2
  shift 2
  local body http_code
  body=$(curl -s -w "\n%{http_code}" -X "$method" \
    -H "Authorization: Bearer ${SENTRY_AUTH_TOKEN}" \
    -H "Content-Type: application/json" \
    "${SENTRY_URL%/}/api/0${path}" "$@")
  http_code=$(echo "$body" | tail -1)
  body=$(echo "$body" | sed '$d')
  if [[ "$http_code" -ge 400 ]]; then
    echo "API ${method} ${path} → HTTP ${http_code}" >&2
    echo "$body" >&2
    if [[ "$http_code" == "401" || "$http_code" == "403" ]]; then
      echo "" >&2
      echo "403/401 hints:" >&2
      echo "  1. Token: User Settings → Auth Tokens (NOT Internal Integration unless org-bound)" >&2
      echo "  2. Scopes: org:read, project:write (+ org:write if org disables member project creation)" >&2
      echo "  3. Org: Settings → General → enable 'Let Members Create Projects'" >&2
      echo "  4. Role: Owner/Manager in org, or create projects manually in UI" >&2
      echo "  5. SENTRY_ORG must match org slug (script lists orgs on verify failure)" >&2
    fi
    exit 1
  fi
  echo "$body"
}

list_orgs() {
  echo "Available organizations:" >&2
  api_or_fail GET "/organizations/" | python3 -c "
import json, sys
for o in json.load(sys.stdin):
    print(f\"  - {o.get('slug')} ({o.get('name')})\")
"
}

verify_org() {
  if api GET "/organizations/${SENTRY_ORG}/" >/dev/null 2>&1; then
    return 0
  fi
  echo "Organization '${SENTRY_ORG}' not found on ${SENTRY_URL}" >&2
  list_orgs || true
  echo "Set SENTRY_ORG to your org slug and retry" >&2
  exit 1
}

ensure_team() {
  if [[ -n "${SKIP_TEAM_CREATE:-}" ]]; then
    return 0
  fi
  if api GET "/teams/${SENTRY_ORG}/${SENTRY_TEAM}/" >/dev/null 2>&1; then
    echo "Team ${SENTRY_ORG}/${SENTRY_TEAM} exists"
    return
  fi
  echo "Creating team ${SENTRY_TEAM}..."
  api_or_fail POST "/teams/${SENTRY_ORG}/" \
    -d "{\"name\":\"${SENTRY_TEAM}\",\"slug\":\"${SENTRY_TEAM}\"}" >/dev/null
}

create_project_org() {
  local slug=$1 platform=$2
  local body http_code
  body=$(curl -s -w "\n%{http_code}" -X POST \
    -H "Authorization: Bearer ${SENTRY_AUTH_TOKEN}" \
    -H "Content-Type: application/json" \
    "${SENTRY_URL%/}/api/0/organizations/${SENTRY_ORG}/projects/" \
    -d "{\"name\":\"${slug}\",\"slug\":\"${slug}\",\"platform\":\"${platform}\"}")
  http_code=$(echo "$body" | tail -1)
  body=$(echo "$body" | sed '$d')
  if [[ "$http_code" -ge 400 ]]; then
    echo "Org project create ${slug} → HTTP ${http_code}" >&2
    echo "$body" >&2
    return 1
  fi
  echo "Created project ${slug} (org API)"
  return 0
}

create_project_team() {
  local slug=$1 platform=$2
  echo "Creating project ${slug} via team ${SENTRY_TEAM} (${platform})..."
  api_or_fail POST "/teams/${SENTRY_ORG}/${SENTRY_TEAM}/projects/" \
    -d "{\"name\":\"${slug}\",\"slug\":\"${slug}\",\"platform\":\"${platform}\"}" >/dev/null
}

ensure_project() {
  local slug=$1 platform=$2
  if api GET "/projects/${SENTRY_ORG}/${slug}/" >/dev/null 2>&1; then
    echo "Project ${slug} exists"
    return
  fi
  if is_cloud; then
    if ! create_project_org "${slug}" "${platform}"; then
      ensure_team
      create_project_team "${slug}" "${platform}"
    fi
  else
    ensure_team
    create_project_team "${slug}" "${platform}"
  fi
}

project_dsn() {
  local slug=$1
  api_or_fail GET "/projects/${SENTRY_ORG}/${slug}/keys/" | python3 -c "
import json, sys
keys = json.load(sys.stdin)
for k in keys:
    dsn = k.get('dsn') or {}
    if k.get('isActive') and dsn.get('public'):
        print(dsn['public'])
        break
else:
    if keys:
        dsn = keys[0].get('dsn') or {}
        print(dsn.get('public', ''))
"
}

is_cloud() {
  [[ "${SENTRY_URL}" == *"sentry.io"* ]]
}

echo "Sentry: ${SENTRY_URL}"
echo "Organization: ${SENTRY_ORG}"

verify_org
ensure_project "${BACKEND_PROJECT}" "python-fastapi"
ensure_project "${WEB_PROJECT}" "javascript-nextjs"

BACKEND_DSN=$(project_dsn "${BACKEND_PROJECT}")
WEB_DSN=$(project_dsn "${WEB_PROJECT}")

if [[ -z "$BACKEND_DSN" || -z "$WEB_DSN" ]]; then
  echo "Failed to read DSN from API" >&2
  exit 1
fi

CLOUD_NOTE=""
if is_cloud; then
  CLOUD_NOTE="# sentry.io cloud — DSN host is ingest.*.sentry.io
"
fi

cat >"${OUT_FILE}" <<EOF
# Generated by create-projects.sh — do not commit
${CLOUD_NOTE}SENTRY_URL=${SENTRY_URL}
SENTRY_ENVIRONMENT=development
SENTRY_TRACES_SAMPLE_RATE=0.1
SENTRY_ORG=${SENTRY_ORG}

# diaai-backend (FastAPI) → root .env
SENTRY_DSN=${BACKEND_DSN}

# diaai-web (Next.js)
WEB_SENTRY_DSN=${WEB_DSN}
NEXT_PUBLIC_SENTRY_DSN=${WEB_DSN}
EOF

chmod 600 "${OUT_FILE}"

echo ""
echo "DSN saved to ${OUT_FILE}"
echo ""
echo "Backend (FastAPI):  SENTRY_DSN=${BACKEND_DSN}"
echo "Web (Next.js):      NEXT_PUBLIC_SENTRY_DSN=${WEB_DSN}"
echo ""
echo "Root .env:"
echo "  SENTRY_DSN=${BACKEND_DSN}"
echo "  WEB_SENTRY_DSN=${WEB_DSN}"
echo "  NEXT_PUBLIC_SENTRY_DSN=${WEB_DSN}"
if is_cloud; then
  echo "  SENTRY_URL=https://sentry.io"
  echo "  SENTRY_ORG=${SENTRY_ORG}"
  echo "  SENTRY_PROJECT=diaai-web"
fi
echo ""
echo "web/.env.local (pnpm dev):"
echo "  SENTRY_DSN=${WEB_DSN}"
echo "  NEXT_PUBLIC_SENTRY_DSN=${WEB_DSN}"
