from __future__ import annotations

import argparse
import datetime as _dt
import json
import pathlib
import subprocess
import sys
from typing import Any


if __package__ in {None, ""}:
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from adapters.local_shell import run_local_command, timestamp
from adapters.slurm import generate_sbatch_script
from parse_experiment_result import parse_metric_from_packet
from update_evidence_ledger import update_evidence_ledger
from validate_experiment_plan import validate_experiment_packet


DECISIONS = {
    "keep",
    "discard",
    "crash",
    "timeout",
    "checks_failed",
    "inconclusive",
}


def _git_head(working_dir: pathlib.Path) -> str | None:
    try:
        completed = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=working_dir,
            text=True,
            capture_output=True,
            check=False,
            timeout=5,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if completed.returncode != 0:
        return None
    return completed.stdout.strip() or None


def _inside(path: pathlib.Path, parent: pathlib.Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def _declared_path_is_forbidden(root: pathlib.Path, path_text: str, forbidden: list[str]) -> bool:
    candidate = pathlib.Path(path_text)
    if not candidate.is_absolute():
        candidate = root / candidate
    for forbidden_text in forbidden:
        forbidden_path = pathlib.Path(forbidden_text)
        if not forbidden_path.is_absolute():
            forbidden_path = root / forbidden_path
        if _inside(candidate, forbidden_path):
            return True
    return False


def check_file_contract(packet: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    root = pathlib.Path(str(packet.get("working_dir") or ".")).expanduser().resolve()
    allowed = [str(value) for value in packet.get("allowed_files") or []]
    forbidden = [str(value) for value in packet.get("forbidden_files") or []]
    command = str(packet.get("command") or "")

    for forbidden_path in forbidden:
        if forbidden_path and forbidden_path in command:
            errors.append(f"Command references forbidden path: {forbidden_path}")

    for allowed_path in allowed:
        if allowed_path in forbidden:
            errors.append(f"Path is both allowed and forbidden: {allowed_path}")

    declared_paths = list(packet.get("output_files") or [])
    metric_source = (packet.get("metric") or {}).get("source")
    if metric_source:
        declared_paths.append(metric_source)
    for path_text in declared_paths:
        if _declared_path_is_forbidden(root, str(path_text), forbidden):
            errors.append(f"Declared result path is forbidden: {path_text}")

    for path_text in packet.get("planned_changed_files") or []:
        candidate = pathlib.Path(path_text)
        if _declared_path_is_forbidden(root, str(path_text), forbidden):
            errors.append(f"Planned changed file is forbidden: {path_text}")
        if allowed:
            absolute = candidate if candidate.is_absolute() else root / candidate
            allowed_match = False
            for allowed_text in allowed:
                allowed_path = pathlib.Path(allowed_text)
                if not allowed_path.is_absolute():
                    allowed_path = root / allowed_path
                if _inside(absolute, allowed_path):
                    allowed_match = True
                    break
            if not allowed_match:
                errors.append(f"Planned changed file is outside allowed_files: {path_text}")
    return errors


def _compare_metric(after: float | None, before: float | None, direction: str) -> str:
    if after is None:
        return "inconclusive"
    if before is None:
        return "keep"
    if direction == "lower":
        return "keep" if after < before else "discard"
    if direction == "higher":
        return "keep" if after > before else "discard"
    return "inconclusive"


def _append_results(path: pathlib.Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix == ".jsonl":
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(row, sort_keys=True) + "\n")
        return

    fields = [
        "created_at",
        "packet_id",
        "request_id",
        "decision",
        "metric_name",
        "metric_direction",
        "metric_before",
        "metric_after",
        "returncode",
    ]
    needs_header = not path.exists()
    with path.open("a", encoding="utf-8") as handle:
        if needs_header:
            handle.write("\t".join(fields) + "\n")
        handle.write("\t".join("" if row.get(field) is None else str(row.get(field)) for field in fields) + "\n")


def _ledger_status(decision: str) -> str:
    if decision == "keep":
        return "verified"
    if decision in {"crash", "timeout", "checks_failed", "discard"}:
        return "failed"
    return "inconclusive"


def _build_claim(
    *,
    packet: dict[str, Any],
    decision: str,
    command_result: dict[str, Any],
    metric_before: float | None,
    metric_after: float | None,
    git_before: str | None,
    git_after: str | None,
) -> dict[str, Any]:
    metric = dict(packet.get("metric") or {})
    packet_id = str(packet.get("packet_id"))
    request_id = str(packet.get("request_id"))
    claim_text = str(packet.get("hypothesis") or "")
    rebuttal_sentence = None
    if decision == "keep":
        sentence_claim = claim_text.rstrip(" .")
        rebuttal_sentence = (
            f"[VERIFIED:{packet_id}] {sentence_claim} "
            f"({metric.get('name')}={metric_after})."
        )
    return {
        "claim_id": f"claim-{packet_id}",
        "request_id": request_id,
        "packet_id": packet_id,
        "claim": claim_text,
        "status": _ledger_status(decision),
        "command": packet.get("command"),
        "git_commit_before": git_before,
        "git_commit_after": git_after,
        "metric_before": metric_before,
        "metric_after": metric_after,
        "metric_name": metric.get("name"),
        "metric_direction": metric.get("direction"),
        "log_files": [
            command_result.get("stdout_log"),
            command_result.get("stderr_log"),
        ],
        "result_files": packet.get("output_files") or [metric.get("source")],
        "rebuttal_sentence": rebuttal_sentence,
        "do_not_overclaim": True,
    }


def run_experiment_packet(
    packet: dict[str, Any],
    *,
    results_path: str | pathlib.Path = "results.tsv",
    ledger_path: str | pathlib.Path = "evidence_ledger.json",
    logs_root: str | pathlib.Path = "logs/experiments",
) -> dict[str, Any]:
    errors = validate_experiment_packet(packet) + check_file_contract(packet)
    working_dir = pathlib.Path(str(packet.get("working_dir") or ".")).expanduser().resolve()
    packet_id = str(packet.get("packet_id") or "packet")
    request_id = str(packet.get("request_id") or "")
    metric = dict(packet.get("metric") or {})
    git_before = _git_head(working_dir)

    run_stamp = timestamp()
    run_logs_dir = pathlib.Path(logs_root) / f"{packet_id}-{run_stamp}"
    if not run_logs_dir.is_absolute():
        run_logs_dir = working_dir / run_logs_dir

    if errors:
        decision = "checks_failed"
        command_result = {
            "status": "not_run",
            "returncode": None,
            "stdout_log": None,
            "stderr_log": None,
            "errors": errors,
        }
        metric_before = None
        metric_after = None
    elif packet.get("launcher") == "slurm":
        script_path = run_logs_dir / "run.sbatch"
        generate_sbatch_script(packet, output_path=script_path)
        decision = "inconclusive"
        command_result = {
            "status": "slurm_script_generated",
            "returncode": None,
            "stdout_log": str(script_path),
            "stderr_log": None,
        }
        metric_before = None
        metric_after = None
    else:
        baseline = dict(packet.get("baseline") or {})
        metric_before = baseline.get("metric_value")
        if metric_before is not None:
            metric_before = float(metric_before)
        if baseline.get("command") and metric_before is None:
            baseline_result = run_local_command(
                command=str(baseline["command"]),
                working_dir=working_dir,
                timeout_minutes=packet.get("timeout_minutes"),
                logs_dir=run_logs_dir,
                label="baseline",
            )
            if baseline_result["status"] == "completed" and baseline_result["returncode"] == 0:
                metric_before = parse_metric_from_packet(packet, baseline.get("metric"))

        command_result = run_local_command(
            command=str(packet["command"]),
            working_dir=working_dir,
            timeout_minutes=packet.get("timeout_minutes"),
            logs_dir=run_logs_dir,
            label="candidate",
        )
        if command_result["status"] == "timeout":
            decision = "timeout"
            metric_after = None
        elif command_result["returncode"] != 0:
            decision = "crash"
            metric_after = None
        else:
            try:
                metric_after = parse_metric_from_packet(packet)
                decision = _compare_metric(metric_after, metric_before, str(metric.get("direction")))
            except Exception as exc:  # noqa: BLE001 - result parsing should be captured as evidence.
                decision = "inconclusive"
                metric_after = None
                command_result["parse_error"] = str(exc)

    git_after = _git_head(working_dir)
    row = {
        "created_at": _dt.datetime.now(_dt.UTC).isoformat().replace("+00:00", "Z"),
        "packet_id": packet_id,
        "request_id": request_id,
        "decision": decision,
        "metric_name": metric.get("name"),
        "metric_direction": metric.get("direction"),
        "metric_before": metric_before,
        "metric_after": metric_after,
        "returncode": command_result.get("returncode"),
        "logs_dir": str(run_logs_dir),
        "rollback_recommended": bool(packet.get("rollback_on_failure")) and decision in {"discard", "crash", "timeout", "checks_failed"},
    }
    results_file = pathlib.Path(results_path)
    if not results_file.is_absolute():
        results_file = working_dir / results_file
    _append_results(results_file, row)

    ledger_file = pathlib.Path(ledger_path)
    if not ledger_file.is_absolute():
        ledger_file = working_dir / ledger_file
    claim = _build_claim(
        packet=packet,
        decision=decision,
        command_result=command_result,
        metric_before=metric_before,
        metric_after=metric_after,
        git_before=git_before,
        git_after=git_after,
    )
    update_evidence_ledger(ledger_path=ledger_file, claim=claim)

    return {
        "decision": decision,
        "result": row,
        "command_result": command_result,
        "evidence_claim": claim,
        "results_path": str(results_file),
        "ledger_path": str(ledger_file),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run or materialize an AutoRebuttal experiment packet.")
    parser.add_argument("packet")
    parser.add_argument("--results", default="results.tsv")
    parser.add_argument("--ledger", default="evidence_ledger.json")
    parser.add_argument("--logs-root", default="logs/experiments")
    args = parser.parse_args(argv)

    packet = json.loads(pathlib.Path(args.packet).read_text(encoding="utf-8"))
    summary = run_experiment_packet(
        packet,
        results_path=args.results,
        ledger_path=args.ledger,
        logs_root=args.logs_root,
    )
    print(json.dumps(summary, indent=2))
    return 0 if summary["decision"] in DECISIONS else 1


if __name__ == "__main__":
    raise SystemExit(main())
