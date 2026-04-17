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
- optional experiment workspace

The job of `/experiment-bridge` is to:

1. extract experiment requests from reviewer feedback
2. classify them into comparison / ablation / efficiency / robustness / supplementary evidence
3. build a bounded experiment bundle
4. auto-run supplementary experiments only when a runnable experiment workspace is actually available

Honest execution rule:

- if a runnable experiment workspace exists, the bridge may continue into experiment execution planning
- if no runnable experiment workspace exists, return blockers clearly and do not pretend the experiments were run

This command should be the lane used by `autoexperiment=true` in `/rebuttal` or `/rebuttal_revise`.

Required phrase to preserve in the user-facing contract:

- `Auto-run supplementary experiments via /experiment-bridge when reviewers ask for new evidence`
