from __future__ import annotations

import argparse
import json
import pathlib
import re


POSITIVE_HINTS = {"strong", "interesting", "promising", "good", "solid"}
NEGATIVE_HINTS = {"unclear", "weak", "missing", "concern", "insufficient", "limited"}


def _reviewer_id(index: int, text: str) -> str:
    match = re.search(r"reviewer\s*([0-9]+)", text, re.IGNORECASE)
    if match:
        return f"R{match.group(1)}"
    return f"R{index + 1}"


def _sentiment(text: str) -> str:
    lowered = text.lower()
    pos = sum(word in lowered for word in POSITIVE_HINTS)
    neg = sum(word in lowered for word in NEGATIVE_HINTS)
    if neg > pos:
        return "negative"
    if pos > neg:
        return "positive"
    return "mixed"


def _movability(text: str, sentiment: str) -> str:
    lowered = text.lower()
    if sentiment == "positive":
        return "supportive"
    if (
        "unclear" in lowered
        or "please clarify" in lowered
        or "missing" in lowered
        or "insufficient" in lowered
        or "limited" in lowered
        or "weak" in lowered
    ):
        return "swing"
    return "fixed"


def _primary_concerns(text: str) -> list[str]:
    lowered = text.lower()
    concerns: list[str] = []
    mapping = [
        ("novelty", "novelty"),
        ("experiment", "empirical_support"),
        ("evidence", "empirical_support"),
        ("weak", "empirical_support"),
        ("insufficient", "empirical_support"),
        ("baseline", "baseline_comparison"),
        ("ablation", "missing_ablation"),
        ("clarify", "clarity"),
        ("writing", "clarity"),
        ("scope", "scope_mismatch"),
        ("limited", "scope_mismatch"),
        ("reproduc", "reproducibility"),
        ("theory", "theory"),
        ("proof", "theory"),
    ]
    for needle, label in mapping:
        if needle in lowered and label not in concerns:
            concerns.append(label)
    if not concerns:
        concerns.append("general_concern")
    return concerns


def build_reviewer_cards(reviews: list[dict[str, str]]) -> list[dict[str, object]]:
    cards: list[dict[str, object]] = []
    for index, review in enumerate(reviews):
        text = review["text"]
        sentiment = _sentiment(text)
        cards.append(
            {
                "reviewer_id": _reviewer_id(index, text),
                "sentiment": sentiment,
                "movability": _movability(text, sentiment),
                "primary_concerns": _primary_concerns(text),
                "attitude": "supportive" if sentiment == "positive" else "skeptical" if sentiment == "negative" else "mixed",
                "source_path": review.get("path"),
            }
        )
    return cards


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build reviewer cards from extracted review text.")
    parser.add_argument("reviews_json")
    args = parser.parse_args(argv)
    reviews = json.loads(pathlib.Path(args.reviews_json).read_text(encoding="utf-8"))
    print(json.dumps(build_reviewer_cards(reviews), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
