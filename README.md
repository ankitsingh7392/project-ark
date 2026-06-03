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
| [**packages/ats**](packages/ats/) | Recruitment automation | TF-IDF weighted Word2Vec + fuzzy skill extraction | Active |
| [**packages/lexiscan**](packages/lexiscan/) | Support ticket routing | Bag-of-Words / TF-IDF + Naïve Bayes | Active |
| [**packages/review-classifier**](packages/review-classifier/) | E-commerce NLP | Feature engineering pipeline (OHE → BoW → TF-IDF) | Active |
| [**automation/n8n**](automation/n8n/) | Workflow infrastructure | Self-hosted n8n + Postgres on Docker Compose | Active |
| [**automation/supermarket-ads**](automation/supermarket-ads/) | AI agent | Stock-aware promotional ad generation | Active |

---

## Package Summaries

### `packages/ats` — Resume ↔ Job Description Matcher

Screens resumes semantically rather than by keyword overlap. A candidate who writes "ML" when the JD says "Machine Learning" should not be filtered out — this does not filter them out.

**How it works:** Text is preprocessed and embedded as TF-IDF weighted Word2Vec document vectors. Cosine similarity scores the match. A parallel fuzzy skill extractor (against a curated 2,000-term taxonomy) produces a structured gap report: which skills the candidate has, which are missing, and how critical each gap is based on frequency in the JD.

**Serves a REST API** via FastAPI — `POST /match`, `POST /rank`, `POST /gaps`.

```
Resume (text)  ──┐
                  ├──► Preprocessor ──► TF-IDF × Word2Vec ──► Cosine Similarity ──► Score
JD     (text)  ──┘                                         ──► Skill Gap Report ──► Gaps
```

→ Full docs: [`packages/ats/README.md`](packages/ats/README.md)

---

### `packages/lexiscan` — Enterprise Text Classifier

Routes incoming text (support tickets, emails, documents) to the correct department or category with a confidence score. Designed to run on CPU without a GPU or cloud dependency.

**How it works:** Vectorises text using `CountVectorizer` (BoW) or `TfidfVectorizer`. A Multinomial Naïve Bayes classifier is trained on labelled examples. At inference, the model returns the predicted category and a confidence percentage; predictions below a configurable threshold are returned as `"Unknown"` rather than a low-confidence guess.

```
Raw text ──► Vectoriser (BoW / TF-IDF) ──► Naïve Bayes ──► Category + Confidence
```

→ Full docs: [`packages/lexiscan/README.md`](packages/lexiscan/README.md)

---

### `packages/review-classifier` — NLP Feature Engineering Pipeline

An end-to-end pipeline that scrapes real product reviews, engineers numerical features three ways, and benchmarks classifiers against each feature set.

```
Web scrape (Playwright) ──► Preprocess ──► OHE / BoW / TF-IDF
    ──► Sparsity analysis ──► Logistic Regression vs Naïve Bayes benchmark
```

**Key finding:** TF-IDF + Logistic Regression consistently outperforms raw BoW across precision, recall, and F1 — establishing it as the right baseline before reaching for embeddings.

→ Full docs: [`packages/review-classifier/README.md`](packages/review-classifier/README.md)

---

### `automation/` — Workflow Automation

Two independent setups built on self-hosted [n8n](https://n8n.io/):

- **`automation/n8n`** — Docker Compose stack: n8n + Postgres + task runners. Fully configured via `.env`; no credentials in source.
- **`automation/supermarket-ads`** — Python agent that reads live stock/pricing data from an inventory sheet and generates promotional ad copy for products with healthy margin.

→ Setup: [`automation/n8n/.env.example`](automation/n8n/.env.example)

---

## Repository Structure

```
project-ark/
│
├── packages/                       # Importable Python modules
│   ├── ats/                        # Resume ↔ JD semantic matcher (FastAPI)
│   │   ├── embedder.py             # TF-IDF × Word2Vec document vectors
│   │   ├── skill_extractor.py      # Exact + fuzzy skill matching
│   │   ├── matcher.py              # Similarity + gap scoring
│   │   ├── preprocessor.py         # Text cleaning / normalisation
│   │   ├── skills_taxonomy.json    # Curated 2,000-term skill taxonomy
│   │   └── pyproject.toml
│   ├── lexiscan/                   # Text classification engine
│   │   ├── lexiscan.py             # BoW/TF-IDF + Naïve Bayes model
│   │   ├── main.py                 # Training + inference entrypoint
│   │   └── data/
│   └── review-classifier/          # NLP feature engineering pipeline
│       ├── scraper.py              # Playwright-based review scraper
│       └── notebook/
│
├── automation/                     # Workflow agents and automation scripts
│   ├── n8n/                        # Self-hosted n8n + Postgres stack
│   └── supermarket-ads/            # Stock-aware ad generation agent
│
├── infra/                          # Infrastructure management
│   ├── infra.sh                    # Service manager (up/down/logs/status)
│   └── postgres/                   # Postgres + pgAdmin compose stack
│
├── .github/workflows/ci.yml        # CI pipeline
├── .pre-commit-config.yaml         # Pre-commit hooks
├── .gitleaks.toml                  # Secret scan config
└── pyproject.toml                  # Workspace root + ruff config
```

---

## Getting Started

This repo uses [uv](https://github.com/astral-sh/uv) for dependency management.

```bash
git clone https://github.com/ankitsingh7392/project-ark.git
cd project-ark
```

**Run a specific package:**

```bash
# ATS matcher
cd packages/ats && uv sync && uvicorn main:app --reload

# LexiScan classifier
cd packages/lexiscan && uv sync && uv run python main.py
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

---

## License

[MIT](LICENSE)
