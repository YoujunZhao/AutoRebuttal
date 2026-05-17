# Evidence Ledger

The evidence ledger links rebuttal claims to the command, metric, logs, and packet that produced them.

Default path:

```text
evidence_ledger.json
```

Default shape:

```json
{
  "schema_version": "0.1",
  "updated_at": "2026-05-16T00:00:00Z",
  "claims": []
}
```

Each claim should include:

- `claim_id`
- `request_id`
- `packet_id`
- `claim`
- `status`
- `command`
- `git_commit_before`
- `git_commit_after`
- `metric_before`
- `metric_after`
- `metric_name`
- `metric_direction`
- `log_files`
- `result_files`
- `rebuttal_sentence`
- `do_not_overclaim`

## Status Semantics

- `verified`: the packet produced parseable measured evidence that passed the keep decision.
- `failed`: the packet crashed, timed out, failed checks, or measured a worse/non-useful result.
- `inconclusive`: the packet did not produce enough evidence for a verified claim.
- `placeholder_only`: no run was completed; the rebuttal may only use placeholders.

## Non-Fabrication Rule

Do not copy a claim into rebuttal prose unless the ledger status is `verified`. For every other status, use a placeholder, blocker note, or omit the claim.
