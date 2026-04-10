from __future__ import annotations

import argparse
import json
import pathlib
import sys


if __package__ in {None, ""}:
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from extract_pdf_text import extract_pdf_text


def build_input_bundle(
    *, paper_pdf: str | pathlib.Path, review_pdfs: list[str | pathlib.Path] | None = None
) -> dict[str, object]:
    paper_path = pathlib.Path(paper_pdf).resolve()
    resolved_review_paths = [pathlib.Path(review_pdf).resolve() for review_pdf in review_pdfs or []]

    return {
        "paper": {
            "path": str(paper_path),
            "text": extract_pdf_text(paper_path),
        },
        "reviews": [
            {
                "path": str(review_path),
                "text": extract_pdf_text(review_path),
            }
            for review_path in resolved_review_paths
        ],
        "source_files": {
            "paper_pdf": str(paper_path),
            "review_pdfs": [str(review_path) for review_path in resolved_review_paths],
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build a JSON input bundle from a paper PDF and optional review PDFs."
    )
    parser.add_argument("--paper-pdf", required=True)
    parser.add_argument("--review-pdf", action="append", default=[])
    args = parser.parse_args(argv)
    print(
        json.dumps(
            build_input_bundle(paper_pdf=args.paper_pdf, review_pdfs=args.review_pdf),
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
