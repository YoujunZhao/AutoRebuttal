from __future__ import annotations

import argparse
import json
import pathlib


def build_latex_output_package(
    *,
    rebuttal_text: str,
    revised_latex_paper: str,
    entrypoint: str,
) -> dict[str, object]:
    return {
        "output_mode": "latex-dual",
        "rebuttal_text": rebuttal_text,
        "revised_latex_paper": revised_latex_paper,
        "entrypoint": entrypoint,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build a dual AutoRebuttal output package for LaTeX workflows.")
    parser.add_argument("--rebuttal-file", required=True)
    parser.add_argument("--latex-file", required=True)
    parser.add_argument("--entrypoint", required=True)
    args = parser.parse_args(argv)
    rebuttal_text = pathlib.Path(args.rebuttal_file).read_text(encoding="utf-8")
    revised_latex_paper = pathlib.Path(args.latex_file).read_text(encoding="utf-8")
    print(
        json.dumps(
            build_latex_output_package(
                rebuttal_text=rebuttal_text,
                revised_latex_paper=revised_latex_paper,
                entrypoint=args.entrypoint,
            ),
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
