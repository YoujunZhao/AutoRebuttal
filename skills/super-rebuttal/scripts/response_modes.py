from __future__ import annotations


def resolve_response_mode(
    *,
    venue: str | None,
    per_reviewer_limit: int | None,
    total_limit: int | None,
    shared_response: bool,
) -> dict[str, object]:
    if per_reviewer_limit is not None:
        return {
            "mode": "per-reviewer",
            "reason": "explicit per-reviewer limit",
            "limit": per_reviewer_limit,
            "venue": venue,
        }
    if shared_response or total_limit is not None:
        return {
            "mode": "shared-global",
            "reason": "shared response or explicit total limit",
            "limit": total_limit,
            "venue": venue,
        }
    return {
        "mode": "needs-user-budget",
        "reason": "no verified venue-specific format or explicit limit",
        "limit": None,
        "venue": venue,
    }
