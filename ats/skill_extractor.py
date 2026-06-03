import json
from pathlib import Path

from rapidfuzz import fuzz


class SkillExtractor:
    "Extract skills in text using a curated taxonomy + fuzzy matching"

    def __init__(self, taxonomy_path: str = "skills_taxonomy.json", fuzz_threshold: int = 88):
        self.fuzz_threshold = fuzz_threshold
        self.skills: list[str] = [
            skill
            for category in self._load_taxonomy(taxonomy_path)["categories"]
            for skill in category["skills"]
        ]
        # Lowercased lookup for exact matching
        self.skills_lower = {s.lower(): s for s in self.skills}

    def _load_taxonomy(self, path: str) -> list[str]:
        p = Path(path)
        if not p.exists():
            # Fallback minimal taxonomy
            return {
                "categories": [
                    {
                        "category": "fallback",
                        "skills": [
                            "python",
                            "java",
                            "c++",
                            "javascript",
                            "sql",
                            "machine learning",
                            "deep learning",
                            "tensorflow",
                            "pytorch",
                            "docker",
                            "kubernetes",
                            "aws",
                            "azure",
                        ],
                    }
                ]
            }
        with p.open() as f:
            return json.load(f)

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
        tokens = text_lower.split()
        # Phase 2: fuzzy match on tokens for typo tolerance
        for token in tokens:
            if len(token) < 4:
                continue
            for skill in self.skills:
                # compare against full skill
                score = fuzz.partial_ratio(token.lower(), skill.lower())
                if score >= self.fuzz_threshold:
                    found.add(skill)
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
