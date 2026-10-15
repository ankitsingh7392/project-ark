"""The golden set is data the eval depends on, so it is tested like code."""

from pathlib import Path

import pytest
from evals.golden import TARGET_MIX, GoldenRow, load, mix

GOLDEN = Path(__file__).resolve().parents[2] / "data" / "golden_set.jsonl"


def test_every_row_validates():
    rows = load(GOLDEN)
    assert rows, "golden set is empty"


def test_unanswerable_rows_have_no_sources():
    for r in load(GOLDEN):
        if r.category == "unanswerable":
            assert r.sources == [], r.id


def test_answerable_rows_cite_a_document():
    for r in load(GOLDEN):
        if r.category != "unanswerable":
            assert r.sources and all(s.document for s in r.sources), r.id


def test_mix_is_checked_once_set_is_large_enough():
    rows = load(GOLDEN)
    if len(rows) < 150:
        pytest.skip(f"mix enforced from 150 rows; have {len(rows)}")
    for cat, share in mix(rows).items():
        assert abs(share - TARGET_MIX[cat]) <= 0.05, cat


def test_duplicate_ids_rejected(tmp_path: Path):
    row = GoldenRow.model_validate_json(GOLDEN.read_text().splitlines()[0]).model_dump_json()
    p = tmp_path / "dup.jsonl"
    p.write_text(row + "\n" + row + "\n")
    with pytest.raises(ValueError, match="duplicate"):
        load(p)
