# FinRAG — SEC filings retrieval you can prove

> **FinRAG answers an equity analyst's questions about SEC 10-K / 10-Q filings with the
> stated figure and a citation to the filing page, and refuses when the filing does not
> contain the answer.**

**Status: scaffold.** Roadmap P1, phase ① (brief, golden set, ADRs, architecture) in
progress. No retrieval code yet. The numbers table below is empty on purpose; it fills in
as `make eval` and `make bench` produce them.

## The four numbers

| Metric | Value | Conditions |
|--------|------:|------------|
| Correctly cited answers (golden set) | — | `make eval`, n = 0 verified rows |
| p50 / p95 time to first token | — | `make bench` |
| Throughput | — | `make bench` |
| £ per query | — | `docs/cost-model.md` |

## Architecture

See [`docs/architecture.md`](docs/architecture.md) for the C4 container diagram and request
flow. Decisions so far:

- [ADR 001](docs/adr/001-vector-store-pgvector.md) — Postgres + pgvector, one datastore
- [ADR 002](docs/adr/002-structure-aware-chunking.md) — structure-aware chunking, tables never split
- [ADR 003](docs/adr/003-tenant-boundary-repository-layer.md) — tenant boundary in the repository layer + RLS

## Quickstart

```bash
cd apps/finrag
cp .env.example .env            # fill in later; nothing needs a key yet
make setup                      # uv sync --frozen --dev
make test                       # unit + integration, model-free
make eval                       # validates data/golden_set.jsonl and prints the category mix
make up && make test-smoke      # Postgres (pgvector) + API via docker compose, then GET /health
```

## Layout

```
apps/finrag/
├── app/            FastAPI service: config, schemas (API contract), main (/health, request id)
├── data/           golden_set.jsonl (committed) · filings/ (downloaded, ignored)
├── evals/          golden-set schema + loader · run_eval.py (the merge gate, once a baseline exists)
├── docs/           brief.md · architecture.md · adr/
├── tests/          unit · integration (api, failures) · smoke
├── CHECKLIST.md    Definition of Done, evidence per item
└── Makefile        setup · up · down · test · lint · typecheck · eval · bench
```

## The plan (roadmap P1)

1. **① Scope & architecture** — brief ✅ · golden set (5 / 150+ rows, 1 verified) · ADRs ✅ (proposed) · C4 ✅
2. **② Ingestion** — parsing that survives real filings · structure-aware chunking · idempotent indexing · multi-tenancy
3. **③ Retrieval & generation** — hybrid BM25 + dense + RRF · reranking · query understanding · grounded generation with refusal
4. **④ Eval harness** — retrieval and generation scored separately · calibrated LLM judge · the ablation table · evals as CI gate · FinanceBench
5. **⑤ Harden & ship** — tracing and cost · latency budget and load test · failure modes · README, write-up, demo

## Limitations

Nothing works yet beyond `/health`. That is the honest state and the README will stay honest.
