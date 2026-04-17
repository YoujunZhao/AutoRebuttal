from __future__ import annotations

import argparse
import json
import pathlib
import sys


if __package__ in {None, ""}:
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from detect_input_artifact import detect_input_artifact
from detect_paper_artifact import detect_paper_artifact
from response_modes import resolve_auto_experiment, resolve_output_format


def build_revision_bundle(
    *,
    rebuttal_input: str | pathlib.Path,
    paper_input: str | pathlib.Path | None = None,
    paper_pdf: str | pathlib.Path | None = None,
    output: str | None = None,
    autoexperiment: str | bool | None = None,
) -> dict[str, object]:
    rebuttal = detect_input_artifact(
        rebuttal_input,
        index=0,
        allow_pdf_image_fallback=False,
        temp_prefix="autorebuttal_rebuttal_pages_",
    )
    paper = None
    resolved_paper_input = paper_input if paper_input is not None else paper_pdf
    if resolved_paper_input is not None:
        paper = detect_paper_artifact(resolved_paper_input)
    return {
        "rebuttal": rebuttal,
        "paper": paper,
        "output_format": resolve_output_format(output=output),
        "auto_experiment": resolve_auto_experiment(autoexperiment=autoexperiment),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build an AutoRebuttal revision bundle from an existing rebuttal and optional paper input."
    )
    parser.add_argument("--rebuttal-input", required=True)
    parser.add_argument("--paper-input")
    parser.add_argument("--paper-pdf")
    parser.add_argument("--output")
    parser.add_argument("--autoexperiment")
    args = parser.parse_args(argv)
    print(
        json.dumps(
            build_revision_bundle(
                rebuttal_input=args.rebuttal_input,
                paper_input=args.paper_input,
                paper_pdf=args.paper_pdf,
                output=args.output,
                autoexperiment=args.autoexperiment,
            ),
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
