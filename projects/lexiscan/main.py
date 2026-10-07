"""Train LexiScan on the bundled ticket dataset and classify text from the CLI.

Usage:
    uv run python main.py "The app crashes every time I log in"
    uv run python main.py --threshold 60 "I was charged twice this month"
    echo "Where is my return label?" | uv run python main.py
"""

import argparse
import os
import sys
from pathlib import Path

from lexiscan import LexiModel

DEFAULT_DATA_PATH = Path(__file__).parent / "data" / "enterprise_tickets.csv"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Route text to a department with a confidence score."
    )
    parser.add_argument("text", nargs="*", help="Text to classify (reads stdin if omitted)")
    parser.add_argument(
        "--data",
        default=os.getenv("LEXISCAN_DATA_PATH", str(DEFAULT_DATA_PATH)),
        help="Labelled CSV with `ticket_text` and `department` columns",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=50,
        help="Minimum confidence (%%) before a prediction is returned instead of Unknown",
    )
    parser.add_argument(
        "--bow", action="store_true", help="Use raw Bag-of-Words counts instead of TF-IDF"
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    text = " ".join(args.text).strip() or sys.stdin.read().strip()
    if not text:
        print("No input text provided.", file=sys.stderr)
        return 1

    model = LexiModel(use_tfidf=not args.bow)
    model.train(data_path=args.data, text_column="ticket_text", label_column="department")

    result = model.predict(text, threshold=args.threshold)
    print(f"{result['category']} ({result['confidence']}%)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
