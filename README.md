# Project Ark

> A monorepo of focused, production-oriented AI/ML services — each solving a real problem independently, sharing one toolchain and CI pipeline.

[![CI](https://github.com/ankitsingh7392/project-ark/actions/workflows/ci.yml/badge.svg)](https://github.com/ankitsingh7392/project-ark/actions/workflows/ci.yml)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-22c55e.svg)](LICENSE)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-D7FF64.svg)](https://github.com/astral-sh/ruff)

---

## Modules

| Module | Domain | Core Technique | Interface |
|--------|--------|---------------|-----------|
| [**projects/ats**](projects/ats/) | Recruitment automation | TF-IDF weighted Word2Vec + fuzzy skill extraction | FastAPI REST service, Docker |
| [**projects/lexiscan**](projects/lexiscan/) | Support ticket routing | TF-IDF + Multinomial Naïve Bayes with confidence thresholding | Python library + CLI |

---

## Project Summaries

### `projects/ats` — Resume ↔ Job Description Matcher

Screens resumes semantically rather than by keyword overlap. A candidate who writes "ML" when the job description says "Machine Learning" is not filtered out.

**How it works:** Text is preprocessed and embedded as TF-IDF weighted Word2Vec document vectors. Cosine similarity scores the match. A parallel fuzzy skill extractor (against a curated taxonomy of 160+ skills spanning 15 categories) produces a structured gap report: which skills the candidate has, which are missing, and how heavily the job description weights each gap.

**Serves a REST API** via FastAPI — `POST /match`, `POST /rank`, `POST /gaps`.

```
Resume (text)  ──┐
                  ├──► Preprocessor ──► TF-IDF × Word2Vec ──► Cosine Similarity ──► Score
JD     (text)  ──┘                                         ──► Skill Gap Report ──► Gaps
```

→ Full docs: [`projects/ats/README.md`](projects/ats/README.md)

---

### `projects/lexiscan` — Support Ticket Classifier

Routes incoming text (support tickets, emails, documents) to the correct department with a confidence score. Runs on CPU with no GPU or cloud dependency.

**How it works:** Text is vectorised with `TfidfVectorizer` (or `CountVectorizer`) and classified by a Multinomial Naïve Bayes model trained on labelled examples. At inference the model returns the predicted category and a confidence percentage; predictions below a configurable threshold are returned as `Unknown` rather than a low-confidence guess, so they can be escalated to a human.

```
Raw text ──► Vectoriser (BoW / TF-IDF) ──► Naïve Bayes ──► Category + Confidence
```

→ Full docs: [`projects/lexiscan/README.md`](projects/lexiscan/README.md)

---

## Repository Structure

```
project-ark/
│
├── projects/
│   ├── ats/                        # Resume ↔ JD semantic matcher (FastAPI)
│   │   ├── app/                    # Application package
│   │   │   ├── main.py             # FastAPI app & endpoints
│   │   │   ├── embedder.py         # TF-IDF × Word2Vec document vectors
│   │   │   ├── matcher.py          # Similarity + ranking
│   │   │   ├── skill_extractor.py  # Exact + fuzzy skill matching
│   │   │   ├── preprocessor.py     # Text cleaning / normalisation
│   │   │   └── schemas.py          # Pydantic request/response models
│   │   ├── data/skills_taxonomy.json  # Curated 160+ skill taxonomy
│   │   ├── tests/                  # Model-free pytest suite
│   │   ├── Dockerfile
│   │   └── pyproject.toml
│   └── lexiscan/                   # Text classification engine
│       ├── lexiscan.py             # TF-IDF / BoW + Naïve Bayes model
│       ├── main.py                 # Train + classify CLI
│       ├── data/                   # Labelled training tickets
│       ├── tests/
│       └── pyproject.toml
│
├── .github/workflows/              # CI: lint, tests per module, secret scan
├── .pre-commit-config.yaml         # Pre-commit hooks
├── .gitleaks.toml                  # Secret scan config
└── pyproject.toml                  # Shared ruff config (each module locks deps independently)
```

---

## Getting Started

This repo uses [uv](https://github.com/astral-sh/uv) for dependency management. Each module is a standalone project with its own lockfile.

```bash
git clone https://github.com/ankitsingh7392/project-ark.git
cd project-ark
```

**Run a module:**

```bash
# ATS matcher (needs the Word2Vec model — see projects/ats/README.md)
cd projects/ats && uv sync && uv run uvicorn app.main:app --reload

# LexiScan classifier
cd projects/lexiscan && uv sync && uv run python main.py "The app crashes every time I log in"
```

**Run the tests:**

```bash
cd projects/ats && W2V_MODEL_PATH=/nonexistent uv run pytest
cd projects/lexiscan && uv run pytest
```

---

## Toolchain

| Concern | Tool |
|---------|------|
| Package management | [uv](https://github.com/astral-sh/uv) |
| Testing | [pytest](https://docs.pytest.org/) |
| Lint + format | [ruff](https://github.com/astral-sh/ruff) |
| Secret scanning | [gitleaks](https://github.com/gitleaks/gitleaks) |
| Pre-commit hooks | [pre-commit](https://pre-commit.com/) |
| CI | GitHub Actions |

**Set up pre-commit locally (one-time):**

```bash
pip install pre-commit && pre-commit install
```

---

## License

[MIT](LICENSE)
