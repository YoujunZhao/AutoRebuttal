from __future__ import annotations

import argparse
import json
import pathlib


def build_style_plan(*, phase: str, mode: str, strategy_memo: dict[str, object]) -> dict[str, object]:
    opener_style = "short-global-opener"
    paragraph_rhythm = "one-strong-point-per-paragraph"
    if phase == "initial":
        opener_style = "brief-thanks-then-direct-answer"

    emphasis = []
    if strategy_memo.get("priority_reviewers"):
        emphasis.append("prioritize-swing-reviewers")
    if strategy_memo.get("shared_issues"):
        emphasis.append("lead-with-shared-issues")
    if not emphasis:
        emphasis.append("lead-with-clearest-clarification")

    return {
        "phase": phase,
        "mode": mode,
        "opener_style": opener_style,
        "paragraph_rhythm": paragraph_rhythm,
        "emphasis": emphasis,
        "avoid": [
            "repetitive-gratitude-loops",
            "broad-promises",
            "buried-answers",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build an initial rebuttal style plan.")
    parser.add_argument("--phase", default="initial")
    parser.add_argument("--mode", required=True)
    parser.add_argument("strategy_memo_json")
    args = parser.parse_args(argv)
    strategy_memo = json.loads(pathlib.Path(args.strategy_memo_json).read_text(encoding="utf-8"))
    print(json.dumps(build_style_plan(phase=args.phase, mode=args.mode, strategy_memo=strategy_memo), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
