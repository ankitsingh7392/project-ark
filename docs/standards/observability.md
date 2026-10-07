# Standard: Observability

Backs [`CHECKLIST.md`](../../CHECKLIST.md) §7.

## The questions it must answer

For any single request, using telemetry alone:

* Why was it slow, and which stage took the time?
* Why did it fail, and in which component?
* Which external provider or dependency was involved?
* What did it cost?

## Logging

* `structlog` with a JSON renderer, or stdlib `logging` with a JSON formatter. One object per line on stdout. No multi-line logs.
* Mandatory fields on every line: `timestamp`, `level`, `event`, `request_id`, `module`.
* One line per request at INFO with `method`, `path`, `status`, `duration_ms`.
* One line per internal stage at DEBUG with `stage` and `duration_ms`. Stage names are fixed per project and documented in the README.
* Exceptions at ERROR with `exc_type`, `stage`, and the stack trace in `exception`.
* **Never log request bodies.** Log `input_chars` or `input_sha256` instead. Verify with the grep in CHECKLIST 7.10.

Example line a reviewer should be able to produce:

```json
{"timestamp":"2026-10-07T12:00:00Z","level":"info","event":"request","request_id":"test-123","method":"POST","path":"/match","status":200,"duration_ms":41.7,"stages":{"preprocess":3.2,"embed":30.1,"skills":6.9}}
```

## Request ID

Middleware that:

1. Reads `X-Request-ID` from the request, or generates a UUID4.
2. Binds it to the logging context for the duration of the request.
3. Echoes it in the response header `X-Request-ID`.
4. Includes it in every error response body.

## Metrics

`GET /metrics` in Prometheus exposition format. Minimum series:

| Series | Type | Labels |
|--------|------|--------|
| `http_requests_total` | counter | `method`, `path`, `status` |
| `http_request_duration_seconds` | histogram | `method`, `path` |
| `stage_duration_seconds` | histogram | `stage` |
| `model_loaded` | gauge | — |
| `errors_total` | counter | `stage`, `exc_type` |

`prometheus-fastapi-instrumentator` covers the first two for FastAPI apps.

## Tracing

* OpenTelemetry SDK with the FastAPI auto-instrumentation.
* Exporter chosen by environment: OTLP when `OTEL_EXPORTER_OTLP_ENDPOINT` is set, console otherwise. No collector is required for local verification.
* One span per stage, named with the stage name. Attributes mirror the log fields.
* LLM-SVC, RAG, AGENT: one span per model call with `model`, `prompt_tokens`, `completion_tokens`, `latency_ms`, `cost_usd`, `prompt_sha256`. One span per retrieval with `k`, `hits`, `top_score`. One span per tool call with `tool`, `ok`.

## ML-SVC reduced variant

For a module with no external provider and no retrieval:

* 7.6 may use the console exporter only.
* 7.7 and 7.8 are `N/A — no provider / no retrieval`.
* Everything else applies in full. Stage timing is still required because the
  interesting latency question for an ML-SVC is "was it preprocessing or the model?"

## README evidence

`## Observability` in the module README contains one real request log line, the
list of stage names, and either a console trace excerpt or a screenshot of a
trace in a backend.
