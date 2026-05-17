from __future__ import annotations

import csv
import pathlib


def parse_csv_metric(source: str | pathlib.Path, key: str) -> float:
    path = pathlib.Path(source)
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError(f"No CSV rows found in {path}")

    if key in rows[-1]:
        for row in reversed(rows):
            raw_value = row.get(key)
            if raw_value not in {None, ""}:
                return float(raw_value)

    for row in reversed(rows):
        metric_name = row.get("metric") or row.get("name")
        raw_value = row.get("value")
        if metric_name == key and raw_value not in {None, ""}:
            return float(raw_value)

    raise KeyError(f"Metric {key!r} not found in {path}")

