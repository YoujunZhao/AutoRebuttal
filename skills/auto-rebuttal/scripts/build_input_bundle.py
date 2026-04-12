from __future__ import annotations

import argparse
import json
import pathlib
import sys


if __package__ in {None, ""}:
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from build_draft_bundle import build_draft_bundle


def build_input_bundle(
    *, paper_pdf: str | pathlib.Path, review_pdfs: list[str | pathlib.Path] | None = None
) -> dict[str, object]:
    bundle = build_draft_bundle(paper_pdf=paper_pdf, review_inputs=list(review_pdfs or []))
    paper_path = pathlib.Path(paper_pdf).expanduser().resolve()
    resolved_review_paths = [pathlib.Path(review_pdf).expanduser().resolve() for review_pdf in review_pdfs or []]
    bundle["source_files"] = {
        "paper_pdf": str(paper_path),
        "review_pdfs": [str(review_path) for review_path in resolved_review_paths],
    }
    return bundle


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
