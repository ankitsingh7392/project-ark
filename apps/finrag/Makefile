# Per-app task runner. Target names are the contract in docs/standards/toolchain.md.
.PHONY: setup up down test test-smoke lint typecheck eval bench clean

setup:       ## Install deps (uv sync --frozen). Corpus download lands in a later milestone.
	uv sync --frozen --dev

up:          ## Start Postgres (pgvector) and the API
	docker compose up -d --build

down:        ## Stop everything `up` started
	docker compose down

test:        ## Unit + integration tests with coverage
	uv run pytest --cov=app --cov-fail-under=80

test-smoke:  ## One request against the running service
	curl -fsS http://localhost:8000/health

lint:        ## ruff check + format check (config in repo root)
	uvx ruff check . && uvx ruff format --check .

typecheck:   ## pyright
	uv run pyright

eval:        ## Validate the golden set and run the eval suite (baseline not recorded yet)
	uv run python -m evals.run_eval

bench:       ## N/A until there is a /query endpoint (CHECKLIST 8.2)
	@echo "N/A: no /query endpoint yet — see CHECKLIST.md 8.2"

clean:
	find . -type d \( -name __pycache__ -o -name .pytest_cache -o -name .ruff_cache \) -prune -exec rm -rf {} +
	rm -rf .venv
