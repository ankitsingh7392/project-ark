# Definition of Done

> An app under `apps/` is **done** when every applicable requirement
> below is satisfied **and a reviewer who did not build it can verify each one
> by running the listed command**, without asking the author anything.

This file lists *what must be true*. The detail behind each section lives in
[`docs/standards/`](docs/standards/). Files to copy live in
[`docs/templates/`](docs/templates/). The principles are in
[`CONSTITUTION.md`](CONSTITUTION.md).

Each requirement has:

| Field | Meaning |
|-------|---------|
| **ID** | Stable identifier (`3.2`). Reference it in commits, PRs and the app's `CHECKLIST.md`. |
| **Applies to** | Which project types must satisfy it. Others mark it `N/A` citing the rule. |
| **Produce** | The file, code or config that must exist, with its path. |
| **Verify** | A command a reviewer runs, and the output that proves it. |

If a requirement cannot be verified by a command, it is not a requirement here.

---

## 0. How to Work Through This

### 0.1 Classify the project first

Record the type at the top of the app's `CHECKLIST.md`. It drives every
"Applies to" column.

| Type | Definition | In this repo |
|------|------------|--------------|
| **ML-SVC** | Classical or statistical ML model served over an API or CLI. No external model provider. | `ats`, `lexiscan` |
| **LLM-SVC** | Calls a hosted or local LLM; prompts are part of the system. | — |
| **RAG** | LLM-SVC plus a retrieval layer. | — |
| **AGENT** | LLM-SVC that calls tools or takes multi-step actions. | — |

"All" means every type. `(ML-SVC: reduced)` means a lighter variant described
in the relevant standard.

### 0.2 Order of work

Each step makes the next cheaper. Do them in this order.

1. **§1 Cold start** — until it runs from a clean clone, nothing else can be verified.
2. **§5 Tests + CI** — the gate every later change passes through.
3. **§9 Security** — mostly config, and stops the rest leaking secrets.
4. **§6 Evaluation** — produces the quality number for §8.
5. **§7 Observability** — produces the latency numbers for §8 and the evidence for §10.
6. **§10 Failure behaviour** — uses §7's logging to prove each path.
7. **§8 Four Numbers** and **§11 Cost** — measure once the above is stable.
8. **§3 Architecture** and **§4 ADRs** — written last so they describe what was built.
9. **§2 README** — assembled from the artifacts above.
10. **§12 Demo** — recorded after the README is final.

### 0.3 Rules for the app's `CHECKLIST.md`

Copy [`docs/templates/CHECKLIST.md`](docs/templates/CHECKLIST.md) into the
project and keep the IDs.

* Status is one of `[x]`, `[ ]`, `[N/A]`.
* Every `[x]` is followed by **evidence**: the command run and the relevant
  output line, or the path to the artifact. Not a sentence saying it is done.
* Every `[N/A]` cites the **applicability rule** that excludes it, e.g.
  `N/A — no LLM provider (10.1)`. An `N/A` without a rule is a `[ ]`.
* **Never write a number that was not measured.** Unmeasured cells are `—` and the item is `[ ]`.
* **Never describe a file that does not exist.** Create it first.
* Never weaken a threshold to make a check pass. Record the real value and leave it `[ ]`.

### 0.4 Fixed conventions

Toolchain, the required `Makefile` targets and the evidence layout are fixed
across the repo and defined in
[`docs/standards/toolchain.md`](docs/standards/toolchain.md). CI and reviewers
call `make` targets by name, so the names are part of the contract.

---

## 1. Reproducible Cold Start

**Goal:** `git clone` → working service, with no step that exists only in the author's head.

| ID | Applies to | Requirement | Produce | Verify |
|----|-----------|-------------|---------|--------|
| 1.1 | All | Prerequisites listed with versions | README `## Quickstart` lists Python, uv, Docker (if used), OS packages | Nothing else was needed in 1.9 |
| 1.2 | All | Every environment variable documented | README table: name, required, default, meaning | `grep -rn "os.getenv\|os.environ" app/` — every name is in the table |
| 1.3 | Any with ≥ 1 env var | `.env.example` with placeholders only | `.env.example` in module root | `grep -E "=(.+)" .env.example` shows only obviously fake values |
| 1.4 | All | Reproducible install | `uv.lock` committed; `make setup` runs `uv sync --frozen` | `make setup` on a clean clone exits 0 |
| 1.5 | All | One-command start | `make up` | `make up && curl -fsS localhost:$PORT/health` exits 0 |
| 1.6 | Any with DB / vector store / queue | Dependencies start automatically | `docker-compose.yml`; `make up` starts them first | `docker compose ps` shows every dependency `healthy` |
| 1.7 | Any with DB | Migrations / init automated | Migration tool or `init.sql` run by `make up` | Fresh volume + `make up` → app serves requests |
| 1.8 | All | Health check | `GET /health` → `{status, model_loaded, version}`, or CLI `--version` | `make test-smoke` exits 0 |
| 1.9 | All | Cold start proven in CI | `cold-start` job: `make setup && make up && make test-smoke` on `ubuntu-latest` | Job green on the PR |

