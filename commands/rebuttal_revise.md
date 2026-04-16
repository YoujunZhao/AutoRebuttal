---
description: "Polish an existing rebuttal draft against the reviews and response constraints"
---

Use the `auto-rebuttal` skill in polish mode.

This command is for revising an existing rebuttal, not starting from an empty draft. Treat the existing rebuttal artifact as first-class input alongside the optional paper and any available review context.

Use this command when the user wants to revise or polish an existing rebuttal under the active venue and budget constraints.

Accepted inputs for this command:

- rebuttal PDF
- rebuttal text
- optional paper PDF
- optional paper text
- optional LaTeX paper as either a single `.tex` file or a directory containing `.tex` files

Auto-detect the rebuttal input:

- rebuttal PDF -> parse it as a rebuttal document
- rebuttal text -> treat it as existing rebuttal prose directly

Auto-detect the optional paper input too:

- paper PDF -> parse it as a paper artifact
- paper text -> treat it as manuscript text directly
- `.tex` file or LaTeX project directory -> preserve it as a LaTeX paper artifact with an entrypoint and `latex_sources`

Start by identifying what should be preserved, tightened, reordered, or removed. Polish for clarity, specificity, and reviewer coverage without changing the factual basis of the response.

Do not invent experiments, numerical gains, citations, or promises that are not already supported by the manuscript or explicit author notes.

If review PDF files are already available and text extraction succeeds, do not ask the user to paste review text again.

If a rebuttal PDF has no extractable text, run best-effort OCR on the rendered pages first.

- if OCR succeeds, revise from the OCR text
- if OCR fails, fail clearly instead of pretending the rebuttal was parsed

If a review PDF is also available and has no extractable text but can be rendered, continue from rendered page images and rebuild the reviewer outline before revising the prose.

If the optional paper artifact is LaTeX, keep the LaTeX project context. The dual target for that path is `rebuttal_text` plus `revised_latex_paper`. Do not claim TeX compilation or broad LaTeX refactoring beyond that repo-level output contract.

Before revising the draft:

- rebuild or validate the reviewer outline
- check reviewer cards and the strategy memo against the existing rebuttal
- identify missing `W#`, `Q#`, and `M#` responses

When polishing the final structure:

- keep `W1 / W2 / W3` responses as point-to-point blocks
- answer direct reviewer questions as `Q1 / Q2 / Q3`
- use short `M1 / M2 / M3` items or one merged `Minor points` paragraph for clustered small comments
- start every `W#`, `Q#`, and `M#` label on its own line

If the existing rebuttal conflicts with the evidence, prefer a bounded correction or placeholder such as `XX` or `[RESULT-TO-FILL]` rather than a stronger unsupported claim.

Accepted output parameter:

- `output=text` -> plain-text style output (default)
- `output=md` -> Markdown-friendly output

Examples:

```text
/rebuttal_revise venue=ICML per_reviewer=5000 output=text
/rebuttal_revise venue=ICML per_reviewer=5000 output=md
```
