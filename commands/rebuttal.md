---
description: "Start the SuperRebuttal workflow for a paper, reviews, and response constraints"
---

Use the `super-rebuttal` skill.

This command is the drafting entrypoint for a new rebuttal from paper and review inputs. If the user already has an existing rebuttal draft and wants revision-only polish, use `/rebuttal_revies` instead.

If the user provides a paper PDF and one or more review PDF files, treat the review PDF files as first-class review sources.

Do not ask the user to paste review text if review PDF files are already available and text extraction succeeds.

If a review PDF has no extractable text but can be rendered, continue from rendered page images instead of stopping or re-asking for pasted review text.
For image-fallback reviews, inspect the rendered pages first and build a reviewer outline before generating reviewer cards. Do not synthesize reviewer cards from empty text.

Before drafting, build reviewer cards and a strategy memo.

Build a reviewer outline for each reviewer before drafting. The reviewer outline must separate major weaknesses, direct reviewer questions, and minor points whenever the review contains them.

Reviewer cards must capture reviewer stance, movability, attitude, and primary concerns.

The strategy memo must summarize the global strategy across reviewers before reviewer-by-reviewer drafting starts.

Use venue-aware formatting defaults:

- ICLR: brief global summary first
- ICML / NeurIPS / AAAI: reviewer blocks only
- CVPR / ICCV / ECCV: brief global summary plus reviewer blocks

Inside each reviewer block, default to `W1 / W2 / W3` point-to-point responses.
Each `W#`, `Q#`, and `M#` label should start on its own line instead of being buried mid-paragraph.

Also respond to reviewer questions as `Q1 / Q2 / Q3`.

If the review contains minor weaknesses or minor comments, respond to them too. Minor points may be handled as:

- short `M1 / M2 / M3` responses, or
- one merged `Minor points` paragraph when several minor comments are highly similar.

When parsing OpenReview-style reviews, recognize real header variants such as `Main Weaknesses`, `Key Questions For Authors`, and `Minor Weaknesses` instead of assuming only plain `Questions:` headers.

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
