# Resume ↔ Job Description Semantic Matcher

> A resume-screening service that uses **TF-IDF weighted Word2Vec embeddings** to
> semantically match candidate resumes against job descriptions, surface skill
> gaps, and rank multiple candidates — served over a **FastAPI** REST API.

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/docker-ready-2496ED.svg?logo=docker&logoColor=white)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/license-MIT-22c55e.svg)](../../LICENSE)

---

## Problem

Keyword-based Applicant Tracking Systems reject strong candidates for using
synonyms ("ML" vs "Machine Learning"), give recruiters no structured view of
what a candidate is *missing*, and don't scale to hundreds of resumes per
opening. This service addresses all three with semantic embeddings and a
structured skill-gap report.

---

## Features

- **Semantic matching** — TF-IDF weighted Word2Vec document vectors compared with
  cosine similarity, so related terms and synonyms still match.
- **Multi-candidate ranking** — rank N resumes against a single job description.
- **Skill-gap analysis** — a curated taxonomy (**160+ skills across 15
  categories**) plus fuzzy matching (RapidFuzz) reports matched vs. missing
  skills, tolerant of typos and casing.
- **REST API** — FastAPI with auto-generated OpenAPI docs at `/docs`.
- **Containerized** — a single `docker build` produces a runnable image.
- **Tested** — pytest suite for the skill extractor and API contract that runs
  without the multi-GB model (see [Testing](#testing)).

---

## Architecture

```
Resume (text) ─┐
               ├─► Preprocessor ─► TF-IDF × Word2Vec ─► Cosine similarity ─► score + label
JD     (text) ─┘   (clean/lemma)   (weighted doc vec)
               │
               └─► Skill Extractor (taxonomy + fuzzy) ─► matched / missing skills
```

How the embedding works — instead of plain averaging (which drowns out
domain terms), each word vector is weighted by its TF-IDF score:

```
doc_vector = Σ (tfidf(word) × word2vec(word)) / Σ tfidf(word)
```

Cosine similarity is rescaled from `[-1, 1]` to `[0, 1]` and mapped to a label
(`Strong` / `Good` / `Weak` / `Poor` Match).

---

## Quick start

This module is managed with [uv](https://github.com/astral-sh/uv).

```bash
cd projects/ats
uv sync
```

### Get the Word2Vec model (one-time, ~3.6 GB)

The matcher loads pre-trained vectors from `data/word2vec.kv`. Download Google
News Word2Vec via gensim and save it in the expected format:

```bash
uv run python - <<'PY'
import gensim.downloader as api
api.load("word2vec-google-news-300").save("data/word2vec.kv")
PY
```

The model files are git-ignored — only the source and the skill taxonomy are
committed.

### Run the API

```bash
uv run uvicorn app.main:app --reload --port 8000
```

Open <http://localhost:8000/docs> for the interactive Swagger UI.
`/health` reports whether the model loaded; if `data/word2vec.kv` is absent the
service still starts, but `/match` and `/rank` return `503` until it is present.

### Run with Docker

```bash
docker build -t resume-matcher .
# Mount the model directory at runtime (it is not baked into the image)
docker run -p 8000:8000 -v "$PWD/data:/app/data" resume-matcher
```

---

## API reference

| Method | Path      | Description                                            |
|--------|-----------|--------------------------------------------------------|
| `GET`  | `/health` | Service + model-load status.                           |
| `POST` | `/match`  | Similarity score + matched/missing skills for one pair.|
| `POST` | `/rank`   | Rank a list of resumes against one JD.                 |
| `POST` | `/gaps`   | Skill-gap report with coverage percentage.             |

**`POST /match`**

```json
// request
{ "resume_text": "Software engineer with 5 years of Python and ML...",
  "jd_text": "Senior ML engineer skilled in Python, TensorFlow..." }

// response
{ "match_score": 0.847,
  "match_label": "Strong Match",
  "matched_skills": ["Python", "Machine Learning", "TensorFlow"],
  "missing_skills": ["Kubernetes", "AWS"] }
```

`resume_text` and `jd_text` must be at least 50 characters (validated by
Pydantic). `/rank` accepts 1–500 resumes, each `{ "id": "...", "text": "..." }`.

---

## Project structure

```
ats/
├── app/
│   ├── main.py            # FastAPI app & endpoints
│   ├── matcher.py         # ResumeMatcher: similarity + ranking
│   ├── embedder.py        # TF-IDF weighted Word2Vec document vectors
│   ├── skill_extractor.py # Taxonomy + fuzzy skill matching
│   ├── preprocessor.py    # NLTK text cleaning / lemmatisation
│   └── schemas.py         # Pydantic request/response models
├── data/
│   └── skills_taxonomy.json   # Curated 160+ skill taxonomy (model files git-ignored)
├── tests/
│   ├── test_api.py
│   └── test_skill_extractor.py
├── Dockerfile
├── pyproject.toml
└── README.md
```

---

## Testing

The suite is intentionally **model-free** so it runs fast in CI — point the
matcher at a non-existent model path so the API skips loading the vectors:

```bash
W2V_MODEL_PATH=/nonexistent uv run pytest
```

It covers the taxonomy loader, exact + fuzzy skill matching, gap analysis, and
the API request-validation contract.

---

## Tech stack

| Layer          | Tool                                  |
|----------------|---------------------------------------|
| Embeddings     | gensim (Word2Vec / KeyedVectors)      |
| TF-IDF         | scikit-learn (`TfidfVectorizer`)      |
| Skill matching | RapidFuzz                             |
| API            | FastAPI + Uvicorn                     |
| Validation     | Pydantic v2                           |
| Preprocessing  | NLTK                                  |
| Testing        | pytest + httpx                        |

---

## Roadmap

- [x] TF-IDF × Word2Vec matcher, skill extraction, FastAPI service, Docker image
- [ ] Held-out evaluation harness with published metrics
- [ ] PDF resume parsing (PyMuPDF)
- [ ] Sentence-BERT as an optional embedding backend
- [ ] Bias audit (name-perturbation testing)

---

## License

[MIT](../../LICENSE)
