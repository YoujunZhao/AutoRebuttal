from __future__ import annotations

import argparse
import json
import pathlib
import re


HEADER_PATTERNS = {
    "ignore": (
        r"summary",
        r"strengths and weaknesses",
        r"strengths",
        r"limitations",
        r"soundness",
        r"presentation",
        r"significance",
        r"originality",
        r"overall recommendation",
        r"confidence",
        r"compliance with .*policy",
        r"code of conduct acknowledgement",
        r"ethics review",
    ),
    "weaknesses": (
        r"weaknesses",
        r"main weaknesses",
        r"major weaknesses",
        r"weakness",
    ),
    "questions": (
        r"questions",
        r"question",
        r"key questions for authors",
        r"questions for authors",
    ),
    "minor": (
        r"minor weaknesses",
        r"minor weakness",
        r"minor comments",
        r"minor comment",
        r"minor points",
        r"minor concerns",
    ),
}

ITEM_PREFIX_RE = re.compile(r"^(?:[\-\*\u2022]\s+|\(?\d+[\.\)]\s+)")
INLINE_HEADER_TOKENS = [
    "Strengths And Weaknesses",
    "Strengths",
    "Main Weaknesses",
    "Major Weaknesses",
    "Weaknesses",
    "Key Questions For Authors",
    "Questions For Authors",
    "Questions",
    "Question",
    "Minor Weaknesses",
    "Minor Weakness",
    "Minor Comments",
    "Minor Comment",
    "Minor Points",
    "Minor Concerns",
    "Summary",
    "Limitations",
    "Overall Recommendation",
    "Confidence",
    "Soundness",
    "Presentation",
    "Significance",
    "Originality",
]
INLINE_HEADER_RE = re.compile(
    rf"(?<=[\.\?\!])\s+(?=(?:{'|'.join(re.escape(token) for token in INLINE_HEADER_TOKENS)})\s*:?)",
    re.IGNORECASE,
)


def _normalize_line(line: str) -> str:
    return " ".join(line.strip().split())


def _label(prefix: str, index: int) -> str:
    return f"{prefix}{index}"


def _expand_inline_headers(review_text: str) -> str:
    return INLINE_HEADER_RE.sub("\n", review_text)


def _match_header(line: str) -> tuple[str, str] | None:
    for section, patterns in HEADER_PATTERNS.items():
        for pattern in patterns:
            match = re.match(rf"^(?:{pattern})\s*:?\s*(.*)$", line, flags=re.IGNORECASE)
            if match:
                return section, match.group(1).strip()
    return None


def _is_item_start(raw_line: str) -> bool:
    return bool(ITEM_PREFIX_RE.match(raw_line.strip()))


def _clean_item_text(line: str) -> str:
    return ITEM_PREFIX_RE.sub("", line).strip()


def _append_item(
    items: list[dict[str, str]],
    *,
    prefix: str,
    text: str,
    is_new_item: bool,
) -> None:
    if not text:
        return
    if not items or is_new_item:
        items.append({"label": _label(prefix, len(items) + 1), "text": text})
        return
    items[-1]["text"] = f"{items[-1]['text']} {text}".strip()


def build_reviewer_outline(*, reviewer_id: str, review_text: str) -> dict[str, object]:
    current_section = "weaknesses"
    weaknesses: list[dict[str, str]] = []
    questions: list[dict[str, str]] = []
    minor_points: list[dict[str, str]] = []

    expanded_text = _expand_inline_headers(review_text)
    for raw_line in expanded_text.splitlines():
        line = _normalize_line(raw_line)
        if not line:
            continue

        header_match = _match_header(line)
        if header_match is not None:
            header_section, remainder = header_match
            current_section = header_section
            if header_section == "ignore" or not remainder:
                continue
            line = remainder
            raw_line = remainder

        clean_text = _clean_item_text(line)
        is_new_item = _is_item_start(raw_line) or header_match is not None
        if current_section == "ignore":
            continue

        if current_section == "questions":
            _append_item(questions, prefix="Q", text=clean_text, is_new_item=is_new_item)
        elif current_section == "minor":
            _append_item(minor_points, prefix="M", text=clean_text, is_new_item=is_new_item)
        elif current_section == "weaknesses":
            _append_item(weaknesses, prefix="W", text=clean_text, is_new_item=is_new_item)

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
