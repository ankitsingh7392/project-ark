# Local CI. Runs the same checks as .github/workflows/ci.yml without using
# Actions minutes. `make ci` before every pull request.

APPS := apps/ats apps/lexiscan

# Tests are model-free; this path makes the ATS matcher skip loading the
# multi-GB Word2Vec vectors, exactly as CI does.
export W2V_MODEL_PATH ?= /nonexistent

.PHONY: ci lint format test secrets hooks clean help

help: ## Show targets
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-10s %s\n", $$1, $$2}'

ci: lint test secrets ## Everything CI runs: lint, tests for every app, secret scan
	@echo "ci: all checks passed"

lint: ## ruff check + ruff format --check (repo-wide)
	uvx ruff check .
	uvx ruff format --check .

format: ## Apply ruff fixes and formatting
	uvx ruff check --fix .
	uvx ruff format .

test: ## uv sync + pytest in every app
	@for app in $(APPS); do \
		echo "==> $$app"; \
		(cd $$app && uv sync --frozen --dev --quiet && uv run pytest -q) || exit 1; \
	done

secrets: ## gitleaks over the full git history (same hook as pre-commit)
	uvx pre-commit run gitleaks --all-files

hooks: ## Install the pre-commit hooks into .git/hooks (one-time)
	uvx pre-commit install

clean: ## Remove caches and virtualenvs
	find . -type d \( -name __pycache__ -o -name .pytest_cache -o -name .ruff_cache \) -prune -exec rm -rf {} +
	@for app in $(APPS); do rm -rf $$app/.venv; done
