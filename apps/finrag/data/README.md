# data/

| File | What | Committed? |
|------|------|-----------|
| `golden_set.jsonl` | Question / ground-truth pairs written **from the filings, before the system exists**. Schema in `evals/golden.py`. | Yes (< 1 MB) |
| `filings/` | Raw SEC EDGAR 10-K / 10-Q documents (HTML/PDF). Downloaded by `make setup` in the ingestion milestone. | No (`.gitignore`) |

## Golden-set rules

- Target mix: 30 % simple lookup · 25 % table extraction · 20 % multi-hop · 10 % comparative · 15 % unanswerable.
- `verified: true` only after a human has read the cited page. LLM-drafted rows stay `verified: false` until then.
- Never write a question you already know the system answers. Write it from the document.
- `make eval` validates every row and prints the mix.
