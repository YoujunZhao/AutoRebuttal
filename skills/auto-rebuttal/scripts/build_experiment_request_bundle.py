from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys


if __package__ in {None, ""}:
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from detect_input_artifact import detect_input_artifact
from response_modes import resolve_auto_experiment


_REQUEST_PATTERNS = (
    ("comparison", ("baseline", "compare", "comparison", "against")),
    ("ablation", ("ablation", "ablate")),
    ("additional_experiment", ("experiment", "evaluation", "benchmark")),
)
_WORKSPACE_MARKERS = (
    "pyproject.toml",
    "requirements.txt",
    "setup.py",
    "Makefile",
    "environment.yml",
    "environment.yaml",
    "Dockerfile",
)
_RUNNABLE_SCRIPT_PATTERNS = ("*.py", "*.sh", "*.bat")


def _normalize_review(
    review: dict[str, object] | str | pathlib.Path,
    *,
    index: int,
) -> dict[str, object]:
    if isinstance(review, dict):
        return dict(review)
    return detect_input_artifact(
        review,
        index=index,
        allow_pdf_image_fallback=True,
        temp_prefix="autorebuttal_experiment_review_pages_",
    )


def _extract_reviewer_label(text: str) -> str | None:
    match = re.search(r"\bReviewer\s+([^\n:]+)", text, re.IGNORECASE)
    if match is None:
        return None
    return match.group(0).strip()


def _iter_sentences(text: str) -> list[str]:
    return [
        sentence.strip(" \t\r\n-:*")
        for sentence in re.split(r"(?<=[.!?])\s+|\n+", text)
        if sentence.strip()
    ]


def _looks_like_request(sentence: str) -> bool:
    lowered = sentence.lower()
    return any(
        token in lowered
        for token in (
            "please",
            "can you",
            "could you",
            "would you",
            "add ",
            "include ",
            "compare",
            "run ",
            "ablation",
            "experiment",
        )
    )


def _extract_requests(reviews: list[dict[str, object]]) -> list[dict[str, object]]:
    requests: list[dict[str, object]] = []
    seen: set[tuple[str, str]] = set()

    for review_index, review in enumerate(reviews):
        text = str(review.get("text") or "").strip()
        if not text:
            continue

        reviewer = _extract_reviewer_label(text)
        for sentence in _iter_sentences(text):
            if not _looks_like_request(sentence):
                continue

            lowered = sentence.lower()
            for request_type, keywords in _REQUEST_PATTERNS:
                if not any(keyword in lowered for keyword in keywords):
                    continue

                marker = (request_type, sentence)
                if marker in seen:
                    continue
                seen.add(marker)
                requests.append(
                    {
                        "request_type": request_type,
                        "review_index": review_index,
                        "reviewer": reviewer,
                        "request_text": sentence,
                    }
                )

    return requests


def _resolve_workspace(workspace: str | pathlib.Path | None) -> pathlib.Path | None:
    if workspace is None:
        return None
    candidate = pathlib.Path(str(workspace)).expanduser()
    if not candidate.exists():
        return candidate
    return candidate.resolve()


def _workspace_is_runnable(workspace: pathlib.Path | None) -> bool:
    if workspace is None or not workspace.exists():
        return False

    root = workspace if workspace.is_dir() else workspace.parent
    if any((root / marker).exists() for marker in _WORKSPACE_MARKERS):
        return True
    return any(root.glob(pattern) for pattern in _RUNNABLE_SCRIPT_PATTERNS)


def _workspace_blockers(
    *,
    workspace: pathlib.Path | None,
    workspace_ready: bool,
    requests: list[dict[str, object]],
) -> list[str]:
    if not requests or workspace_ready:
        return []
    if workspace is None:
        return [
            "No experiment workspace was provided, so supplementary experiment requests cannot be run."
        ]
    if not workspace.exists():
        return [f"Experiment workspace path does not exist: {workspace}"]
    return [
        "The provided experiment workspace does not look runnable; expected a project marker or executable script."
    ]


def build_experiment_request_bundle(
    *,
    reviews: list[dict[str, object] | str | pathlib.Path] | None = None,
    auto_experiment: str | bool | None = None,
    workspace: str | pathlib.Path | None = None,
) -> dict[str, object]:
    normalized_reviews = [
        _normalize_review(review, index=index) for index, review in enumerate(reviews or [])
    ]
    requests = _extract_requests(normalized_reviews)
    resolved_workspace = _resolve_workspace(workspace)
    workspace_ready = _workspace_is_runnable(resolved_workspace)
    return {
        "reviews": normalized_reviews,
        "requests": requests,
        "auto_experiment": resolve_auto_experiment(autoexperiment=auto_experiment),
        "workspace": None if resolved_workspace is None else str(resolved_workspace),
        "workspace_ready": workspace_ready,
        "blockers": _workspace_blockers(
            workspace=resolved_workspace,
            workspace_ready=workspace_ready,
            requests=requests,
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build an AutoRebuttal experiment request bundle from review inputs."
    )
    parser.add_argument("--review-input", action="append", default=[])
    parser.add_argument("--workspace")
    parser.add_argument("--autoexperiment")
    args = parser.parse_args(argv)
    print(
        json.dumps(
            build_experiment_request_bundle(
                reviews=args.review_input,
                auto_experiment=args.autoexperiment,
                workspace=args.workspace,
            ),
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
