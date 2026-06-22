# Review Classifier — NLP Feature Engineering Pipeline

> Scrapes real product reviews and (work in progress) engineers numerical
> features three ways — One-Hot Encoding, Bag of Words, TF-IDF — to benchmark
> classifiers and show *why* TF-IDF is the right baseline before reaching for
> embeddings.

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.4+-F7931E.svg?logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Status: WIP](https://img.shields.io/badge/status-work%20in%20progress-yellow.svg)]()

---

## Status

| Stage | State |
|-------|-------|
| Review scraper (Playwright) | ✅ Implemented |
| Preprocessing + vocabulary | 🚧 Planned |
| Feature engineering (OHE / BoW / TF-IDF) | 🚧 Planned |
| Classifier benchmark (LogReg vs. Naïve Bayes) | 🚧 Planned |

This module is an in-progress study, not a finished benchmark. The scraper runs
today; the feature-engineering and evaluation stages are the next milestones.
The benchmark numbers are intentionally **not** published here until the
evaluation code exists.

---

## What's here

```
review-classifier/
├── scraper.py     # Playwright review scraper (functions + __main__ entrypoint)
├── tests/         # Smoke tests for the scraper helpers (no network)
└── pyproject.toml
```

---

## Quick start

Managed with [uv](https://github.com/astral-sh/uv).

```bash
cd projects/review-classifier
uv sync

# Playwright needs its browser binaries once
uv run playwright install chromium

# Scrape reviews into reviews.csv (the output file is git-ignored)
uv run python scraper.py
```

Run the tests (no browser or network required):

```bash
uv run pytest
```

---

## Planned approach

The pipeline will transform scraped reviews into three feature
representations and compare them on a sentiment-classification task:

| Encoding         | Captures frequency | Penalises common words | Best for          |
|------------------|:------------------:|:----------------------:|-------------------|
| One-Hot Encoding | ✗                  | ✗                      | tiny vocabularies |
| Bag of Words     | ✓                  | ✗                      | fast baselines    |
| TF-IDF           | ✓                  | ✓                      | large corpora     |

`TF-IDF(t, d) = TF(t, d) × log(N / df(t))` — down-weights ubiquitous words and
highlights discriminative terms. The hypothesis to test is that **TF-IDF +
Logistic Regression** beats raw Bag-of-Words on precision/recall/F1.

> Note: scraped data is collected for personal study only; respect each
> platform's terms of service. No data files are committed.

---

## Tech stack

| Layer            | Tool                                |
|------------------|-------------------------------------|
| Scraping         | Playwright                          |
| Data handling    | pandas, NumPy                       |
| Feature engineering | scikit-learn (`CountVectorizer`, `TfidfVectorizer`) |
| Classification   | scikit-learn (`LogisticRegression`, `MultinomialNB`) |
| Testing          | pytest                              |

---

## License

[MIT](../../LICENSE)
