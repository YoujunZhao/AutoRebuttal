from __future__ import annotations

import argparse
import json


def _base_plan(venue: str) -> dict[str, object]:
    normalized = venue.strip().upper()

    if normalized == "ICLR":
        return {
            "venue": normalized,
            "global_summary": True,
            "budget_mode": "per-reviewer",
            "default_per_reviewer_limit": None,
            "weakness_prefix": "W",
        }
    if normalized == "ICML":
        return {
            "venue": normalized,
            "global_summary": False,
            "budget_mode": "per-reviewer",
            "default_per_reviewer_limit": 5000,
            "weakness_prefix": "W",
        }
    if normalized == "NEURIPS":
        return {
            "venue": normalized,
            "global_summary": False,
            "budget_mode": "per-reviewer",
            "default_per_reviewer_limit": 10000,
            "weakness_prefix": "W",
        }
    if normalized == "AAAI":
        return {
            "venue": normalized,
            "global_summary": False,
            "budget_mode": "per-reviewer",
            "default_per_reviewer_limit": 2500,
            "weakness_prefix": "W",
        }
    if normalized == "IEEE":
        return {
            "venue": normalized,
            "global_summary": False,
            "budget_mode": "per-reviewer",
            "default_per_reviewer_limit": None,
            "weakness_prefix": "W",
        }
    if normalized in {"CVPR", "ICCV", "ECCV"}:
        return {
            "venue": normalized,
            "global_summary": True,
            "budget_mode": "cv-one-page",
            "default_per_reviewer_limit": None,
            "weakness_prefix": "W",
        }
    return {
        "venue": normalized,
        "global_summary": False,
        "budget_mode": "generic",
        "default_per_reviewer_limit": None,
        "weakness_prefix": "W",
    }


def build_venue_format_plan(
    venue: str,
    *,
    per_reviewer_limit: int | None = None,
    total_limit: int | None = None,
    global_summary: bool | None = None,
) -> dict[str, object]:
    plan = _base_plan(venue)
    source = "default"

    if per_reviewer_limit is not None:
        plan["budget_mode"] = "per-reviewer"
        plan["default_per_reviewer_limit"] = per_reviewer_limit
        source = "user-override"
    elif total_limit is not None:
        plan["budget_mode"] = "shared-global"
        plan["default_total_limit"] = total_limit
        source = "user-override"

    if global_summary is not None:
        plan["global_summary"] = global_summary
        source = "user-override"

    plan["source"] = source
    return plan


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build a venue-aware rebuttal formatting plan.")
    parser.add_argument("venue")
    parser.add_argument("--per-reviewer-limit", type=int)
    parser.add_argument("--total-limit", type=int)
    parser.add_argument("--global-summary", choices=("true", "false"))
    args = parser.parse_args(argv)
    global_summary = None
    if args.global_summary == "true":
        global_summary = True
    elif args.global_summary == "false":
        global_summary = False
    print(
        json.dumps(
            build_venue_format_plan(
                args.venue,
                per_reviewer_limit=args.per_reviewer_limit,
                total_limit=args.total_limit,
                global_summary=global_summary,
            ),
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
