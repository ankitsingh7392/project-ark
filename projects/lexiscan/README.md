# LexiScan — Enterprise Text Classifier

> A CPU-only text classification engine that routes support tickets, emails and
> documents to the right department with a confidence score — and refuses to
> guess when it isn't sure.

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.4+-F7931E.svg?logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-22c55e.svg)](../../LICENSE)

---

## Problem

High-volume inboxes and ticket queues need triage before a human reads them.
Large language models can do this, but they are expensive per request, slow on
commodity hardware, and opaque about *why* they chose a label. For a fixed set
of departments, a linear model over TF-IDF features is faster, cheaper,
explainable, and accurate enough for first-pass routing.

---

## Features

- **TF-IDF or Bag-of-Words vectorisation** — unigrams + bigrams with English
  stop-word removal; the feature space is capped to keep memory bounded.
- **Multinomial Naïve Bayes classifier** — trains in milliseconds on thousands
  of examples and predicts in constant time.
- **Confidence-thresholded routing** — every prediction carries a confidence
  percentage. Anything below the threshold is returned as `Unknown` so it can
  be escalated instead of mis-routed.
- **No external services** — runs entirely on CPU with scikit-learn and pandas.

---

## Architecture

```
Labelled CSV ──► lowercase ──► TfidfVectorizer (1–2 grams) ──► MultinomialNB.fit
                                                                     │
New text ─────► lowercase ──► transform ──► predict_proba ──► max ≥ threshold ? label : Unknown
```

---

## Quick start

This module is managed with [uv](https://github.com/astral-sh/uv).

```bash
cd projects/lexiscan
uv sync

uv run python main.py "The app crashes every time I log in"
# Technical Support (66.98%)

uv run python main.py --threshold 70 "Do you offer student discounts?"
# Unknown (39.3%)
```

The CLI trains on [`data/enterprise_tickets.csv`](data/enterprise_tickets.csv)
(100+ labelled tickets across Billing, Technical Support and Returns). Point it
at your own data with `--data path/to/tickets.csv` or `LEXISCAN_DATA_PATH`; the
CSV needs `ticket_text` and `department` columns.

### Use as a library

```python
from lexiscan import LexiModel

model = LexiModel(use_tfidf=True)
model.train("data/enterprise_tickets.csv", text_column="ticket_text", label_column="department")

model.predict("I was charged twice for my subscription")
# {'category': 'Billing', 'confidence': 53.52}
```

---

## Project structure

```
lexiscan/
├── lexiscan.py    # LexiModel: vectoriser + Naïve Bayes + thresholding
├── main.py        # CLI: train on the bundled dataset and classify input
├── data/
│   └── enterprise_tickets.csv
├── tests/
│   └── test_lexiscan.py
└── pyproject.toml
```

---

## Testing

```bash
uv run pytest
```

Tests train on a small in-memory dataset, so they need no data files and run in
well under a second.

---

## Tech stack

| Layer          | Tool                                          |
|----------------|-----------------------------------------------|
| Vectorisation  | scikit-learn (`TfidfVectorizer`, `CountVectorizer`) |
| Classification | scikit-learn (`MultinomialNB`)                |
| Data handling  | pandas                                        |
| Testing        | pytest                                        |

---

## License

[MIT](../../LICENSE)
