"""Unit tests for the taxonomy loader and skill matching (no model required)."""

from pathlib import Path

import pytest
from app.skill_extractor import SkillExtractor

TAXONOMY = Path(__file__).resolve().parents[1] / "data" / "skills_taxonomy.json"


@pytest.fixture
def extractor() -> SkillExtractor:
    return SkillExtractor(taxonomy_path=str(TAXONOMY))


def test_taxonomy_flattens_categories(extractor: SkillExtractor):
    """The structured {'categories': [...]} taxonomy is flattened to a skill list."""
    assert isinstance(extractor.skills, list)
    assert len(extractor.skills) > 100
    assert "Python" in extractor.skills


def test_flatten_accepts_plain_list():
    assert SkillExtractor._flatten_taxonomy(["python", "java"]) == ["python", "java"]


def test_flatten_deduplicates():
    data = {"categories": [{"skills": ["Python", "SQL"]}, {"skills": ["Python"]}]}
    assert SkillExtractor._flatten_taxonomy(data) == ["Python", "SQL"]


def test_flatten_rejects_bad_format():
    with pytest.raises(ValueError):
        SkillExtractor._flatten_taxonomy(42)


def test_exact_match(extractor: SkillExtractor):
    found = extractor.extract("Experienced in Python and Docker.")
    assert "Python" in found
    assert "Docker" in found


def test_fuzzy_match_tolerates_typo(extractor: SkillExtractor):
    # "kubernets" (typo) should still resolve to Kubernetes
    found = extractor.extract("Deployed services on kubernets clusters")
    assert "Kubernetes" in found


def test_gap_analysis(extractor: SkillExtractor):
    resume = "Backend engineer skilled in Python and SQL."
    jd = "Looking for Python, SQL and Docker experience."
    gaps = extractor.gap_analysis(resume, jd)
    assert "Python" in gaps["matched"]
    assert "Docker" in gaps["missing"]
    assert gaps["matched"] == sorted(gaps["matched"])
