from __future__ import annotations

import datetime as _dt
import pathlib
import subprocess
from typing import Any


def timestamp() -> str:
    return _dt.datetime.now(_dt.UTC).strftime("%Y%m%dT%H%M%SZ")


def run_local_command(
    *,
    command: str,
    working_dir: str | pathlib.Path,
    timeout_minutes: int | float | None,
    logs_dir: str | pathlib.Path,
    label: str,
) -> dict[str, Any]:
    root = pathlib.Path(working_dir).expanduser().resolve()
    log_root = pathlib.Path(logs_dir)
    if not log_root.is_absolute():
        log_root = root / log_root
    log_root.mkdir(parents=True, exist_ok=True)

    stdout_path = log_root / f"{label}.stdout.log"
    stderr_path = log_root / f"{label}.stderr.log"
    timeout_seconds = None if timeout_minutes is None else float(timeout_minutes) * 60

    try:
        completed = subprocess.run(
            command,
            cwd=root,
            shell=True,
            text=True,
            capture_output=True,
            timeout=timeout_seconds,
            check=False,
        )
        stdout_path.write_text(completed.stdout, encoding="utf-8")
        stderr_path.write_text(completed.stderr, encoding="utf-8")
        return {
            "status": "completed",
            "returncode": completed.returncode,
            "stdout_log": str(stdout_path),
            "stderr_log": str(stderr_path),
        }
    except subprocess.TimeoutExpired as exc:
        stdout_path.write_text(exc.stdout or "", encoding="utf-8")
        stderr_path.write_text(exc.stderr or "", encoding="utf-8")
        return {
            "status": "timeout",
            "returncode": None,
            "stdout_log": str(stdout_path),
            "stderr_log": str(stderr_path),
        }

