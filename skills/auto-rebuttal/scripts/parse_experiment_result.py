from __future__ import annotations

import argparse
import json
import pathlib
import sys
from typing import Any


if __package__ in {None, ""}:
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from adapters.csv_metric_parser import parse_csv_metric
from adapters.json_metric_parser import parse_json_metric
from adapters.log_metric_parser import parse_log_metric


def _resolve_source(working_dir: pathlib.Path, source: str | pathlib.Path) -> pathlib.Path:
    path = pathlib.Path(source)
    if not path.is_absolute():
        path = working_dir / path
    return path


def parse_metric_from_packet(
    packet: dict[str, Any],
    metric_override: dict[str, Any] | None = None,
) -> float:
    metric = dict(metric_override or packet.get("metric") or {})
    parser = str(metric.get("parser") or "").lower()
    source = metric.get("source")
    key = metric.get("key") or metric.get("name")
    if not parser or not source or not key:
        raise ValueError("Metric requires parser, source, and key/name.")

    working_dir = pathlib.Path(str(packet.get("working_dir") or ".")).expanduser().resolve()
    path = _resolve_source(working_dir, str(source))
    if parser == "json":
        return parse_json_metric(path, str(key))
    if parser == "csv":
        return parse_csv_metric(path, str(key))
    if parser == "log":
        return parse_log_metric(path, str(key), metric.get("pattern"))
    raise ValueError(f"Unsupported metric parser: {parser}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Parse a metric for an experiment packet.")
    parser.add_argument("packet")
    args = parser.parse_args(argv)

    packet = json.loads(pathlib.Path(args.packet).read_text(encoding="utf-8"))
    print(json.dumps({"metric_value": parse_metric_from_packet(packet)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
