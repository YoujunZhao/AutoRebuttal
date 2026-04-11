from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys


if __package__ in {None, ""}:
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from build_reviewer_outline import build_reviewer_outline


POSITIVE_HINTS = {"strong", "interesting", "promising", "good", "solid"}
NEGATIVE_HINTS = {"unclear", "weak", "missing", "concern", "insufficient", "limited"}


def _reviewer_id(index: int, text: str) -> str:
    match = re.search(r"reviewer\s*([a-z0-9]+)", text, re.IGNORECASE)
    if match:
        reviewer_token = match.group(1)
        if reviewer_token.isdigit():
            return f"R{reviewer_token}"
        return reviewer_token
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


def _outline_text(outline: dict[str, object]) -> str:
    parts: list[str] = []
    for key in ("weaknesses", "questions", "minor_points"):
        for item in outline.get(key, []):
            if isinstance(item, dict):
                text = item.get("text")
                if isinstance(text, str) and text:
                    parts.append(text)
    return " ".join(parts)


def build_reviewer_cards(reviews: list[dict[str, object]]) -> list[dict[str, object]]:
    cards: list[dict[str, object]] = []
    for index, review in enumerate(reviews):
        text = review.get("text") or ""
        reviewer_id = _reviewer_id(index, text)
        outline = review.get("outline")
        extraction_mode = str(review.get("extraction_mode", "text"))
        if extraction_mode == "image_fallback" and not text and not isinstance(outline, dict):
            raise ValueError(
                "Image-fallback reviews require image-derived text or a prebuilt outline before reviewer-card generation."
            )
        if not isinstance(outline, dict):
            outline = build_reviewer_outline(reviewer_id=reviewer_id, review_text=text)
        analysis_text = _outline_text(outline) or text
        sentiment = _sentiment(analysis_text)
        cards.append(
            {
                "reviewer_id": reviewer_id,
                "sentiment": sentiment,
                "movability": _movability(analysis_text, sentiment),
                "primary_concerns": _primary_concerns(analysis_text),
                "attitude": "supportive" if sentiment == "positive" else "skeptical" if sentiment == "negative" else "mixed",
                "source_path": review.get("path"),
                "outline": outline,
                "question_count": len(outline.get("questions", [])),
                "minor_point_count": len(outline.get("minor_points", [])),
                "source_mode": extraction_mode,
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
