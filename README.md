# Project Ark

> A monorepo of focused, production-oriented AI/ML modules — each solving a real problem independently, sharing a unified infrastructure and toolchain.

[![CI](https://github.com/ankitsingh7392/project-ark/actions/workflows/ci.yml/badge.svg)](https://github.com/ankitsingh7392/project-ark/actions/workflows/ci.yml)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-22c55e.svg)](LICENSE)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-D7FF64.svg)](https://github.com/astral-sh/ruff)

---

## Modules

| Module | Domain | Core Technique | Status |
|--------|--------|---------------|--------|
| [**ats**](ats/) | Recruitment automation | TF-IDF weighted Word2Vec + fuzzy skill extraction | Active |
| [**lexiscan**](lexiscan/) | Support ticket routing | Bag-of-Words / TF-IDF + Naïve Bayes | Active |
| [**product_review_classifier**](product_review_classifier/) | E-commerce NLP | Feature engineering pipeline (OHE → BoW → TF-IDF) | Active |
| [**n8n**](n8n/) | Workflow automation | Self-hosted n8n + AI-driven ad generation agent | Active |

---

## Module Summaries

### `ats` — Resume ↔ Job Description Matcher

Screens resumes semantically rather than by keyword overlap. A candidate who writes "ML" when the JD says "Machine Learning" should not be filtered out — this does not filter them out.

**How it works:** Text is preprocessed and embedded as TF-IDF weighted Word2Vec document vectors. Cosine similarity scores the match. A parallel fuzzy skill extractor (against a curated 2,000-term taxonomy) produces a structured gap report: which skills the candidate has, which are missing, and how critical each gap is based on frequency in the JD.

**Serves a REST API** via FastAPI — `POST /match`, `POST /rank`, `POST /gaps`.

```
Resume (text)  ──┐
                  ├──► Preprocessor ──► TF-IDF × Word2Vec ──► Cosine Similarity ──► Score
JD     (text)  ──┘                                         ──► Skill Gap Report ──► Gaps
```

→ Full docs: [`ats/README.md`](ats/README.md)

---

### `lexiscan` — Enterprise Text Classifier

Routes incoming text (support tickets, emails, documents) to the correct department or category with a confidence score. Designed to run on CPU without a GPU or cloud dependency.

**How it works:** Vectorises text using `CountVectorizer` (BoW) or `TfidfVectorizer`. A Multinomial Naïve Bayes classifier is trained on labelled examples. At inference, the model returns the predicted category and a confidence percentage; predictions below a configurable threshold are returned as `"Unknown"` rather than a low-confidence guess.

```
Raw text ──► Vectoriser (BoW / TF-IDF) ──► Naïve Bayes ──► Category + Confidence
```

→ Full docs: [`lexiscan/README.md`](lexiscan/README.md)

---

### `product_review_classifier` — NLP Feature Engineering Pipeline

An end-to-end learning exercise that scrapes real product reviews, engineers numerical features three ways, and benchmarks classifiers against each feature set. The primary output is insight, not a production service.

**Pipeline stages:**

```
Web scrape (Playwright) ──► Preprocess ──► OHE / BoW / TF-IDF
    ──► Sparsity analysis ──► Logistic Regression vs Naïve Bayes benchmark
```

**Key finding:** TF-IDF + Logistic Regression consistently outperforms raw BoW across precision, recall, and F1 — establishing it as the right baseline before reaching for embeddings.

→ Full docs: [`product_review_classifier/README.md`](product_review_classifier/README.md)

---

### `n8n` — Automation Infrastructure

Two independent automation setups built on self-hosted [n8n](https://n8n.io/):

- **`self-hosted-server`** — Docker Compose stack: n8n + Postgres + task runners. Fully configured via `.env`; no credentials in source.
- **`supermarket-ads`** — An n8n workflow + Python agent that reads live stock/pricing data from an Excel sheet and generates promotional ad copy for products with healthy margin.

→ Setup: [`n8n/self-hosted-server/.env.example`](n8n/self-hosted-server/.env.example)

---

## Repository Structure

```
project-ark/
├── ats/                        # Resume ↔ JD semantic matcher (FastAPI)
│   ├── embedder.py             # TF-IDF × Word2Vec document vectors
│   ├── skill_extractor.py      # Exact + fuzzy skill matching
│   ├── matcher.py              # Similarity + gap scoring
│   ├── preprocessor.py         # Text cleaning / normalisation
│   ├── skills_taxonomy.json    # Curated 2,000-term skill taxonomy
│   └── pyproject.toml
├── lexiscan/                   # Text classification engine
│   ├── lexiscan.py             # BoW/TF-IDF + Naïve Bayes model
│   ├── main.py                 # Training + inference entrypoint
│   └── data/
│       └── enterprise_tickets.csv
├── product_review_classifier/  # NLP feature engineering pipeline
│   ├── scraper.py              # Playwright-based review scraper
│   └── notebook/               # Jupyter analysis
├── n8n/
│   ├── self-hosted-server/     # Docker Compose + Postgres
│   └── supermarket-ads/        # Ad-generation agent
├── infra/
│   ├── infra.sh                # Service manager (up/down/logs/status)
│   └── postgres/               # Postgres + pgAdmin compose stack
├── .github/workflows/ci.yml    # CI pipeline
├── .pre-commit-config.yaml     # Pre-commit hooks
├── .gitleaks.toml              # Secret scan config
└── pyproject.toml              # Workspace root + ruff config
```

---

## Getting Started

This repo uses [uv](https://github.com/astral-sh/uv) for dependency management.

```bash
git clone https://github.com/ankitsingh7392/project-ark.git
cd project-ark
```

**Run a specific module:**

```bash
# ATS matcher
cd ats && uv sync && uvicorn main:app --reload

# LexiScan classifier
cd lexiscan && uv sync && uv run python main.py
```

**Start infrastructure:**

```bash
# First run — prompts for credentials, saves to ~/.secrets/.env
./infra/infra.sh up postgres

./infra/infra.sh status
./infra/infra.sh logs postgres
```

---

## Toolchain

| Concern | Tool |
|---------|------|
| Package management | [uv](https://github.com/astral-sh/uv) |
| Lint + format | [ruff](https://github.com/astral-sh/ruff) |
| Secret scanning | [gitleaks](https://github.com/gitleaks/gitleaks) |
| Shell lint | [shellcheck](https://www.shellcheck.net/) |
| Pre-commit hooks | [pre-commit](https://pre-commit.com/) |
| CI | GitHub Actions |

**Set up pre-commit locally (one-time):**

```bash
pip install pre-commit && pre-commit install
```

After this, every `git commit` automatically runs the full hook suite — secrets, lint, format, shell checks — before the commit lands.

---

## License

[MIT](LICENSE)