Large model files (the 3.6 GB Word2Vec vectors in `ats`, for example) are
downloaded by `make setup` to a git-ignored path, or a `MODEL_PATH` override is
documented. A reviewer never reads source to find out where the model goes.

---

## 2. README

**Goal:** a technical reviewer understands what the module does, how well, how
fast, at what cost and how it fails **before opening any source file**.

Use exactly these H2 headings in this order. No empty sections: write
`N/A — <rule>` under a heading that does not apply.

| # | Heading | Content | From |
|---|---------|---------|------|
| 1 | *(title + one-line tagline, badges)* | What it is, in one sentence | — |
| 2 | `## Demo` | Link plus a screenshot or short terminal capture. **Above the fold.** | §12 |
| 3 | `## Problem` | What is broken without this, and for whom | — |
| 4 | `## Solution` | Approach in ≤ 5 sentences | — |
| 5 | `## Architecture` | Mermaid diagram identical to `docs/architecture.md`, plus one paragraph of data flow | §3 |
| 6 | `## Results` | Four Numbers table, generated from `bench/results/latest.json` and `evals/baseline.json` | §8 |
| 7 | `## Quickstart` | Prerequisites, env vars, `make setup && make up`, smoke command | §1 |
| 8 | `## Usage` | One real request and response per endpoint or command | — |
| 9 | `## Evaluation` | Dataset, metric, methodology, `make eval` | §6 |
| 10 | `## Observability` | What is logged, where traces go, one real log line or trace | §7 |
| 11 | `## Failure behaviour` | Summary table from `docs/failure-modes.md` | §10 |
| 12 | `## Cost` | Summary from `docs/cost-model.md` | §11 |
| 13 | `## Security` | Controls in place | §9 |
| 14 | `## Limitations` | Honest list, at least 3 items | — |
| 15 | `## Decisions` | One line per ADR, linked | §4 |
| 16 | `## Project structure` | Tree with one comment per file | — |
| 17 | `## License` | — | — |

**Verify:** every heading above is present and non-empty.

---

## 3. Architecture

| ID | Applies to | Requirement | Produce | Verify |
|----|-----------|-------------|---------|--------|
| 3.1 | All | Diagram source committed | `docs/architecture.md` with a Mermaid block | Renders on GitHub |
| 3.2 | All | Container-level view | Every process, datastore, external system and the user as boxes | Each box maps to a directory, container or URL |
| 3.3 | All | Primary request data flow | Numbered arrows or a `sequenceDiagram` | A reviewer traces one request end to end |
| 3.4 | All | Model components explicit | Model, embeddings, vectoriser, LLM calls are their own boxes, labelled with artifact or provider | — |
| 3.5 | RAG, AGENT | Retrieval and tool boundaries | Vector store, index, each tool as separate boxes | — |
| 3.6 | Any with auth | Trust boundaries | Dashed boundary around the authenticated zone | — |
| 3.7 | All | README mirrors it | Same block in README `## Architecture` | `diff` of the two blocks is empty |

Not accepted: screenshots, slides, images without source. Template:
[`docs/templates/architecture.md`](docs/templates/architecture.md).

---

## 4. Architecture Decision Records

| ID | Applies to | Requirement | Produce | Verify |
|----|-----------|-------------|---------|--------|
| 4.1 | All | At least 3 ADRs | `docs/adr/NNN-slug.md`, zero-padded, never renumbered | `ls docs/adr/*.md \| wc -l` ≥ 3 |
| 4.2 | All | Template followed | Headings from [`docs/templates/adr.md`](docs/templates/adr.md) | `grep -L "## Alternatives" docs/adr/*.md` is empty |
| 4.3 | All | Rejected options named | ≥ 2 alternatives per ADR, each with the reason it lost | — |
| 4.4 | All | Linked from README `## Decisions` | — | Every file linked |

