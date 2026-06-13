install:
	uv venv
	uv sync

run:
	uv run python -m diaai.main

lint:
	uv run ruff check src backend

format:
	uv run ruff format src backend

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
