#!/bin/sh
set -e
cd /app
if [ "$1" = "uv" ]; then
  exec "$@"
fi
/app/.venv/bin/alembic upgrade head
exec /app/.venv/bin/uvicorn backend.main:app --host 0.0.0.0 --port 8000
