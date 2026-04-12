from __future__ import annotations

import argparse
import json


def allocate_budget(
    *,
    mode: str,
    reviewer_count: int,
    per_reviewer_limit: int | None,
    total_limit: int | None,
) -> dict[str, object]:
    if mode == "per-reviewer":
        if per_reviewer_limit is None:
            raise ValueError("per_reviewer_limit is required for per-reviewer mode")
        opener = int(per_reviewer_limit * 0.12)
        closing = int(per_reviewer_limit * 0.08)
        reviewer_body = per_reviewer_limit - opener - closing
        return {
            "mode": mode,
            "per_reviewer_limit": per_reviewer_limit,
            "reviewer_count": reviewer_count,
            "section_plan": {
                "opener": opener,
                "reviewer_body": reviewer_body,
                "closing": closing,
            },
        }

    if mode == "shared-global":
        if total_limit is None:
            raise ValueError("total_limit is required for shared-global mode")
        opener = int(total_limit * 0.10)
        closing = int(total_limit * 0.08)
        shared_body = total_limit - opener - closing
        per_reviewer = shared_body // reviewer_count if reviewer_count > 0 else 0
        remainder = shared_body - (per_reviewer * reviewer_count)
        reviewer_sections = [per_reviewer for _ in range(reviewer_count)]
        for index in range(remainder):
            reviewer_sections[index] += 1
        return {
            "mode": mode,
            "total_limit": total_limit,
            "reviewer_count": reviewer_count,
            "section_plan": {
                "opener": opener,
                "shared_body": shared_body,
                "closing": closing,
            },
            "reviewer_sections": reviewer_sections,
        }

    raise ValueError(f"Unsupported mode: {mode}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Allocate rebuttal character budget.")
    parser.add_argument("--mode", required=True, choices=("per-reviewer", "shared-global"))
    parser.add_argument("--reviewer-count", required=True, type=int)
    parser.add_argument("--per-reviewer-limit", type=int)
    parser.add_argument("--total-limit", type=int)
    args = parser.parse_args(argv)
    print(
        json.dumps(
            allocate_budget(
                mode=args.mode,
                reviewer_count=args.reviewer_count,
                per_reviewer_limit=args.per_reviewer_limit,
                total_limit=args.total_limit,
            ),
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
