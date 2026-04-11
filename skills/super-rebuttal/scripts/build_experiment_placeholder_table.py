from __future__ import annotations

import argparse


def build_experiment_placeholder_table(*, title: str, rows: list[str]) -> str:
    header = (
        f"### {title}\n\n"
        "| setting | metric | current evidence | rebuttal-added result | note |\n"
        "| --- | --- | --- | --- | --- |\n"
    )
    body = [f"| {row} | metric | existing evidence | XX | interpretation |" for row in rows]
    return header + "\n".join(body) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build an experiment placeholder table.")
    parser.add_argument("--title", required=True)
    parser.add_argument("rows", nargs="+")
    args = parser.parse_args(argv)
    print(build_experiment_placeholder_table(title=args.title, rows=args.rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
