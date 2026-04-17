---
description: "Start the AutoRebuttal workflow for a paper, reviews, and response constraints"
---

Use the `auto-rebuttal` skill.

This command is the drafting entrypoint for a new rebuttal from paper and review inputs. If the user already has an existing rebuttal draft and wants revision-only polish, use `/rebuttal_revise` instead.

Accepted inputs for this command:

- one paper PDF
- paper text
- one LaTeX paper as either a single `.tex` file or a directory containing `.tex` files
- one or more review PDFs
- one or more text reviews

Auto-detect each review input:

- PDF review -> parse as a review document
- text review -> treat as reviewer text directly

Auto-detect the paper input too:

- paper PDF -> parse it as a paper artifact
- paper text -> treat it as manuscript text directly
- `.tex` file or LaTeX project directory -> preserve it as a LaTeX paper artifact with an entrypoint and `latex_sources`

If the user provides a paper PDF and one or more review PDF files, treat the review PDF files as first-class review sources.
If the user provides copied review text instead, treat it as a text review source without asking them to convert it to PDF first.

Do not ask the user to paste review text if review PDF files are already available and text extraction succeeds.

If a review PDF has no extractable text but can be rendered, run best-effort OCR on the rendered page images first.

- if OCR succeeds, continue from the OCR text
- if OCR fails, keep the honest image fallback and inspect the rendered pages before generating reviewer cards

Before drafting, build reviewer cards and a strategy memo.

If the paper artifact is LaTeX, keep the LaTeX project context instead of flattening it away. The dual target for that path is `rebuttal_text` plus `revised_latex_paper`. Do not claim TeX compilation or arbitrary project rewriting beyond that repo-level output contract.

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

Accepted output parameter:

- `output=text` -> plain-text style output (default)
- `output=md` -> Markdown-friendly output

Accepted experiment parameter:

- `autoexperiment=false` -> keep experiment placeholders only (default)
- `autoexperiment=true` -> Auto-run supplementary experiments via `/experiment-bridge` when reviewers ask for new evidence

Accepted code parameter:

- `code=false` -> no project code path is available (default)
- `code=/path/to/project` -> project code path used by `/experiment-bridge`
- supplementary experiments only run when both `autoexperiment=true` and `code=<path>` are provided

Examples:

- `venue=ICML per_reviewer=5000 output=text`
- `venue=AAAI per_reviewer=3000`
- `venue=ICML per_reviewer=5000 output=md`
- `venue=ICML per_reviewer=5000 autoexperiment=true code=./project`
- `venue=ICLR global_summary=false per_reviewer=4500`
- `/rebuttal venue=ICML per_reviewer=5000 output=text`

If the venue format is not explicitly verified by the repository, ask for an explicit character or word limit and continue in generic mode.
