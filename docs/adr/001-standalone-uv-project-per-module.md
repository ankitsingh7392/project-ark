# 001. Each module is a standalone uv project with its own lockfile

- **Status:** Accepted
- **Date:** 2026-06-22

## Context

The repository holds several independent ML services. They share a toolchain
(ruff, pytest, GitHub Actions) but not runtime dependencies: `ats` needs gensim,
NLTK and FastAPI; `lexiscan` needs only scikit-learn and pandas. A single shared
environment would force every module to carry every other module's
dependencies, and a version bump for one service would risk breaking another.

## Decision

We will give each module under `apps/` its own `pyproject.toml`,
`uv.lock` and `.python-version`. The root `pyproject.toml` holds only shared
tooling configuration (ruff) and declares no dependencies. CI runs one matrix
job per module, each doing `uv sync --frozen` in that module's directory.

## Alternatives

| Option | Why rejected |
|--------|--------------|
| One root environment with all dependencies | Every module inherits every other module's install time, image size and upgrade risk. A gensim upgrade should not be able to break a Naïve Bayes classifier. |
| uv workspace with shared lockfile | Resolves one version of each package across all members, so two modules cannot pin different versions of the same library. Also couples their release cadence. |
| Separate repositories per module | Loses the shared CI, pre-commit and standards, and the single place a reviewer can see all the work. The modules are small enough that one repo is the simpler choice. |

## Consequences

**Positive:** modules are independently installable, testable and
containerisable. Dependency changes are scoped to one directory and one CI job.
A reviewer can `cd` into any module and run it without understanding the rest.

**Negative, debt accepted:** shared code would have to be duplicated or
published as a package; there is none yet. Each module repeats a few lines of
pytest and pyright configuration.

**Revisit when:** two modules need the same non-trivial shared code, or the
module count makes per-module CI jobs slower than a single workspace job.
