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

# Singleton matcher loaded at startup
state = {"matcher": None}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load model on startup, clean up on shutdown."""
    embedder = TfIdfWord2VecEmbedder()
    if Path(MODEL_PATH).exists():
        embedder.load_word_vectors(MODEL_PATH)
        # Fit TF-IDF on a small bootstrap corpus — in production, fit on your full dataset
        embedder.fit_tfidf(
            [
                "software engineer python machine learning",
                "data scientist deep learning tensorflow",
                "frontend developer react javascript",
            ]
        )
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

    # Assign uniform importance for the stub; production should use TF-IDF weights
    missing_with_weights = [SkillGap(skill=s, importance=1.0) for s in gap["missing"]]
    return GapsResponse(
        matched_skills=gap["matched"],
        missing_skills=missing_with_weights,
        coverage_pct=round(coverage, 1),
    )
