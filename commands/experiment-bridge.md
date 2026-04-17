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
4. auto-run supplementary experiments only when both `autoexperiment=true` and `code=<path>` lead to a runnable experiment workspace

Honest execution rule:

- if a valid code path exists and the experiment workspace is runnable, the bridge may continue into experiment execution planning
- if `code` is missing, disabled, or not runnable, return blockers clearly and do not pretend the experiments were run

This command should be the lane used by `autoexperiment=true` in `/rebuttal` or `/rebuttal_revise`.

Required phrase to preserve in the user-facing contract:

- `Auto-run supplementary experiments via /experiment-bridge when reviewers ask for new evidence`
- `Only run experiments when both autoexperiment=true and code=<path> are provided`
