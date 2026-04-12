---
description: "Polish an existing rebuttal draft against the reviews and response constraints"
---

Use the `super-rebuttal` skill in polish mode.

This command is for revising an existing rebuttal, not starting from an empty draft. Treat the existing rebuttal text as a first-class input artifact alongside the paper, reviews, and venue or budget constraints.

Start by identifying what should be preserved, tightened, reordered, or removed. Polish for clarity, specificity, and reviewer coverage without changing the factual basis of the response.

Do not invent experiments, numerical gains, citations, or promises that are not already supported by the manuscript or explicit author notes.

If review PDF files are already available and text extraction succeeds, do not ask the user to paste review text again.

If a review PDF has no extractable text but can be rendered, continue from rendered page images and rebuild the reviewer outline before revising the prose.

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
