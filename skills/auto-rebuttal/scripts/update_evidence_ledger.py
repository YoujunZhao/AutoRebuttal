from __future__ import annotations

import argparse
import datetime as _dt
import json
import pathlib
from typing import Any


def empty_ledger() -> dict[str, Any]:
    return {
        "schema_version": "0.1",
        "updated_at": None,
        "claims": [],
    }


def load_ledger(path: str | pathlib.Path) -> dict[str, Any]:
    ledger_path = pathlib.Path(path)
    if not ledger_path.exists():
        return empty_ledger()
    data = json.loads(ledger_path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return {"schema_version": "0.1", "updated_at": None, "claims": data}
    if "claims" not in data:
        data["claims"] = []
    return data


def upsert_claim(
    ledger: dict[str, Any],
    claim: dict[str, Any],
) -> dict[str, Any]:
    claims = list(ledger.get("claims") or [])
    claim_id = claim.get("claim_id")
    replaced = False
    for index, existing in enumerate(claims):
        if existing.get("claim_id") == claim_id:
            claims[index] = claim
            replaced = True
            break
    if not replaced:
        claims.append(claim)
    ledger["claims"] = claims
    ledger["updated_at"] = _dt.datetime.now(_dt.UTC).isoformat().replace("+00:00", "Z")
    return ledger


def write_ledger(path: str | pathlib.Path, ledger: dict[str, Any]) -> None:
    ledger_path = pathlib.Path(path)
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    ledger_path.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")


def update_evidence_ledger(
    *,
    ledger_path: str | pathlib.Path,
    claim: dict[str, Any],
) -> dict[str, Any]:
    ledger = upsert_claim(load_ledger(ledger_path), claim)
    write_ledger(ledger_path, ledger)
    return ledger


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Upsert an AutoRebuttal evidence claim.")
    parser.add_argument("--ledger", required=True)
    parser.add_argument("--claim", required=True, help="Path to a claim JSON file.")
    args = parser.parse_args(argv)

    claim = json.loads(pathlib.Path(args.claim).read_text(encoding="utf-8"))
    update_evidence_ledger(ledger_path=args.ledger, claim=claim)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

