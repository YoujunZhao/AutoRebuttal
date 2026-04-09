from __future__ import annotations

import argparse
import json


def measure_budget(text: str, limit: int, mode: str = "chars") -> dict[str, int | bool | str]:
    """Measure used and remaining budget for text in either chars or words."""
    if mode not in {"chars", "words"}:
        raise ValueError(f"Unsupported mode: {mode}")

    used = len(text) if mode == "chars" else len(text.split())
    remaining = limit - used
    return {
        "mode": mode,
        "limit": limit,
        "used": used,
        "remaining": remaining,
        "overflow": remaining < 0,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Measure a rebuttal text budget.")
    parser.add_argument("--text", required=True)
    parser.add_argument("--limit", required=True, type=int)
    parser.add_argument("--mode", default="chars")
    args = parser.parse_args(argv)
    print(json.dumps(measure_budget(args.text, args.limit, args.mode), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
