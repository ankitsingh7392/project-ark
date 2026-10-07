# Failure Modes — <module>

Scenario IDs refer to [`docs/standards/failure-modes.md`](../../docs/standards/failure-modes.md).
Every row names a test in `tests/integration/test_failures.py`.

| Failure | Detection | System response | User sees | Recovery | Test |
|---------|-----------|-----------------|-----------|----------|------|
| F5 Malformed input | Pydantic validation | Reject before processing | 422 with field errors | Fix the request | `test_malformed_input_422` |
| F6 Oversize input | Size middleware | Reject before parsing | 413 | Reduce the payload | `test_oversize_input_413` |
| F11 Model artifact missing | `Path.exists()` at startup | Start degraded | `/health` → `model_loaded: false`; model routes → 503 | Mount the artifact, restart | `test_missing_model_503` |
| F13 Unhandled exception | Catch-all handler | Log with request_id + stack | 500 `{"detail":"internal error","request_id":…}` | Investigate by request_id | `test_unhandled_exception_500` |

## Timeouts

| Call | Timeout | Env var | Test |
|------|---------|---------|------|
| ... | ... | ... | ... |

## Retries

| Call | Max retries | Backoff | Test |
|------|-------------|---------|------|
| ... | ... | ... | ... |
