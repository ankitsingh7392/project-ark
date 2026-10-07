FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_PROJECT_ENVIRONMENT=/usr/local

# System deps needed to build gensim/scikit-learn wheels when no binary is available
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# uv for dependency management (consistent with the rest of the monorepo)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Install runtime dependencies only — the app is run from source, not installed
COPY pyproject.toml ./
RUN uv sync --no-install-project --no-dev

# Pre-download NLTK corpora so the container starts offline
RUN python -c "import nltk; [nltk.download(p, quiet=True) for p in ['punkt','punkt_tab','stopwords','wordnet','averaged_perceptron_tagger']]"

# Application code + the skill taxonomy (the large Word2Vec model is mounted at runtime)
COPY app/ ./app/
COPY data/skills_taxonomy.json ./data/skills_taxonomy.json

EXPOSE 8000

# Mount the Word2Vec model at /app/data/word2vec.kv (e.g. -v $PWD/data:/app/data)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
