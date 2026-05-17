from __future__ import annotations

import pathlib
import re


_NUMBER_PATTERN = r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?"


def default_metric_pattern(key: str) -> str:
    return rf"{re.escape(key)}\s*[:=]\s*(?P<value>{_NUMBER_PATTERN})"


def parse_log_metric(
    source: str | pathlib.Path,
    key: str,
    pattern: str | None = None,
) -> float:
    text = pathlib.Path(source).read_text(encoding="utf-8", errors="replace")
    regex = re.compile(pattern or default_metric_pattern(key), re.IGNORECASE)
    matches = list(regex.finditer(text))
    if not matches:
        raise ValueError(f"Metric {key!r} not found in {source}")

    match = matches[-1]
    if "value" in match.groupdict():
        return float(match.group("value"))

    for group in match.groups():
        try:
            return float(group)
        except (TypeError, ValueError):
            continue
    raise ValueError(f"Regex for {key!r} did not capture a numeric value.")

