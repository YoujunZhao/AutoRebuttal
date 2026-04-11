from __future__ import annotations

import argparse
import json
import pathlib
from collections import Counter


def build_strategy_memo(reviewer_cards: list[dict[str, object]]) -> dict[str, object]:
    counts: Counter[str] = Counter()
    priority_reviewers: list[str] = []

    for card in reviewer_cards:
        for concern in card.get("primary_concerns", []):
            counts[str(concern)] += 1
        if card.get("movability") == "swing":
            priority_reviewers.append(str(card.get("reviewer_id")))

    shared_issues = sorted(
        [concern for concern, count in counts.items() if count > 1],
        key=lambda item: (-counts[item], item),
    )

    global_strategy: list[str] = []
    if shared_issues:
        global_strategy.append("Lead with the highest-leverage shared issues before reviewer-specific details.")
    if priority_reviewers:
        global_strategy.append(f"Prioritize swing reviewers first: {', '.join(priority_reviewers)}.")
    if not global_strategy:
        global_strategy.append("Open with the clearest shared clarification and keep replies concrete.")

    return {
        "shared_issues": shared_issues,
        "priority_reviewers": priority_reviewers,
        "global_strategy": global_strategy,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build a strategy memo from reviewer cards.")
    parser.add_argument("reviewer_cards_json")
    args = parser.parse_args(argv)
    reviewer_cards = json.loads(pathlib.Path(args.reviewer_cards_json).read_text(encoding="utf-8"))
    print(json.dumps(build_strategy_memo(reviewer_cards), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
