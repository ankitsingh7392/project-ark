"""Extracts skills from text using a curated taxonomy and fuzzy matching."""

import json
from pathlib import Path

from rapidfuzz import fuzz, process


class SkillExtractor:
    """Identifies skills in text using a curated taxonomy + fuzzy matching."""

    def __init__(self, taxonomy_path: str = "data/skills_taxonomy.json", fuzz_threshold: int = 88):
        self.fuzz_threshold = fuzz_threshold
        self.skills: list[str] = self._load_taxonomy(taxonomy_path)
        # Lowercased lookup for exact matching
        self.skills_lower = {s.lower(): s for s in self.skills}

    def _load_taxonomy(self, path: str) -> list[str]:
        p = Path(path)
        if not p.exists():
            # Fallback minimal taxonomy
            return [
                "python",
                "java",
                "c++",
                "javascript",
                "sql",
                "machine learning",
                "deep learning",
                "natural language processing",
                "computer vision",
                "tensorflow",
                "pytorch",
                "scikit-learn",
                "pandas",
                "numpy",
                "aws",
                "gcp",
                "azure",
                "docker",
                "kubernetes",
                "linux",
                "react",
                "angular",
                "vue",
                "node.js",
                "fastapi",
                "flask",
                "communication",
                "leadership",
                "teamwork",
                "problem solving",
            ]
        with p.open() as f:
            data = json.load(f)
        return self._flatten_taxonomy(data)

    @staticmethod
    def _flatten_taxonomy(data) -> list[str]:
        """Accept either a flat ``["python", ...]`` list or the structured
        ``{"categories": [{"skills": [...]}, ...]}`` taxonomy and return a flat,
        de-duplicated list of skill names."""
        if isinstance(data, dict) and "categories" in data:
            skills = [
                skill for category in data["categories"] for skill in category.get("skills", [])
            ]
        elif isinstance(data, list):
            skills = data
        else:
            raise ValueError(
                "Unsupported taxonomy format: expected a list of skills or "
                "a {'categories': [...]} object."
            )
        # De-duplicate while preserving order
        return list(dict.fromkeys(skills))

    def extract(self, text: str) -> set[str]:
        """Return the set of skills found in the text."""
        text_lower = text.lower()
        found: set[str] = set()

        # Phase 1: exact substring matching (fast)
        for skill_lower, skill in self.skills_lower.items():
            # word boundary check for short skills to avoid e.g. "r" matching everywhere
            if len(skill_lower) <= 3:
                if f" {skill_lower} " in f" {text_lower} ":
                    found.add(skill)
            elif skill_lower in text_lower:
                found.add(skill)

        # Phase 2: fuzzy match on tokens for typo tolerance. Match against the
        # lowercased taxonomy (the curated taxonomy is title-cased, so a
        # case-sensitive comparison would miss most typos) and map back to the
        # canonical skill name.
        tokens = set(text_lower.split())
        for token in tokens:
            if len(token) < 4:
                continue
            match = process.extractOne(
                token,
                self.skills_lower.keys(),
                scorer=fuzz.ratio,
                score_cutoff=self.fuzz_threshold,
            )
            if match:
                found.add(self.skills_lower[match[0]])

        return found

    def gap_analysis(self, resume_text: str, jd_text: str) -> dict:
        """Return matched + missing skills."""
        resume_skills = self.extract(resume_text)
        jd_skills = self.extract(jd_text)
        return {
            "matched": sorted(resume_skills & jd_skills),
            "missing": sorted(jd_skills - resume_skills),
            "extra": sorted(resume_skills - jd_skills),
        }
