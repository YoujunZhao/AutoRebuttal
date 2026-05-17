from __future__ import annotations

import json
import pathlib
from typing import Any


def _resolve_key(data: Any, key: str) -> Any:
    current = data
    for part in key.split("."):
        if isinstance(current, list):
            current = current[int(part)]
        elif isinstance(current, dict):
            current = current[part]
        else:
            raise KeyError(f"Cannot resolve {part!r} inside non-container value.")
    return current


def parse_json_metric(source: str | pathlib.Path, key: str) -> float:
    data = json.loads(pathlib.Path(source).read_text(encoding="utf-8"))
    value = _resolve_key(data, key)
    return float(value)

