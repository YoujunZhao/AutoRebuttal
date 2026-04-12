from __future__ import annotations

import argparse
import json
import pathlib
import sys


if __package__ in {None, ""}:
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from detect_input_artifact import detect_input_artifact
from extract_pdf_text import extract_pdf_text


def build_revision_bundle(
    *,
    rebuttal_input: str | pathlib.Path,
    paper_pdf: str | pathlib.Path | None,
) -> dict[str, object]:
    rebuttal = detect_input_artifact(
        rebuttal_input,
        index=0,
        allow_pdf_image_fallback=False,
        temp_prefix="autorebuttal_rebuttal_pages_",
    )
    paper = None
    if paper_pdf is not None:
        paper_path = pathlib.Path(paper_pdf).expanduser().resolve()
        paper = {
            "source_type": "pdf",
            "path": str(paper_path),
            "text": extract_pdf_text(paper_path),
        }
    return {
        "rebuttal": rebuttal,
        "paper": paper,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build an AutoRebuttal revision bundle from an existing rebuttal and optional paper PDF."
    )
    parser.add_argument("--rebuttal-input", required=True)
    parser.add_argument("--paper-pdf")
    args = parser.parse_args(argv)
    print(
        json.dumps(
            build_revision_bundle(
                rebuttal_input=args.rebuttal_input,
                paper_pdf=args.paper_pdf,
            ),
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
