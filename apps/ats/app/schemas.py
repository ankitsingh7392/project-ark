"""Pydantic models for request/response validation."""

from pydantic import BaseModel, ConfigDict, Field


class MatchRequest(BaseModel):
    resume_text: str = Field(..., min_length=50, description="Full resume text")
    jd_text: str = Field(..., min_length=50, description="Job description text")


class MatchResponse(BaseModel):
    match_score: float = Field(..., ge=0.0, le=1.0)
    match_label: str  # "Strong Match", "Good Match", "Weak Match", "Poor Match"
    matched_skills: list[str]
    missing_skills: list[str]


class ResumeEntry(BaseModel):
    id: str
    text: str = Field(..., min_length=50)


class RankRequest(BaseModel):
    jd_text: str = Field(..., min_length=50)
    resumes: list[ResumeEntry] = Field(..., min_length=1, max_length=500)


class RankedCandidate(BaseModel):
    id: str
    score: float
    rank: int


class RankResponse(BaseModel):
    ranking: list[RankedCandidate]


class SkillGap(BaseModel):
    skill: str
    importance: float  # TF-IDF weight in JD


class GapsResponse(BaseModel):
    matched_skills: list[str]
    missing_skills: list[SkillGap]
    coverage_pct: float


class HealthResponse(BaseModel):
    # ``model_loaded`` collides with Pydantic's protected ``model_`` namespace
    model_config = ConfigDict(protected_namespaces=())

    status: str
    model_loaded: bool
    version: str
