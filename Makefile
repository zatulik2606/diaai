install:
	uv venv
	uv sync

run:
	uv run python -m diaai.main

lint:
	uv run ruff check src backend tests

format:
	uv run ruff format src backend tests

test:
	uv run pytest backend/tests tests

backend-install:
	uv sync

backend-run:
	uv run uvicorn backend.main:app --host $${BACKEND_HOST:-127.0.0.1} --port $${BACKEND_PORT:-8000} --reload

backend-test:
	uv run pytest backend/tests

backend-lint:
	uv run ruff check backend

backend-format:
	uv run ruff format backend

backend-migrate:
	uv run alembic upgrade head

backend-openapi-export:
	curl -s http://$${BACKEND_HOST:-127.0.0.1}:$${BACKEND_PORT:-8000}/openapi.json | uv run python -m json.tool > docs/api/openapi.generated.json
