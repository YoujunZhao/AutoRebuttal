---
description: "Start the SuperRebuttal workflow for a paper, reviews, and response constraints"
---

Use the `super-rebuttal` skill.

If the user provides a paper PDF and one or more review PDF files, treat the review PDF files as first-class review sources.

Do not ask the user to paste review text if review PDF files are already available and text extraction succeeds.

First identify whether the author needs:

1. a per-reviewer response budget
2. one shared global rebuttal budget

If the venue format is not explicitly verified by the repository, ask for an explicit character or word limit and continue in generic mode.
