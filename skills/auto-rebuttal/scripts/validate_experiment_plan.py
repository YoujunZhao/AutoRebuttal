from __future__ import annotations

import argparse
import json
import pathlib
from typing import Any


PACKET_REQUIRED_FIELDS = (
    "packet_id",
    "request_id",
    "hypothesis",
    "command",
    "working_dir",
    "launcher",
    "timeout_minutes",
    "metric",
    "success_condition",
    "rollback_on_failure",
)

METRIC_REQUIRED_FIELDS = ("name", "direction", "parser", "source", "key")


def validate_experiment_packet(packet: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for field in PACKET_REQUIRED_FIELDS:
        if field not in packet:
            errors.append(f"Missing required packet field: {field}")

    launcher = packet.get("launcher")
    if launcher not in {"local", "slurm"}:
        errors.append("launcher must be one of: local, slurm")

    metric = packet.get("metric")
    if not isinstance(metric, dict):
        errors.append("metric must be an object")
    else:
        for field in METRIC_REQUIRED_FIELDS:
            if field not in metric:
                errors.append(f"Missing required metric field: {field}")
        if metric.get("direction") not in {"higher", "lower"}:
            errors.append("metric.direction must be higher or lower")
        if metric.get("parser") not in {"json", "csv", "log"}:
            errors.append("metric.parser must be json, csv, or log")

    timeout = packet.get("timeout_minutes")
    if timeout is not None and float(timeout) <= 0:
        errors.append("timeout_minutes must be positive")

    for field in ("allowed_files", "forbidden_files", "output_files"):
        if field in packet and not isinstance(packet[field], list):
            errors.append(f"{field} must be a list when provided")
    return errors


def validate_experiment_plan(data: dict[str, Any]) -> dict[str, Any]:
    if "packets" not in data:
        errors = validate_experiment_packet(data)
        return {"ok": not errors, "errors": errors}

    packet_errors = []
    for index, packet in enumerate(data.get("packets") or []):
        errors = validate_experiment_packet(packet)
        if errors:
            packet_errors.append(
                {
                    "index": index,
                    "packet_id": packet.get("packet_id"),
                    "errors": errors,
                }
            )
    return {
        "ok": not packet_errors,
        "errors": [],
        "packet_errors": packet_errors,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate an AutoRebuttal experiment packet.")
    parser.add_argument("packet")
    args = parser.parse_args(argv)

    data = json.loads(pathlib.Path(args.packet).read_text(encoding="utf-8"))
    result = validate_experiment_plan(data)
    print(json.dumps(result, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
