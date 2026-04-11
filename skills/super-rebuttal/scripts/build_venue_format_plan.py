from __future__ import annotations

import argparse
import json


def build_venue_format_plan(venue: str) -> dict[str, object]:
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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build a venue-aware rebuttal formatting plan.")
    parser.add_argument("venue")
    args = parser.parse_args(argv)
    print(json.dumps(build_venue_format_plan(args.venue), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
