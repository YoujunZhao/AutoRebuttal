from __future__ import annotations

import pathlib
import shlex
from typing import Any


def generate_sbatch_script(
    packet: dict[str, Any],
    *,
    output_path: str | pathlib.Path | None = None,
) -> str:
    slurm = dict(packet.get("slurm") or {})
    command = str(slurm.get("command") or packet.get("command") or "").strip()
    if not command:
        raise ValueError("Slurm script generation requires a command.")

    lines = ["#!/usr/bin/env bash", "set -euo pipefail"]
    mapping = {
        "partition": "partition",
        "account": "account",
        "gres": "gres",
        "cpus_per_task": "cpus-per-task",
        "mem": "mem",
        "time": "time",
    }
    for field, sbatch_name in mapping.items():
        value = slurm.get(field)
        if value not in {None, ""}:
            lines.append(f"#SBATCH --{sbatch_name}={value}")

    output_log = slurm.get("output_log_path") or slurm.get("output") or "logs/slurm-%j.out"
    lines.append(f"#SBATCH --output={output_log}")
    lines.append("")

    conda_env = slurm.get("conda_env")
    if conda_env:
        lines.extend(
            [
                "if command -v conda >/dev/null 2>&1; then",
                "  source \"$(conda info --base)/etc/profile.d/conda.sh\"",
                f"  conda activate {shlex.quote(str(conda_env))}",
                "fi",
                "",
            ]
        )

    working_dir = packet.get("working_dir")
    if working_dir not in {None, ""}:
        lines.append(f"cd {shlex.quote(str(working_dir))}")
    lines.append(command)
    script = "\n".join(lines) + "\n"

    if output_path is not None:
        path = pathlib.Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(script, encoding="utf-8")
    return script

