# Standard: Toolchain, Makefile Contract and Evidence Layout

Backs [`CHECKLIST.md`](../../CHECKLIST.md) §0.4, §1 and §5.

## Fixed conventions

| Concern | Convention |
|---------|------------|
| Language | Python ≥ 3.12, pinned per module in `.python-version` |
| Dependencies | [uv](https://github.com/astral-sh/uv). One `pyproject.toml` and `uv.lock` **per app**. No shared workspace (see [ADR 001](../adr/001-standalone-uv-project-per-module.md)). |
| Lint and format | ruff, configured once in the root `pyproject.toml` |
| Type checking | pyright, `typeCheckingMode = "basic"` minimum, configured in the module's `pyproject.toml` |
| Tests | pytest with `pytest-cov`; `tests/unit`, `tests/integration`, `tests/smoke` |
| CI | GitHub Actions, `.github/workflows/ci.yml`, one matrix entry per app |
| Secrets | gitleaks in pre-commit and CI. `.env` is never committed. |
| Task runner | `Makefile` per app exposing exactly the targets below |
| Docs | Markdown. Diagrams as Mermaid blocks inside Markdown. |

## Makefile contract

CI and reviewers call these by name. The names are part of the contract.

```makefile
.PHONY: setup up down test test-smoke lint typecheck eval bench clean

setup:       ## Install deps (uv sync --frozen) and download models/corpora
up:          ## Start the service and its dependencies
down:        ## Stop everything `up` started
test:        ## Unit + integration tests with coverage (--cov-fail-under=80)
test-smoke:  ## One request against the running service; exit non-zero on failure
lint:        ## ruff check . && ruff format --check .
typecheck:   ## pyright
eval:        ## Run the evaluation suite; exit non-zero below min_acceptable
bench:       ## Run the benchmark; write bench/results/<date>-<sha>.json and latest.json
clean:       ## Remove caches, build artifacts, downloaded models
```

A target that does not apply still exists, prints why, and exits 0:

```makefile
eval:
	@echo "N/A: see CHECKLIST.md 6.x"
```

## Root Makefile

The repo root has its own `Makefile` whose `ci` target runs lint, every app's
tests and the secret scan locally. It is the primary gate; GitHub Actions runs
the same targets when enabled. `make ci` must pass before a PR is opened.

## CI job shape

One job per target that gates merge, each running with
`working-directory: apps/<name>` and calling the target. CI never
re-implements what a target does.

```text
lint   typecheck   test   secrets   eval   cold-start
```

All must pass. `cold-start` is `make setup && make up && make test-smoke` on a
fresh `ubuntu-latest` runner.

## Evidence layout inside an app

```text
apps/<name>/
├── CHECKLIST.md          # Copy of docs/templates/CHECKLIST.md, filled in
├── README.md             # CHECKLIST §2
├── Makefile              # Contract above
├── .env.example          # If any env var exists
├── docs/
│   ├── architecture.md   # §3, Mermaid
│   ├── adr/              # §4, NNN-slug.md
│   ├── failure-modes.md  # §10
│   ├── cost-model.md     # §11
│   └── demo-script.md    # §12
├── evals/
│   ├── README.md         # Metric + methodology
│   ├── dataset.*         # Small, versioned, committed
│   ├── run_eval.py
│   ├── baseline.json
│   └── results/          # <sha>.json per run
├── bench/
│   ├── run_bench.py
│   └── results/          # <date>-<sha>.json + latest.json
└── tests/
    ├── unit/
    ├── integration/
    └── smoke/
```
