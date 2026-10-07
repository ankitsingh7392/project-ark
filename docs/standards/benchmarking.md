# Standard: Benchmarking

Backs [`CHECKLIST.md`](../../CHECKLIST.md) §8.

## Principle

A number without its measurement conditions is not a result. Instead of
"latency: 200 ms", publish "p95 420 ms, 10 concurrent, 1,000 requests, 4 vCPU
laptop". Every result file carries its own methodology.

## Procedure

`bench/run_bench.py`:

1. Loads a committed payload set (`bench/payloads.jsonl`) and prints its sha256. Payloads are realistic in size and shape; do not benchmark with a 20-character input if real inputs are 2,000 characters.
2. Waits for `GET /health` to report the model loaded.
3. Warms up with 50 requests, discarded.
4. Sends `N` requests at concurrency `C`, cycling through the payload set. Default `N=1000`, `C=10`. Add `C=1` and `C=50` runs if the service is latency-sensitive.
5. Records every request's wall-clock latency and status.
6. Writes `bench/results/<YYYY-MM-DD>-<sha>.json` and copies it to `bench/results/latest.json`.
7. Prints the Markdown table that goes into the README.

Accepted implementations: a Python script using `httpx.AsyncClient` and
`asyncio.Semaphore`, or `oha`, `hey` or `k6` with output parsed into the schema
below. The choice is recorded in the result file.

## Result schema

```json
{
  "commit": "abc1234",
  "timestamp": "YYYY-MM-DDTHH:MM:SSZ",
  "tool": "httpx-asyncio",
  "hardware": { "cpu": "Apple M2", "cores": 8, "ram_gb": 16, "label": "laptop" },
  "python": "3.12.9",
  "concurrency": 10,
  "requests": 1000,
  "warmup": 50,
  "payload_set_sha256": "…",
  "latency_ms": { "p50": 38.2, "p95": 71.4, "p99": 95.0, "max": 140.3 },
  "throughput_rps": 212.5,
  "errors": 0
}
```

`hardware.label` is one of `laptop`, `ci-runner`, `cloud-<instance-type>`.
Laptop numbers are fine when labelled `laptop`. They are not fine labelled as
anything else.

## README table

Generated, not typed. A small script (`bench/to_markdown.py`) reads
`latest.json` and `evals/baseline.json` and prints:

```markdown
| Metric | Value | Conditions |
|--------|------:|------------|
| Macro-F1 | 0.912 | evals/dataset sha 3f2a…, n=240 |
| p50 latency | 38 ms | C=10, N=1000, laptop (M2, 8 cores) |
| p95 latency | 71 ms | same |
| Throughput | 212 req/s | same |
| Cost per request | $0.0000009 | 4 vCPU at $0.17/h, 60% utilisation |
```

The README `## Results` section is this output verbatim. A reviewer diffs the
two; any numeric drift fails 8.6.
