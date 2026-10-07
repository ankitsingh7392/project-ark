# Standard: Security Baseline

Backs [`CHECKLIST.md`](../../CHECKLIST.md) §9.

## Principle

Security is checked by automation, not remembered during review. Every control
below has either a CI job or a test.

## Scanners

| Control | Tool | Where | Fails on |
|---------|------|-------|----------|
| Secrets in commits | gitleaks | pre-commit + CI `secrets` job | Any finding |
| Secrets in pushes | GitHub push protection | Repo settings | Any finding |
| Vulnerable dependencies | `pip-audit` against `uv export --frozen` | CI `audit` job | Any known CVE with a fix available |
| Outdated dependencies | Dependabot | `.github/dependabot.yml`, weekly | Opens PRs |
| Container vulnerabilities | `trivy image` | CI, modules with a Dockerfile | CRITICAL |
| Static analysis | `ruff` security rules (`S` ruleset) | CI `lint` job | Any finding |

## Dependency constraints

Runtime dependencies are pinned (`==`) or upper-bounded below the next major.
`uv.lock` is committed and CI installs with `--frozen`. An unbounded `>=` is a
lint failure.

## Input handling

* Every API request body is a Pydantic model with explicit `min_length`, `max_length` and type on each field.
* A request-size limit (default 1 MB) is enforced before parsing. Over-limit → 413.
* Rate limiting per client IP or API key (default 60 requests per minute). Over-limit → 429 with `Retry-After`.
* CLI arguments are validated by `argparse` types and explicit checks; bad input → usage message and exit 2.

Each of these has a test in `tests/integration`.

## Authentication and authorization

Required on any deployment beyond localhost:

* API key via `X-API-Key` header or OIDC bearer token, on every route except `/health` and `/metrics`.
* Keys are compared in constant time and never logged.
* Multi-tenant systems scope every query by tenant and test that cross-tenant access returns 403.

**Local-only variant:** 9.10 and 9.11 may be `N/A — not deployed beyond
localhost` only when an ADR records that decision and the README `## Security`
section states it.

## Containers

* `USER` directive; the process runs as non-root.
* Read-only root filesystem where the app allows it; writable volume for the model mount only.
* No secrets in the image. Configuration via environment at runtime.

## AI-specific controls (LLM-SVC, RAG, AGENT)

* Model output is parsed against a schema before use. Invalid output → one retry → 502. Raw output is never returned to the caller.
* Tools are allow-listed per route. Destructive tools (write, delete, send, pay) require an explicit `confirm=true` and are logged at INFO with the actor.
* `docs/security.md` in the module lists prompt-injection vectors considered (user input, retrieved content, tool results) and the mitigation for each.
* The evaluation dataset contains at least 3 adversarial cases tagged `injection`, and the eval reports the pass rate on that slice.

## What not to log

Request bodies, prompts, retrieved documents, API keys, tokens, user identifiers
beyond a request-scoped ID. Lengths and hashes are fine. CHECKLIST 7.10 is the
check.
