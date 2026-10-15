"""API contract. Fixed before any retrieval code exists (docs/brief.md)."""

from typing import Literal

from pydantic import BaseModel, Field

AnswerType = Literal[
    "simple_lookup", "table_extraction", "multi_hop", "comparative", "unanswerable"
]


class Citation(BaseModel):
    """A claim is only valid if it resolves to a retrieved chunk."""

    source_chunk_id: str = Field(min_length=1)
    document: str = Field(min_length=1, description="e.g. 'AAPL 10-K FY2023'")
    page: int = Field(ge=1)
    quote: str = Field(min_length=1, max_length=1000)


class Claim(BaseModel):
    text: str = Field(min_length=1, max_length=2000)
    citations: list[Citation] = Field(min_length=1)


class QueryRequest(BaseModel):
    question: str = Field(min_length=5, max_length=2000)
    tenant_id: str = Field(min_length=1, max_length=64)
    filters: dict[str, str] = Field(
        default_factory=dict, description="ticker, fiscal_year, section"
    )


class QueryResponse(BaseModel):
    answered: bool
    claims: list[Claim] = Field(default_factory=list)
    refusal_reason: str | None = Field(default=None, max_length=500)
    request_id: str


class HealthResponse(BaseModel):
    status: Literal["ok", "degraded"]
    version: str
    db: Literal["up", "down", "not_configured"]
