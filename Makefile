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
	docker compose up -d postgres
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

.PHONY: web-install web-dev web-build web-lint

web-install:
	cd web && pnpm install

web-dev:
	cd web && pnpm dev

web-build:
	cd web && pnpm build

web-lint:
	cd web && pnpm lint

.PHONY: stack-up stack-down stack-ps stack-logs stack-logs-tail stack-health stack-init stack-up-registry stack-pull-registry stack-up-registry-bot stack-pull-registry-bot

GHCR_REGISTRY ?= ghcr.io
GHCR_OWNER ?= zatulik2606
IMAGE_TAG ?= main
DIAAI_BACKEND_IMAGE = $(GHCR_REGISTRY)/$(GHCR_OWNER)/diaai-backend:$(IMAGE_TAG)
DIAAI_WEB_IMAGE = $(GHCR_REGISTRY)/$(GHCR_OWNER)/diaai-web:$(IMAGE_TAG)
DIAAI_BOT_IMAGE = $(GHCR_REGISTRY)/$(GHCR_OWNER)/diaai-bot:$(IMAGE_TAG)

stack-up:
	COMPOSE_PROFILES=build docker compose up -d --build

stack-up-bot:
	COMPOSE_PROFILES=build,bot docker compose up -d --build

stack-up-registry:
	COMPOSE_PROFILES=registry \
	DIAAI_BACKEND_IMAGE=$(DIAAI_BACKEND_IMAGE) \
	DIAAI_WEB_IMAGE=$(DIAAI_WEB_IMAGE) \
	docker compose up -d --no-build --pull missing

stack-pull-registry:
	COMPOSE_PROFILES=registry \
	DIAAI_BACKEND_IMAGE=$(DIAAI_BACKEND_IMAGE) \
	DIAAI_WEB_IMAGE=$(DIAAI_WEB_IMAGE) \
	docker compose pull backend web

stack-up-registry-bot:
	COMPOSE_PROFILES=registry,bot \
	DIAAI_BACKEND_IMAGE=$(DIAAI_BACKEND_IMAGE) \
	DIAAI_WEB_IMAGE=$(DIAAI_WEB_IMAGE) \
	DIAAI_BOT_IMAGE=$(DIAAI_BOT_IMAGE) \
	docker compose up -d --no-build --pull missing

stack-pull-registry-bot:
	COMPOSE_PROFILES=registry,bot \
	DIAAI_BACKEND_IMAGE=$(DIAAI_BACKEND_IMAGE) \
	DIAAI_WEB_IMAGE=$(DIAAI_WEB_IMAGE) \
	DIAAI_BOT_IMAGE=$(DIAAI_BOT_IMAGE) \
	docker compose pull backend web bot

stack-down:
	docker compose --profile build --profile registry --profile bot down

stack-ps:
	docker compose --profile build --profile registry --profile bot ps

stack-logs:
	@if [ -n "$(SVC)" ]; then docker compose --profile build --profile registry --profile bot logs -f $(SVC); else docker compose --profile build --profile registry --profile bot logs -f; fi

stack-logs-tail:
	@if [ -n "$(SVC)" ]; then docker compose --profile build --profile registry --profile bot logs --tail=100 $(SVC); else docker compose --profile build --profile registry --profile bot logs --tail=100; fi

stack-health:
	@echo "Checking postgres..."
	@docker compose exec -T postgres pg_isready -U diaai -d diaai >/dev/null 2>&1 || (echo "FAIL: postgres" >&2; exit 1)
	@echo "OK: postgres"
	@echo "Checking backend /health..."
	@curl -sf http://127.0.0.1:8000/health >/dev/null || (echo "FAIL: backend http://127.0.0.1:8000/health" >&2; exit 1)
	@echo "OK: backend"
	@echo "Checking web :3000..."
	@curl -sf -o /dev/null http://127.0.0.1:3000/ || (echo "FAIL: web http://127.0.0.1:3000/" >&2; exit 1)
	@echo "OK: web"
	@echo "stack-health: all checks passed"

stack-init:
	$(MAKE) db-reset
	$(MAKE) stack-up
