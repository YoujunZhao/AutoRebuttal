from __future__ import annotations

import argparse
import json
import pathlib
import re


SECTION_HEADERS = {
    "weaknesses": ("weaknesses", "major weaknesses", "main weaknesses"),
    "questions": ("questions", "question"),
    "minor": ("minor weaknesses", "minor weakness", "minor comments", "minor points"),
}


def _normalize_line(line: str) -> str:
    return " ".join(line.strip().split())


def _label(prefix: str, index: int) -> str:
    return f"{prefix}{index}"


def build_reviewer_outline(*, reviewer_id: str, review_text: str) -> dict[str, object]:
    current_section = "weaknesses"
    weaknesses: list[dict[str, str]] = []
    questions: list[dict[str, str]] = []
    minor_points: list[dict[str, str]] = []

    for raw_line in review_text.splitlines():
        line = _normalize_line(raw_line)
        if not line:
            continue
        lowered = line.lower().rstrip(":")

        if lowered in SECTION_HEADERS["weaknesses"]:
            current_section = "weaknesses"
            continue
        if lowered in SECTION_HEADERS["questions"]:
            current_section = "questions"
            continue
        if lowered in SECTION_HEADERS["minor"]:
            current_section = "minor"
            continue

        line = re.sub(r"^[\-\*\d\.\)\(]+\s*", "", line)
        if current_section == "questions":
            questions.append({"label": _label("Q", len(questions) + 1), "text": line})
        elif current_section == "minor":
            minor_points.append({"label": _label("M", len(minor_points) + 1), "text": line})
        else:
            weaknesses.append({"label": _label("W", len(weaknesses) + 1), "text": line})

    return {
        "reviewer_id": reviewer_id,
        "weaknesses": weaknesses,
        "questions": questions,
        "minor_points": minor_points,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build a reviewer outline with W/Q/M sections.")
    parser.add_argument("--reviewer-id", required=True)
    parser.add_argument("review_text_file")
    args = parser.parse_args(argv)
    review_text = pathlib.Path(args.review_text_file).read_text(encoding="utf-8")
    print(json.dumps(build_reviewer_outline(reviewer_id=args.reviewer_id, review_text=review_text), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