Mandatory topics for every module: model or algorithm choice; serving
interface; storage and model-artifact strategy. LLM-SVC, RAG and AGENT add:
provider choice; prompt and version management; retrieval strategy.

---

## 5. Automated Testing and CI

| ID | Applies to | Requirement | Produce | Verify |
|----|-----------|-------------|---------|--------|
| 5.1 | All | Unit tests | `tests/unit/`: no network, no model files, < 10 s | `uv run pytest tests/unit -q` passes |
| 5.2 | All | Integration tests | `tests/integration/`: real app in-process hitting every endpoint or command, with a small real model or a double on the same code path | `uv run pytest tests/integration -q` passes |
| 5.3 | All | Smoke test | `tests/smoke/`: one request against a running service at `$BASE_URL` | `make test-smoke` passes after `make up` |
| 5.4 | All | Lint | ruff, root config | `make lint` exits 0 |
| 5.5 | All | Type check | pyright `basic`, zero errors | `make typecheck` exits 0 |
| 5.6 | All | Coverage floor | `--cov-fail-under=80` on the package | `make test` prints the coverage line |
| 5.7 | All | CI matrix entry | Module in every applicable job of `.github/workflows/ci.yml` | Jobs appear on the PR |
| 5.8 | All | Branch protection | `main` requires `lint`, `typecheck`, `test`, `secrets`, `eval` | `gh api repos/:owner/:repo/branches/main/protection --jq .required_status_checks.contexts` |

CI jobs call the `make` target of the same name and never duplicate its logic.

---

## 6. Evaluation as a Merge Gate

**Goal:** a change to model, features, prompt, retrieval or thresholds cannot silently lower quality.

| ID | Applies to | Requirement | Produce | Verify |
|----|-----------|-------------|---------|--------|
| 6.1 | All | Evaluation dataset committed | `evals/dataset.*`, ≥ 100 labelled examples, disjoint from training data, with a `source` column | A test asserts no overlap with the training set |
| 6.2 | All | Metric defined | `evals/README.md`: metric, formula or library call, why this metric | — |
| 6.3 | All | Runner | `evals/run_eval.py` → `evals/results/<sha>.json` | `make eval` produces the file |
| 6.4 | All | Baseline recorded | `evals/baseline.json` per the schema in the standard | File exists |
| 6.5 | All | Regression threshold | `min_acceptable` in baseline; runner exits 1 below it | Lower the baseline temporarily: `make eval` fails |
| 6.6 | All | Runs in CI | `eval` job | Job appears on the PR |
| 6.7 | All | Reproducible | Fixed seed; identical value across two runs | Run twice; values equal to 4 dp |
| 6.8 | LLM-SVC, RAG, AGENT | Prompt or model changes trigger eval | CI `paths` filter includes `prompts/**`, `evals/**`, `app/**` | — |

Metrics by project type and the baseline schema:
[`docs/standards/evaluation.md`](docs/standards/evaluation.md). Raising the
baseline needs a PR with the new results file. Lowering `min_acceptable` needs an ADR.

---

## 7. Observability

| ID | Applies to | Requirement | Produce | Verify |
|----|-----------|-------------|---------|--------|
| 7.1 | All | Structured JSON logs | One JSON object per line on stdout | One request; the line parses with `jq .` |
| 7.2 | All (API) | Request ID | Middleware reads or generates `X-Request-ID`, echoes it, stamps every log line | `curl -i -H 'X-Request-ID: test-123' …`; header present; `jq 'select(.request_id=="test-123")'` finds ≥ 1 line |
| 7.3 | All | Per-request timing | `method`, `path`, `status`, `duration_ms` per request | Visible in 7.1 |
| 7.4 | All | Stage timing | `duration_ms` per stage (preprocess, embed, score, retrieve, llm_call, tool_call) | One request shows every stage |
| 7.5 | All (API) | Metrics endpoint | `GET /metrics` (Prometheus): request count, latency histogram, errors, model-load gauge | `curl localhost:$PORT/metrics \| grep http_request_duration` |
| 7.6 | All | Tracing | OpenTelemetry; OTLP exporter via `OTEL_EXPORTER_OTLP_ENDPOINT`, console when unset | `OTEL_TRACES_EXPORTER=console` prints a span tree |
| 7.7 | LLM-SVC, RAG, AGENT | Model calls observable | Span per call: `model`, `prompt_tokens`, `completion_tokens`, `latency_ms`, `cost_usd`; prompt hash, never full prompt | Attributes visible in 7.6 |
| 7.8 | RAG | Retrieval observable | Span per retrieval: `k`, `hits`, `top_score`, `latency_ms` | — |
| 7.9 | All | Errors with context | `request_id`, stage, exception type, stack at ERROR | Trigger a §10 failure; line contains all three |
| 7.10 | All | No sensitive data in logs | Request bodies never logged; lengths and hashes only | `grep -rn "resume_text\|jd_text\|text=" app/ \| grep -i log` is empty |
| 7.11 | All | README evidence | One real log line and one trace in README `## Observability` | — |

