"""Unit tests for the LexiScan classifier — trains on a tiny in-memory dataset."""

import pandas as pd
import pytest
from lexiscan import LexiModel


@pytest.fixture
def trained_model(tmp_path):
    """Train a small model on a throwaway CSV so tests need no data files."""
    rows = [
        ("my invoice was charged twice please refund", "Billing"),
        ("the payment did not go through on my card", "Billing"),
        ("i was double charged for my subscription", "Billing"),
        ("the app crashes every time i open it", "Technical"),
        ("i cannot log in it says invalid password", "Technical"),
        ("the screen freezes after the login page", "Technical"),
    ]
    csv = tmp_path / "tickets.csv"
    pd.DataFrame(rows, columns=["ticket_text", "department"]).to_csv(csv, index=False)

    model = LexiModel(use_tfidf=True)
    model.train(data_path=str(csv), text_column="ticket_text", label_column="department")
    return model


def test_predict_returns_expected_shape(trained_model):
    result = trained_model.predict("I want a refund for a duplicate charge")
    assert set(result) == {"category", "confidence"}
    assert 0.0 <= result["confidence"] <= 100.0


def test_predict_routes_billing(trained_model):
    result = trained_model.predict("please refund the duplicate charge on my invoice")
    assert result["category"] == "Billing"


def test_low_confidence_returns_unknown(trained_model):
    # An unrelated query should fall below a high threshold and route to Unknown
    result = trained_model.predict("what are your store opening hours", threshold=99)
    assert result["category"] == "Unknown"
