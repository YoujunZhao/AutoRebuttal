from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import sys
import tempfile


if __package__ in {None, ""}:
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from extract_pdf_text import extract_pdf_text
from render_review_pdf_pages import render_review_pdf_pages


def _render_bucket(root: pathlib.Path, review_path: pathlib.Path, index: int) -> pathlib.Path:
    digest = hashlib.sha1(str(review_path).encode("utf-8")).hexdigest()[:10]
    return root / f"{index + 1:02d}_{review_path.stem}_{digest}"


def build_input_bundle(
    *, paper_pdf: str | pathlib.Path, review_pdfs: list[str | pathlib.Path] | None = None
) -> dict[str, object]:
    paper_path = pathlib.Path(paper_pdf).resolve()
    resolved_review_paths = [pathlib.Path(review_pdf).resolve() for review_pdf in review_pdfs or []]
    tmp_root = pathlib.Path(tempfile.mkdtemp(prefix="superrebuttal_review_pages_"))

    reviews = []
    for index, review_path in enumerate(resolved_review_paths):
        try:
            reviews.append(
                {
                    "path": str(review_path),
                    "text": extract_pdf_text(review_path),
                    "page_images": [],
                    "extraction_mode": "text",
                }
            )
        except ValueError:
            reviews.append(
                {
                    "path": str(review_path),
                    "text": None,
                    "page_images": render_review_pdf_pages(
                        pdf_path=review_path,
                        output_dir=_render_bucket(tmp_root, review_path, index),
                    ),
                    "extraction_mode": "image_fallback",
                }
            )

    return {
        "paper": {
            "path": str(paper_path),
            "text": extract_pdf_text(paper_path),
        },
        "reviews": reviews,
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
