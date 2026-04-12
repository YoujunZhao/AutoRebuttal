from __future__ import annotations

import argparse
import pathlib
import re
import sys


LABEL_RE = re.compile(r"(?<!^)(?<!\n)\s+(?=(?:W|Q|M)\d+(?:[\.\):]|\s*\())")


def format_rebuttal_blocks(text: str) -> str:
    """Force reviewer labels like W1/Q1/M1 onto their own line."""
    return LABEL_RE.sub("\n", text)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Normalize rebuttal blocks so W/Q/M labels start on their own line."
    )
    parser.add_argument("input_file", nargs="?")
    args = parser.parse_args(argv)
    if args.input_file:
        source = pathlib.Path(args.input_file).read_text(encoding="utf-8")
    else:
        source = sys.stdin.read()
    sys.stdout.write(format_rebuttal_blocks(source))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