Detail and the ML-SVC reduced variant:
[`docs/standards/observability.md`](docs/standards/observability.md).

---

## 8. The Four Numbers

Published in README `## Results`, generated from committed artifacts, never typed by hand.

| Metric | Value | Conditions |
|--------|------:|------------|
| Quality (`<metric>`) | — | dataset sha, n |
| p50 latency | — ms | concurrency, requests, hardware |
| p95 latency | — ms | same |
| Throughput | — req/s | same |
| Cost per request | — | assumptions |

| ID | Applies to | Requirement | Produce | Verify |
|----|-----------|-------------|---------|--------|
| 8.1 | All | Quality from §6 | Read from `evals/baseline.json` | Values match |
| 8.2 | All | Benchmark runner | `bench/run_bench.py` → `bench/results/<date>-<sha>.json` and `latest.json` | `make bench` creates both |
| 8.3 | All | Methodology inside the result | `hardware`, `python`, `commit`, `concurrency`, `requests`, `warmup`, `payload_set_sha256` | All keys present |
| 8.4 | All | Cost from §11 | Read from `docs/cost-model.md` | Values match |
| 8.5 | All | Minimum load | `N=1000`, `C=10`; add `C=1` and `C=50` if latency-sensitive | — |
| 8.6 | All | README table generated | Script regenerates the table; README matches `latest.json` | No numeric drift |

Procedure and result schema:
[`docs/standards/benchmarking.md`](docs/standards/benchmarking.md). Laptop
numbers are acceptable when labelled as such.

---

## 9. Security Baseline

| ID | Applies to | Requirement | Produce | Verify |
|----|-----------|-------------|---------|--------|
| 9.1 | All | No secrets in history | gitleaks in pre-commit and CI | `gitleaks git --no-banner .` → 0 leaks |
| 9.2 | All | `.env` ignored | Root `.gitignore` | `git check-ignore .env` prints `.env` |
| 9.3 | All | `.env.example` placeholders only | — | 1.3 |
| 9.4 | All | Secret scanning and push protection on | Repo settings | `gh api repos/:owner/:repo --jq .security_and_analysis.secret_scanning_push_protection.status` → `enabled` |
| 9.5 | All | Dependency vulnerability scan | `pip-audit` CI job; Dependabot config | Job green; `.github/dependabot.yml` exists |
| 9.6 | All | Dependencies constrained | Pinned or upper-bounded; `uv.lock` committed | No unbounded `>=` in `pyproject.toml` |
| 9.7 | All | Input validation | Pydantic bounds on every request; CLI args validated | Oversize, empty, wrong-type input → 422 |
| 9.8 | All (API) | Request size limit | Default 1 MB | 2 MB body → 413 |
| 9.9 | All (API) | Rate limiting | Per-client limit, documented default | Burst above limit → 429 |
| 9.10 | Any non-local deployment | Authentication | API key or OIDC on every route except `/health`, `/metrics` | No credential → 401 |
| 9.11 | Any multi-tenant | Authorization | Tenant scoping tested | Cross-tenant → 403 |
| 9.12 | All | Sensitive data not logged | 7.10 | 7.10 |
| 9.13 | LLM-SVC, RAG, AGENT | Model output validated | Schema-parsed; retry once then 502 | Mocked malformed response test |
| 9.14 | AGENT | Tool permissions restricted | Allow-list per route; destructive tools need an explicit flag | Unlisted tool → rejected |
| 9.15 | LLM-SVC, RAG, AGENT | Prompt injection considered | `docs/security.md` lists vectors and mitigations; ≥ 3 adversarial eval cases | — |
| 9.16 | Any with Dockerfile | Container scan | `trivy image` in CI; no CRITICAL | Job green |
| 9.17 | Any with Dockerfile | Non-root container | `USER` directive | `docker run … id -u` ≠ 0 |

Scanner configuration and the local-only variant:
[`docs/standards/security.md`](docs/standards/security.md).

---

## 10. Failure Behaviour

**Goal:** every failure path was chosen, not discovered.

