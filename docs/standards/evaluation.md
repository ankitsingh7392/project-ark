# Standard: Evaluation

Backs [`CHECKLIST.md`](../../CHECKLIST.md) §6.

## Why

Unit tests prove the code does what the author intended. They do not prove the
model is any good. Evaluation is the test suite for model behaviour, and it
gates merges the same way unit tests do.

## Dataset rules

* Committed under `evals/`, small enough to review in a PR (target < 1 MB).
* At least 100 labelled examples. Fewer gives a confidence interval too wide to detect regressions.
* **Disjoint from training data.** A test asserts this by hashing each example and checking for overlap.
* Has a `source` column: where each example came from (synthetic, scraped, hand-written, production sample).
* Versioned by content hash. The hash is recorded in every results file and in the baseline.
* Adversarial or edge cases are labelled as such in a `tag` column so per-slice metrics can be reported.

## Metrics by project type

| Type | Minimum metrics |
|------|-----------------|
| ML-SVC classifier | Accuracy, macro-F1, per-class precision and recall, confusion matrix. If the model abstains (`Unknown`), the abstain rate and accuracy-when-answered. |
| ML-SVC ranker or matcher | Spearman ρ or NDCG@k against human-labelled pairs; top-1 accuracy on pairwise comparisons. |
| LLM-SVC | Answer correctness via an LLM judge with a written rubric **and** at least 50 human-labelled items that calibrate the judge; structured-output validity rate; refusal rate on a safety subset. |
| RAG | LLM-SVC metrics plus retrieval recall@k, precision@k, and groundedness or faithfulness. |
| AGENT | LLM-SVC metrics plus tool-call accuracy, task completion rate, mean steps per task. |

Every type also records per-run **latency** and, where a provider bills per
token, **tokens and cost**, so §8 and §11 come from the same artifact.

## Runner contract

`evals/run_eval.py`:

1. Loads the dataset, computes and prints its sha256.
2. Fixes every random seed.
3. Runs the model through the same code path the service uses (import the app, do not re-implement).
4. Writes `evals/results/<git-sha>.json`.
5. Compares the primary metric against `min_acceptable` in `evals/baseline.json`.
6. Exits 1 if below, 0 otherwise. Prints both numbers either way.

## `evals/baseline.json`

```json
{
  "metric": "macro_f1",
  "value": 0.912,
  "min_acceptable": 0.89,
  "n": 240,
  "dataset_sha256": "…",
  "commit": "abc1234",
  "date": "YYYY-MM-DD"
}
```

## `evals/results/<sha>.json`

```json
{
  "commit": "abc1234",
  "timestamp": "YYYY-MM-DDTHH:MM:SSZ",
  "dataset_sha256": "…",
  "n": 240,
  "metrics": { "macro_f1": 0.912, "accuracy": 0.925, "abstain_rate": 0.04 },
  "per_class": { "Billing": { "precision": 0.94, "recall": 0.91 } },
  "latency_ms": { "p50": 3.1, "p95": 5.8 },
  "tokens": null,
  "cost_usd": null
}
```

## Changing the baseline

* **Raising `value`:** a PR that includes the new results file. The new value becomes the baseline.
* **Lowering `min_acceptable`:** requires an ADR explaining why the lower bar is acceptable.
* **Changing the dataset:** the hash changes, so the baseline must be re-established in the same PR, with the old and new numbers both shown in the PR description.
