install:
	uv venv
	uv sync

run:
	uv run python -m diaai.main

lint:
	uv run ruff check src backend tests scripts

format:
	uv run ruff format src backend tests scripts

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

.PHONY: db-up db-down db-reset db-migrate db-seed db-shell db-inspect

db-up:
	docker compose up -d
	@for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15; do \
		docker compose exec -T postgres pg_isready -U diaai -d diaai >/dev/null 2>&1 && exit 0; \
		sleep 1; \
	done; \
	echo "PostgreSQL did not become ready in time" >&2; exit 1

db-down:
	docker compose down

db-reset:
	docker compose down -v
	$(MAKE) db-up
	$(MAKE) db-migrate
	$(MAKE) db-seed

db-migrate: backend-migrate

db-seed:
	uv run python scripts/db/seed_from_progress.py

db-shell:
	docker compose exec postgres psql -U diaai -d diaai

db-inspect:
	uv run python scripts/db/db_inspect.py
