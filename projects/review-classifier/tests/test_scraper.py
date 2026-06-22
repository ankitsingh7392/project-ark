"""Smoke tests for the review scraper — pure helpers only, no network/browser."""

import csv

from scraper import review_url, write_csv


def test_review_url_paginates():
    assert review_url(1).endswith("page=1")
    assert review_url(7).endswith("page=7")


def test_write_csv_roundtrip(tmp_path):
    rows = [["Widget", "great product"], ["Widget", "works well"]]
    out = tmp_path / "reviews.csv"
    write_csv(rows, str(out))

    with open(out, encoding="utf-8") as f:
        parsed = list(csv.reader(f))

    assert parsed[0] == ["product_name", "review"]
    assert parsed[1:] == rows
