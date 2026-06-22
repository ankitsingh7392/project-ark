"""Core matching logic: combines semantic similarity with skill gap analysis."""

import numpy as np

from app.embedder import TfIdfWord2VecEmbedder
from app.skill_extractor import SkillExtractor


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Cosine similarity scaled to [0, 1]."""
    denom = (np.linalg.norm(a) * np.linalg.norm(b)) + 1e-9
    raw = float(np.dot(a, b) / denom)
    return (raw + 1.0) / 2.0  # rescale from [-1, 1] to [0, 1]


def score_to_label(score: float) -> str:
    if score >= 0.80:
        return "Strong Match"
    if score >= 0.65:
        return "Good Match"
    if score >= 0.50:
        return "Weak Match"
    return "Poor Match"


class ResumeMatcher:
    """Top-level matcher orchestrating embedding and skill extraction."""

    def __init__(self, embedder: TfIdfWord2VecEmbedder, skill_extractor: SkillExtractor):
        self.embedder = embedder
        self.skill_extractor = skill_extractor

    def match(self, resume_text: str, jd_text: str) -> dict:
        """Score a single resume against a JD."""
        resume_vec = self.embedder.embed(resume_text)
        jd_vec = self.embedder.embed(jd_text)
        score = cosine_similarity(resume_vec, jd_vec)
        gaps = self.skill_extractor.gap_analysis(resume_text, jd_text)

        return {
            "match_score": round(score, 3),
            "match_label": score_to_label(score),
            "matched_skills": gaps["matched"],
            "missing_skills": gaps["missing"],
        }

    def rank(self, jd_text: str, resumes: list[dict]) -> list[dict]:
        """Rank multiple resumes against a single JD."""
        jd_vec = self.embedder.embed(jd_text)
        results = []
        for r in resumes:
            resume_vec = self.embedder.embed(r["text"])
            score = cosine_similarity(resume_vec, jd_vec)
            results.append({"id": r["id"], "score": round(score, 3)})

        results.sort(key=lambda x: x["score"], reverse=True)
        for idx, item in enumerate(results, start=1):
            item["rank"] = idx
        return results
