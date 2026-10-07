# Project Ark

> A monorepo of focused, production-oriented AI/ML services — each solving a real problem independently, sharing one toolchain and CI pipeline.

[![CI](https://github.com/ankitsingh7392/project-ark/actions/workflows/ci.yml/badge.svg)](https://github.com/ankitsingh7392/project-ark/actions/workflows/ci.yml)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-22c55e.svg)](LICENSE)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-D7FF64.svg)](https://github.com/astral-sh/ruff)

---

## Apps

| App | Domain | Core Technique | Interface |
|--------|--------|---------------|-----------|
| [**apps/ats**](apps/ats/) | Recruitment automation | TF-IDF weighted Word2Vec + fuzzy skill extraction | FastAPI REST service, Docker |
| [**apps/lexiscan**](apps/lexiscan/) | Support ticket routing | TF-IDF + Multinomial Naïve Bayes with confidence thresholding | Python library + CLI |

---

## App Summaries

### `apps/ats` — Resume ↔ Job Description Matcher

Screens resumes semantically rather than by keyword overlap. A candidate who writes "ML" when the job description says "Machine Learning" is not filtered out.

**How it works:** Text is preprocessed and embedded as TF-IDF weighted Word2Vec document vectors. Cosine similarity scores the match. A parallel fuzzy skill extractor (against a curated taxonomy of 160+ skills spanning 15 categories) produces a structured gap report: which skills the candidate has, which are missing, and how heavily the job description weights each gap.

**Serves a REST API** via FastAPI — `POST /match`, `POST /rank`, `POST /gaps`.

```
Resume (text)  ──┐
                  ├──► Preprocessor ──► TF-IDF × Word2Vec ──► Cosine Similarity ──► Score
JD     (text)  ──┘                                         ──► Skill Gap Report ──► Gaps
```

→ Full docs: [`apps/ats/README.md`](apps/ats/README.md)

---

### `apps/lexiscan` — Support Ticket Classifier

Routes incoming text (support tickets, emails, documents) to the correct department with a confidence score. Runs on CPU with no GPU or cloud dependency.

**How it works:** Text is vectorised with `TfidfVectorizer` (or `CountVectorizer`) and classified by a Multinomial Naïve Bayes model trained on labelled examples. At inference the model returns the predicted category and a confidence percentage; predictions below a configurable threshold are returned as `Unknown` rather than a low-confidence guess, so they can be escalated to a human.

```
Raw text ──► Vectoriser (BoW / TF-IDF) ──► Naïve Bayes ──► Category + Confidence
```

→ Full docs: [`apps/lexiscan/README.md`](apps/lexiscan/README.md)

---

## How This Repo Is Built

Every app is held to the same written standard, so the quality is checkable rather than claimed.

| Document | Answers |
|----------|---------|
| [`CONSTITUTION.md`](CONSTITUTION.md) | How we build. The principles behind every decision. |
| [`CHECKLIST.md`](CHECKLIST.md) | What must be true before an app is done, with the command a reviewer runs to verify each item. |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | Branches, commits, pull requests. |
| [`docs/standards/`](docs/standards/) | The detailed standard behind each checklist section: toolchain, evaluation, observability, benchmarking, security, failure modes, cost. |
| [`docs/adr/`](docs/adr/) | Why repository-wide decisions were made: one uv project per app, the `apps/` and `libs/` layout. |
| [`docs/templates/`](docs/templates/) | Files to copy when starting an app or recording a decision. |

```
CONSTITUTION.md  ──►  CHECKLIST.md  ──►  apps/<name>/    ──►  CI / evaluation gate
  principles          requirements        implementation + evidence     enforcement
```

---

## Repository Structure

```
project-ark/
│
├── CONSTITUTION.md                 # Principles: how we build
├── CHECKLIST.md                    # Definition of done: what must be true
├── CONTRIBUTING.md                 # How contributors work
│
├── docs/
│   ├── adr/                        # Repository-wide decision records
│   ├── standards/                  # Detailed engineering standards
│   └── templates/                  # CHECKLIST, ADR, architecture, failure-mode, cost templates
│
├── apps/                           # Deployable services, one standalone uv project each
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
├── libs/                           # Shared code, created only when a pattern repeats across apps (ADR 002)
│
├── Makefile                        # Local CI: make ci
├── .github/workflows/              # Same checks on GitHub Actions
├── .pre-commit-config.yaml         # Pre-commit hooks
├── .gitleaks.toml                  # Secret scan config
└── pyproject.toml                  # Shared ruff config (each app locks deps independently)
```

---

## Getting Started

This repo uses [uv](https://github.com/astral-sh/uv) for dependency management. Each app is a standalone project with its own lockfile.

```bash
git clone https://github.com/ankitsingh7392/project-ark.git
cd project-ark
```

**Run an app:**

```bash
# ATS matcher (needs the Word2Vec model — see apps/ats/README.md)
cd apps/ats && uv sync && uv run uvicorn app.main:app --reload

# LexiScan classifier
cd apps/lexiscan && uv sync && uv run python main.py "The app crashes every time I log in"
```

**Run the checks:**

```bash
make ci          # lint + tests for every app + secret scan, from the repo root
make help        # individual targets
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
| CI | `make ci` locally; GitHub Actions runs the same targets |

**Set up pre-commit locally (one-time):**

```bash
make hooks
```

---

## License

[MIT](LICENSE)
