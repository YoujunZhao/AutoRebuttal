---
description: "Start the SuperRebuttal workflow for a paper, reviews, and response constraints"
---

Use the `super-rebuttal` skill.

If the user provides a paper PDF and one or more review PDF files, treat the review PDF files as first-class review sources.

Do not ask the user to paste review text if review PDF files are already available and text extraction succeeds.

Before drafting, build reviewer cards and a strategy memo.

Reviewer cards must capture reviewer stance, movability, attitude, and primary concerns.

The strategy memo must summarize the global strategy across reviewers before reviewer-by-reviewer drafting starts.

Use venue-aware formatting defaults:

- ICLR: brief global summary first
- ICML / NeurIPS / AAAI: reviewer blocks only
- CVPR / ICCV / ECCV: brief global summary plus reviewer blocks

Inside each reviewer block, default to `W1 / W2 / W3` point-to-point responses.

When empirical evidence is requested, allow a local experiment placeholder table with `XX` values instead of fabricated numbers.

First identify whether the author needs:

1. a per-reviewer response budget
2. one shared global rebuttal budget

User-provided requirements always override venue defaults.

Examples:

- `venue=ICML per_reviewer=5000`
- `venue=AAAI per_reviewer=3000`
- `venue=ICLR global_summary=false per_reviewer=4500`

If the venue format is not explicitly verified by the repository, ask for an explicit character or word limit and continue in generic mode.
