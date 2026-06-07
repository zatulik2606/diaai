install:
	uv venv
	uv sync

run:
	uv run python -m diaai.main

lint:
	uv run ruff check

format:
	uv run ruff format