| ID | Applies to | Requirement | Produce | Verify |
|----|-----------|-------------|---------|--------|
| 10.1 | All | Failure table | `docs/failure-modes.md`: one row per applicable scenario from the standard, columns Failure / Detection / Response / User sees / Recovery / Test | Every applicable scenario present |
| 10.2 | All | Each row has a test | `tests/integration/test_failures.py` | `pytest -k failure -q` count equals rows |
| 10.3 | All | Timeouts tested | Mock sleeps past the timeout | Test asserts the timeout fires |
| 10.4 | All | Retries bounded and tested | Mock always fails | Exactly `max_retries + 1` calls |
| 10.5 | All | No generic 500 where a specific code applies | — | `grep -rn "HTTPException(500" app/` returns only the catch-all handler |
| 10.6 | All | Catch-all handler | 500 with `{"detail": "internal error", "request_id": …}`; stack trace only in logs | Response body contains no trace |
| 10.7 | All | README mirrors it | README `## Failure behaviour` is the table | — |

The scenario list with required behaviours:
[`docs/standards/failure-modes.md`](docs/standards/failure-modes.md). Template:
[`docs/templates/failure-modes.md`](docs/templates/failure-modes.md).

---

## 11. Cost Model

| ID | Applies to | Requirement | Produce |
|----|-----------|-------------|---------|
| 11.1 | All | Unit economics | `docs/cost-model.md`: per request, per 1k, per 1M per month, arithmetic shown |
| 11.2 | All | Drivers itemised | One row per applicable driver |
| 11.3 | All | Assumptions explicit | Instance and price with date, requests per day, utilisation |
| 11.4 | All | Biggest lever named | One paragraph with an estimate |
| 11.5 | LLM-SVC, RAG, AGENT | Token accounting | Mean tokens per request from the eval run × provider price |
| 11.6 | All | Linked to measurement | Throughput from §8 → instances at target load → compute cost |

Worked example and template:
[`docs/standards/cost-model.md`](docs/standards/cost-model.md),
[`docs/templates/cost-model.md`](docs/templates/cost-model.md).

---

## 12. Demonstrable System

| ID | Applies to | Requirement | Produce | Verify |
|----|-----------|-------------|---------|--------|
| 12.1 | All | ≤ 3-minute demo | Screen recording link, or `docs/demo.cast` (asciinema) | Link resolves; ≤ 3:30 |
| 12.2 | All | Above the fold | README `## Demo` is the first H2 after the badges | — |
| 12.3 | All | Shows the real system | `make up`, one real request, one real response | — |
| 12.4 | All | Covers architecture, results, one failure | `docs/demo-script.md` with timestamps | — |
| 12.5 | All | Reproducible | Every demo command is in the script and works on `main` | Reviewer replays it |

---

## Final Gate

An app is **done** when its `CHECKLIST.md` shows every section as `[x]` or a
justified `[N/A]`, and each command below passes on `main`.

| § | Gate | One-command verification |
|---|------|--------------------------|
| 1 | Cold start | `make setup && make up && make test-smoke` on a clean clone |
| 2 | README | All headings present, none empty |
| 3 | Architecture | `docs/architecture.md` renders; README copy identical |
| 4 | ADRs | ≥ 3 files, template headings present |
| 5 | Tests + CI | `make lint && make typecheck && make test`; all jobs required on `main` |
| 6 | Evaluation | `make eval` exits 0; lowered baseline makes it exit 1 |
| 7 | Observability | JSON log with `request_id`; `/metrics` serves; console trace prints |
| 8 | Four Numbers | `bench/results/latest.json` exists; README table matches |
| 9 | Security | gitleaks 0, pip-audit clean, 422/413/429 tests pass |
| 10 | Failure modes | `pytest -k failure` count equals table rows |
| 11 | Cost | `docs/cost-model.md` shows the arithmetic |
| 12 | Demo | Link resolves, ≤ 3:30, script replays |

---

## Reviewer Protocol

The reviewer did not build the app and does not talk to the author.

1. Clone fresh into an empty directory. Run the §1 command. Stop if it fails.
2. Read the README top to bottom. Note every question it did not answer.
3. Open the app's `CHECKLIST.md`. For each `[x]`, run its evidence command. Any mismatch becomes `[ ]`.
4. For each `[N/A]`, confirm the cited rule actually excludes it.
5. Run the Final Gate table.
6. The verdict is **Done** only if steps 1, 3, 4 and 5 produced zero findings.

> **Build it. Test it. Measure it. Observe it. Secure it. Document it. Prove it.**
> If a stranger cannot verify it with a command, it is not done.
