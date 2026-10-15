"""Eval runner (docs/standards/evaluation.md). Today it validates the golden set and reports
its state; retrieval and generation metrics arrive with the baseline milestone."""

import sys
from pathlib import Path

from evals.golden import TARGET_MIX, load, mix, sha256

GOLDEN = Path(__file__).resolve().parent.parent / "data" / "golden_set.jsonl"


def main() -> int:
    rows = load(GOLDEN)
    verified = sum(r.verified for r in rows)
    print(
        f"golden set: {GOLDEN.name}  sha256={sha256(GOLDEN)[:12]}  n={len(rows)}  verified={verified}"
    )
    for cat, share in mix(rows).items():
        print(f"  {cat:17s} {share:5.1%}  (target {TARGET_MIX[cat]:.0%})")
    if len(rows) < 150:
        print(f"golden set has {len(rows)} rows; need >= 150 before a baseline is recorded")
    if verified < len(rows):
        print(
            f"{len(rows) - verified} rows unverified — a baseline is only meaningful on verified rows"
        )
    print("no evals/baseline.json yet: nothing to gate on. Exit 0.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
