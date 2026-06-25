#!/usr/bin/env bash
# Create diaai-backend + diaai-web on sentry.io (SaaS).
#
# 1. Sign up: https://sentry.io/signup/
# 2. Auth token: https://sentry.io/settings/account/api/auth-tokens/
#    Scopes: org:read, project:read, project:write, team:write
# 3. Run:
#      export SENTRY_AUTH_TOKEN=sntrys_...
#      export SENTRY_ORG=your-org-slug    # default: diaai
#      bash devops/sentry/scripts/create-projects-cloud.sh
#
# Output: devops/sentry/dsn.cloud.local.env (gitignored)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

export SENTRY_URL="${SENTRY_URL:-https://sentry.io}"
export OUT_FILE="${OUT_FILE:-${SCRIPT_DIR}/../dsn.cloud.local.env}"

exec "${SCRIPT_DIR}/create-projects.sh"
