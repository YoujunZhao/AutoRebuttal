from __future__ import annotations

import argparse
import json
import pathlib
from typing import Any


def _slug(value: str) -> str:
    return "".join(char.lower() if char.isalnum() else "-" for char in value).strip("-")


def build_experiment_packets(
    requests: list[dict[str, Any]],
    *,
    default_command: str = "",
    working_dir: str = ".",
    launcher: str = "local",
) -> list[dict[str, Any]]:
    packets: list[dict[str, Any]] = []
    for index, request in enumerate(requests, start=1):
        request_id = str(request.get("id") or f"request-{index}")
        experiment_type = str(
            request.get("experiment_type") or request.get("request_type") or "other"
        )
        packets.append(
            {
                "packet_id": f"{request_id}-{_slug(experiment_type)}",
                "request_id": request_id,
                "hypothesis": request.get("claim_to_support")
                or request.get("needed_evidence")
                or "Author must fill the measured hypothesis before running.",
                "command": default_command,
                "working_dir": working_dir,
                "launcher": launcher,
                "timeout_minutes": 120,
                "metric": {
                    "name": "metric",
                    "direction": "higher",
                    "parser": "json",
                    "source": "outputs/metrics.json",
                    "key": "metric",
                },
                "baseline": {"command": "", "metric_value": None},
                "success_condition": "Metric is parsed from a real result file and improves over baseline when a baseline is defined.",
                "allowed_files": ["configs/", "scripts/", "eval/"],
                "forbidden_files": ["data/", "paper/main.tex"],
                "output_files": ["outputs/metrics.json", "logs/run.log"],
                "rebuttal_usage": "short table + one sentence",
                "rollback_on_failure": True,
                "status": "needs_author_mapping" if not default_command else "runnable",
            }
        )
    return packets


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build draft experiment packets from requests.")
    parser.add_argument("--requests", required=True, help="JSON file containing requests or a bundle.")
    parser.add_argument("--command", default="")
    parser.add_argument("--working-dir", default=".")
    parser.add_argument("--launcher", choices=("local", "slurm"), default="local")
    args = parser.parse_args(argv)

    data = json.loads(pathlib.Path(args.requests).read_text(encoding="utf-8"))
    if isinstance(data, dict) and "requests" in data:
        requests = data["requests"]
    elif isinstance(data, dict):
        requests = [data]
    else:
        requests = data
    print(
        json.dumps(
            {
                "schema_version": "0.1",
                "packets": build_experiment_packets(
                    list(requests),
                    default_command=args.command,
                    working_dir=args.working_dir,
                    launcher=args.launcher,
                ),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
