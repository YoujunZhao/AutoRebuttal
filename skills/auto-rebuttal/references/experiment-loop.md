# Experiment Loop

AutoRebuttal's experiment loop is a measured evidence lane, not a prose shortcut.

The loop has four artifacts:

1. `Experiment Request`: reviewer-facing need extracted from a comment.
2. `Experiment Packet`: one small runnable unit with command, timeout, metric, baseline, and file contract.
3. `Result Row`: append-only run summary in `results.tsv` or `results.jsonl`.
4. `Evidence Ledger`: rebuttal-facing provenance for claims.

## Decision Values

- `keep`: command completed, metric parsed, and the candidate was useful or improved against the baseline.
- `discard`: command completed and metric parsed, but the candidate did not improve against the baseline.
- `crash`: command exited non-zero.
- `timeout`: command exceeded `timeout_minutes`.
- `checks_failed`: packet validation or file-contract checks failed before execution.
- `inconclusive`: execution or script generation did not produce a verified measured claim.

## File Contract

The runner performs a lightweight static check:

- `forbidden_files` must not appear in the command string.
- declared metric/output paths must not point under `forbidden_files`.
- optional `planned_changed_files` must be inside `allowed_files` when provided.

This is not a filesystem sandbox. It is a provenance and safety check for experiment packets.

## Rebuttal Boundary

Only `keep` can generate a verified rebuttal sentence. Other decisions remain ledger evidence, blockers, or placeholders.

