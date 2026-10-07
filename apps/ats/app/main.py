"""FastAPI application — exposes the matcher via REST."""

import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException

from app.embedder import TfIdfWord2VecEmbedder
from app.matcher import ResumeMatcher
from app.schemas import (
    GapsResponse,
    HealthResponse,
    MatchRequest,
    MatchResponse,
    RankedCandidate,
    RankRequest,
    RankResponse,
    SkillGap,
)
from app.skill_extractor import SkillExtractor

VERSION = "0.1.0"
MODEL_PATH = os.getenv("W2V_MODEL_PATH", "data/word2vec.kv")

# Representative role descriptions used to bootstrap the TF-IDF weighting. Common
# skills recur across many entries (low IDF → low importance) while specialized
# ones appear rarely (high IDF → high importance), giving the matcher and the
# skill-gap importance a meaningful weighting out of the box.
BOOTSTRAP_CORPUS = [
    "backend software engineer python fastapi flask rest api postgresql sql docker aws",
    "senior python engineer microservices docker kubernetes aws sql ci cd",
    "data scientist python machine learning deep learning tensorflow pytorch sql statistics",
    "machine learning engineer python pytorch scikit learn mlops docker aws kubernetes",
    "nlp engineer python deep learning transformers natural language processing pytorch",
    "data engineer python sql spark airflow etl aws data warehouse pipelines",
    "frontend developer react typescript javascript html css redux",
    "full stack engineer react typescript node js graphql postgresql docker",
    "devops engineer kubernetes docker terraform aws ci cd linux monitoring",
    "cloud engineer aws gcp azure terraform kubernetes networking security",
    "computer vision engineer python pytorch opencv deep learning cnn",
    "analytics engineer sql python dbt data modeling reporting dashboards",
]

# Singleton matcher loaded at startup
state: dict[str, ResumeMatcher | None] = {"matcher": None}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load model on startup, clean up on shutdown."""
    embedder = TfIdfWord2VecEmbedder()
    if Path(MODEL_PATH).exists():
        embedder.load_word_vectors(MODEL_PATH)
        # Bootstrap TF-IDF corpus — representative role descriptions spanning the
        # skill taxonomy so IDF can differentiate common skills (python, sql) from
        # rarer ones (kubernetes, graphql). In production, fit on your full dataset.
        embedder.fit_tfidf(BOOTSTRAP_CORPUS)
    skill_extractor = SkillExtractor()
    state["matcher"] = ResumeMatcher(embedder, skill_extractor)
    yield
    state["matcher"] = None


app = FastAPI(
    title="Resume Matcher API",
    description="Semantic resume-to-JD matching with Word2Vec + TF-IDF",
    version=VERSION,
    lifespan=lifespan,
)


@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(
        status="ok",
        model_loaded=state["matcher"] is not None,
        version=VERSION,
    )


@app.post("/match", response_model=MatchResponse)
async def match(req: MatchRequest):
    matcher = state["matcher"]
    if matcher is None:
        raise HTTPException(503, "Matcher not initialized")
    try:
        result = matcher.match(req.resume_text, req.jd_text)
        return MatchResponse(**result)
    except RuntimeError as e:
        raise HTTPException(503, str(e)) from e


@app.post("/rank", response_model=RankResponse)
async def rank(req: RankRequest):
    matcher = state["matcher"]
    if matcher is None:
        raise HTTPException(503, "Matcher not initialized")
    resumes = [{"id": r.id, "text": r.text} for r in req.resumes]
    ranking = matcher.rank(req.jd_text, resumes)
    return RankResponse(ranking=[RankedCandidate(**r) for r in ranking])


@app.post("/gaps", response_model=GapsResponse)
async def gaps(req: MatchRequest):
    matcher = state["matcher"]
    if matcher is None:
        raise HTTPException(503, "Matcher not initialized")

    gap = matcher.skill_extractor.gap_analysis(req.resume_text, req.jd_text)
    total = len(gap["matched"]) + len(gap["missing"])
    coverage = (len(gap["matched"]) / total * 100) if total else 0.0

    # Importance = how heavily the job description weights each missing skill,
    # derived from the JD's TF-IDF token weights and normalized to [0, 1] so the
    # most-emphasized gap scores 1.0. Multi-word skills sum their token weights.
    embedder = matcher.embedder
    jd_weights = embedder.token_weights(req.jd_text)
    raw_importance = {
        skill: sum(jd_weights.get(tok, 0.0) for tok in embedder.preprocessor.tokenize(skill))
        for skill in gap["missing"]
    }
    peak = max(raw_importance.values(), default=0.0)
    missing_with_weights = sorted(
        (
            SkillGap(skill=s, importance=round(raw_importance[s] / peak, 3) if peak else 1.0)
            for s in gap["missing"]
        ),
        key=lambda sg: sg.importance,
        reverse=True,
    )
    return GapsResponse(
        matched_skills=gap["matched"],
        missing_skills=missing_with_weights,
        coverage_pct=round(coverage, 1),
    )
