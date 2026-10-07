# Standard: Failure Behaviour

Backs [`CHECKLIST.md`](../../CHECKLIST.md) §10.

## Principle

Every failure path is chosen, documented and tested. "It returns a 500" is a
finding, not a design.

## Scenarios and required behaviour

A module's `docs/failure-modes.md` has one row for each scenario below that
applies to its project type, plus any scenario specific to the module.

| ID | Applies to | Scenario | Required behaviour |
|----|-----------|----------|--------------------|
| F1 | LLM-SVC, RAG, AGENT | Provider outage | Timeout at the documented value; 1 retry with backoff; then 503 with `Retry-After` |
| F2 | LLM-SVC, RAG, AGENT | Provider rate limit (429) | Honour `Retry-After`; at most 3 retries; then 503 |
| F3 | LLM-SVC, RAG, AGENT | Provider timeout | As F1; partial results are never returned as complete |
| F4 | RAG | Empty retrieval | Explicit "no supporting documents" response; never generate from nothing |
| F5 | All | Malformed input | 422 with field-level errors; CLI prints usage and exits 2 |
| F6 | All | Oversize input | 413 (API) or a clear error (CLI) before any processing |
| F7 | LLM-SVC, RAG, AGENT | Invalid model output | Schema validation; retry once; then 502 |
| F8 | AGENT | Tool failure | Error returned to the model once; step budget enforced; then the task fails with its trace |
| F9 | Any with DB | Database down | `/health` reports `db: down`; requests fail fast with 503; no unbounded reconnect loop |
| F10 | RAG | Vector store down | As F9 |
| F11 | All | Model artifact missing or corrupt | Service starts degraded; `/health` reports `model_loaded: false`; model routes return 503 |
| F12 | All | Dependency missing at import | Error names the package and the `make setup` step that installs it |
| F13 | All | Unhandled exception | Logged with `request_id` and stack; response is 500 `{"detail": "internal error", "request_id": …}` with no trace in the body |

## Table format

```markdown
| Failure | Detection | System response | User sees | Recovery | Test |
|---------|-----------|-----------------|-----------|----------|------|
| F11 Model file missing at start | `Path.exists()` in lifespan | Start anyway, `model_loaded=false` | `/health` → `model_loaded: false`; `/match` → 503 | Mount model, restart | `test_missing_model_returns_503` |
```

The **Test** column names a test in `tests/integration/test_failures.py`. The
count of rows equals the count of tests collected by `pytest -k failure`.

## Timeouts and retries

* Every outbound call has an explicit timeout. The value is a named constant or
  env var, documented in the README env-var table.
* Every retry has a maximum and a backoff. A test with a mock that always fails
  asserts the call count is exactly `max_retries + 1`.
* A test with a mock that sleeps past the timeout asserts the timeout fires and
  the documented error is returned.
