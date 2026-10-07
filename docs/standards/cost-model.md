# Standard: Cost Model

Backs [`CHECKLIST.md`](../../CHECKLIST.md) §11.

## Principle

A system that works but cannot be run economically is not finished. Every
module states what it costs to run, shows the arithmetic, and names the single
biggest lever for reducing it.

## Required content of `docs/cost-model.md`

1. **Assumptions**, each with a date: instance type and hourly list price, provider token prices, requests per day, target utilisation.
2. **Drivers**, one row each, only those that apply: compute, model inference, embeddings, vector database, relational database, storage, external APIs, observability backend, network egress.
3. **Unit economics**: cost per request, per 1,000 requests, per 1,000,000 requests per month. Arithmetic shown, not just the answer.
4. **Fixed floor**: what it costs at zero traffic (an always-on instance, a minimum DB tier).
5. **Biggest lever**: one paragraph naming the change that most reduces cost, with an estimate of the saving.
6. **Link to measurement**: throughput comes from `bench/results/latest.json`; token counts come from `evals/results/`.

## Worked example: ML-SVC, compute only

```text
Measured (bench/results/latest.json):
  Throughput                         85 req/s at C=10 on 4 vCPU

Assumptions (list prices, 2026-10-07):
  Instance                           4 vCPU / 8 GB, $0.17 per hour
  Target utilisation                 60%

Capacity per instance-hour           85 × 0.6 × 3600 = 183,600 requests
Cost per request                     0.17 / 183,600 = $0.00000093
Cost per 1,000 requests              $0.00093
Cost per 1,000,000 requests          $0.93

Fixed floor                          1 instance always on: 0.17 × 730 = $124 per month
Break-even traffic for the floor     124 / 0.00000093 ≈ 133M requests per month;
                                     below that, the floor dominates

Biggest lever                        The 3.6 GB Word2Vec model forces an 8 GB instance.
                                     100-dimensional vectors cut the model to ~1.2 GB,
                                     allowing a 4 GB instance at ~$0.09/h: ~47% saving
                                     on the floor. Quality impact must be measured
                                     with `make eval` before adopting.
```

## Worked example: LLM-SVC, provider billed

```text
Measured (evals/results/<sha>.json):
  Mean prompt tokens                 1,850
  Mean completion tokens             220

Assumptions (provider list price, 2026-10-07):
  Input                              $3.00 per 1M tokens
  Output                             $15.00 per 1M tokens

Inference per request                (1850 × 3 + 220 × 15) / 1,000,000 = $0.00885
Compute per request                  (from the ML-SVC method above)       $0.00001
Cost per request                     ≈ $0.0089
Cost per 1,000 requests              $8.90
Cost per 1,000,000 requests          $8,900

Biggest lever                        Prompt is 1,850 tokens; 1,100 of those are a static
                                     instruction block. Prompt caching or trimming it to
                                     600 tokens cuts input cost by ~60%: ≈ $5,300 per 1M.
```
