from __future__ import annotations

import argparse
import json
import pathlib
import sys


if __package__ in {None, ""}:
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from detect_input_artifact import detect_input_artifact
from extract_pdf_text import extract_pdf_text


def build_draft_bundle(
    *,
    paper_pdf: str | pathlib.Path,
    review_inputs: list[str | pathlib.Path] | None = None,
) -> dict[str, object]:
    paper_path = pathlib.Path(paper_pdf).expanduser().resolve()
    reviews = [
        detect_input_artifact(
            review_input,
            index=index,
            allow_pdf_image_fallback=True,
            temp_prefix="autorebuttal_review_pages_",
        )
        for index, review_input in enumerate(review_inputs or [])
    ]
    return {
        "paper": {
            "source_type": "pdf",
            "path": str(paper_path),
            "text": extract_pdf_text(paper_path),
        },
        "reviews": reviews,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build an AutoRebuttal draft bundle from a paper PDF and review inputs."
    )
    parser.add_argument("--paper-pdf", required=True)
    parser.add_argument("--review-input", action="append", default=[])
    args = parser.parse_args(argv)
    print(
        json.dumps(
            build_draft_bundle(
                paper_pdf=args.paper_pdf,
                review_inputs=args.review_input,
            ),
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
