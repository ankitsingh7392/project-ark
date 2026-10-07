# Cost Model — <module>

Method: [`docs/standards/cost-model.md`](../../docs/standards/cost-model.md).

## Assumptions (dated)

| Assumption | Value | Source | Date |
|------------|-------|--------|------|
| Instance | ... vCPU / ... GB, $.../h | provider list price | YYYY-MM-DD |
| Target utilisation | 60% | — | — |
| Requests per day | ... | — | — |

## Measured inputs

| Input | Value | From |
|-------|-------|------|
| Throughput | ... req/s at C=... | `bench/results/latest.json` |
| Mean prompt tokens | ... | `evals/results/<sha>.json` |
| Mean completion tokens | ... | `evals/results/<sha>.json` |

## Drivers

| Driver | Per request | Notes |
|--------|------------:|-------|
| Compute | $... | ... |
| Inference | $... | ... |

## Unit economics

```text
Capacity per instance-hour    = throughput × utilisation × 3600 = ...
Cost per request              = instance $/h ÷ capacity          = ...
Cost per 1,000 requests       = ...
Cost per 1,000,000 requests   = ...
Fixed floor per month         = instance $/h × 730                = ...
```

## Biggest lever

One paragraph: the single change that most reduces cost, with the estimated
saving and what must be re-measured before adopting it.
