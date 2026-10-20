"""Golden-set schema and loader. One row per line in data/golden_set.jsonl."""

import hashlib
from collections import Counter
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

Category = Literal["simple_lookup", "table_extraction", "multi_hop", "comparative", "unanswerable"]
Difficulty = Literal["easy", "medium", "hard"]

# Target mix from docs/brief.md. Tolerance ±5 points, checked once n >= 150.
TARGET_MIX: dict[str, float] = {
    "simple_lookup": 0.30,
    "table_extraction": 0.25,
    "multi_hop": 0.20,
    "comparative": 0.10,
    "unanswerable": 0.15,
}


class Source(BaseModel):
    document: str = Field(min_length=1, description="e.g. 'AAPL 10-K FY2023'")
    page: int | None = Field(default=None, ge=1)
    section: str | None = None


class GoldenRow(BaseModel):
    id: str = Field(pattern=r"^g\d{4}$")
    question: str = Field(min_length=10, max_length=1000)
    ground_truth: str = Field(min_length=1, max_length=2000)
    sources: list[Source] = Field(default_factory=list)
    category: Category
    difficulty: Difficulty
    verified: bool = Field(
        description="True only after a human checked the answer against the filing"
    )
    origin: Literal["hand_written", "llm_drafted"]


def load(path: Path) -> list[GoldenRow]:
    rows = [
        GoldenRow.model_validate_json(line)
        for line in path.read_text().splitlines()
        if line.strip()
    ]
    ids = [r.id for r in rows]
    if len(ids) != len(set(ids)):
        dupes = [i for i, c in Counter(ids).items() if c > 1]
        raise ValueError(f"duplicate golden ids: {dupes}")
    for r in rows:
        if r.category != "unanswerable" and not r.sources:
            raise ValueError(f"{r.id}: answerable rows need at least one source")
    return rows


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def mix(rows: list[GoldenRow]) -> dict[str, float]:
    n = len(rows) or 1
    counts = Counter(r.category for r in rows)
    return {k: round(counts.get(k, 0) / n, 3) for k in TARGET_MIX}
