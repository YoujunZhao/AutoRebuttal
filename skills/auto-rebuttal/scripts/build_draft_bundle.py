from __future__ import annotations

import argparse
import json
import pathlib
import sys


if __package__ in {None, ""}:
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from detect_input_artifact import detect_input_artifact
from detect_paper_artifact import detect_paper_artifact
from response_modes import resolve_auto_experiment, resolve_code_path, resolve_output_format


def build_draft_bundle(
    *,
    paper_input: str | pathlib.Path | None = None,
    paper_pdf: str | pathlib.Path | None = None,
    review_inputs: list[str | pathlib.Path] | None = None,
    output: str | None = None,
    autoexperiment: str | bool | None = None,
    code: str | pathlib.Path | bool | None = None,
) -> dict[str, object]:
    resolved_paper_input = paper_input if paper_input is not None else paper_pdf
    if resolved_paper_input is None:
        raise ValueError("A paper_input or paper_pdf value is required for draft mode.")
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
        "paper": detect_paper_artifact(resolved_paper_input),
        "reviews": reviews,
        "output_format": resolve_output_format(output=output),
        "auto_experiment": resolve_auto_experiment(autoexperiment=autoexperiment),
        "code": resolve_code_path(code=code),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build an AutoRebuttal draft bundle from a paper input and review inputs."
    )
    parser.add_argument("--paper-input")
    parser.add_argument("--paper-pdf")
    parser.add_argument("--review-input", action="append", default=[])
    parser.add_argument("--output")
    parser.add_argument("--autoexperiment")
    parser.add_argument("--code")
    args = parser.parse_args(argv)
    print(
        json.dumps(
            build_draft_bundle(
                paper_input=args.paper_input,
                paper_pdf=args.paper_pdf,
                review_inputs=args.review_input,
                output=args.output,
                autoexperiment=args.autoexperiment,
                code=args.code,
            ),
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
