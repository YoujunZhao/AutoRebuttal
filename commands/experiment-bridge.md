---
description: "Auto-run supplementary experiments when reviewers ask for new evidence"
---

Use the `auto-rebuttal` skill in experiment-bridge mode.

This command is the supplementary evidence lane for rebuttal work. Use it when reviewers ask for:

- stronger baseline comparisons
- ablations
- runtime, latency, or memory evidence
- robustness or sensitivity checks
- any other new experimental evidence

Accepted inputs:

- paper PDF, paper text, or LaTeX paper
- review PDF or review text
- optional existing rebuttal text
- optional `code=<path>` project code path

The job of `/experiment-bridge` is to:

1. extract experiment requests from reviewer feedback
2. classify them into comparison / ablation / efficiency / robustness / supplementary evidence
3. build a bounded experiment bundle
4. map runnable requests into experiment packets with metric and benchmark contracts
5. auto-run supplementary experiments only when both `autoexperiment=true` and `code=<path>` lead to a runnable experiment workspace
6. record measured outcomes in `results.tsv` or `results.jsonl` and `evidence_ledger.json`

Honest execution rule:

- if a valid code path exists and the experiment workspace is runnable, the bridge may continue into experiment execution planning
- if `code` is missing, disabled, or not runnable, return blockers clearly and do not pretend the experiments were run
- if a packet fails, crashes, times out, or produces no parseable metric, keep that as ledger evidence but do not write it as a verified rebuttal claim
- Slurm support is dry-run/script-generation unless the user provides real cluster execution evidence

This command should be the lane used by `autoexperiment=true` in `/rebuttal` or `/rebuttal_revise`.

Required phrase to preserve in the user-facing contract:

- `Auto-run supplementary experiments via /experiment-bridge when reviewers ask for new evidence`
- `Only run experiments when both autoexperiment=true and code=<path> are provided`
