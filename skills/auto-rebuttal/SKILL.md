---
name: auto-rebuttal
description: Use when drafting a conference or journal rebuttal from a paper, reviews, and venue constraints, especially when the response must stay polite, venue-aware, evidence-based, and free of fabricated experiments, gains, or citations.
---

# Auto Rebuttal

## Overview

Turn a manuscript, a review set, and venue constraints into a rebuttal strategy and final response text.

First-class input artifacts include one paper PDF, paper text, or LaTeX paper plus zero or more review PDFs / review texts. When PDFs are used, extract text on a best-effort basis for text-based files and keep each review as a separate source item.

Load the detailed references only when needed:

- `references/input-contract.md` for accepted inputs and fallback modes
- `references/venue-policies.md` for dated venue rules
- `references/rebuttal-playbook.md` for issue extraction and drafting tactics
- `references/source-notes.md` for research basis and source links
- `scripts/build_draft_bundle.py` when the user provides paper PDF plus review PDF or review text inputs
- `scripts/build_revision_bundle.py` when the user provides an existing rebuttal PDF or rebuttal text, with optional paper PDF
- `scripts/detect_paper_artifact.py` when the paper input may be PDF, `.tex`, or a LaTeX project directory
- `scripts/build_latex_output_package.py` when the paper source type is LaTeX and the workflow should return both rebuttal text and revised LaTeX paper
- `scripts/build_input_bundle.py` as the PDF-only compatibility wrapper for draft-mode bundle building
- `scripts/ocr_rendered_pages.py` when a PDF must be OCRed after page rendering
- `scripts/render_review_pdf_pages.py` when a review PDF has no text layer and must continue through rendered page images
- `scripts/build_reviewer_outline.py` to preserve `W/Q/M` structure before prose drafting
- `scripts/build_reviewer_cards.py` to create reviewer cards before drafting
- `scripts/build_venue_format_plan.py` to resolve venue-specific structure
- `scripts/build_strategy_memo.py` to summarize shared issues and the global strategy
- `scripts/build_style_plan.py` to decide how the initial rebuttal should sound
- `scripts/allocate_rebuttal_budget.py` to plan characters before drafting
- `scripts/build_experiment_placeholder_table.py` when a reviewer asks for new empirical evidence
- `references/reviewer-model.md` for reviewer stance and attitude analysis
- `references/human-rebuttal-style.md` for a more human-like rebuttal rhythm

## Supported Inputs

- one paper PDF, one paper LaTeX file, one LaTeX paper directory, or extracted manuscript text
- zero or more review PDFs, or copied review text
- an existing rebuttal draft when the user wants revision-only polish
- an existing rebuttal PDF when the user wants revision-only polish
- venue and budget constraints
- author notes about promises, limits, or forbidden claims

## Human-Like Intermediate Artifacts

Before drafting, form:

1. reviewer cards
2. a strategy memo
3. a venue-aware format plan
4. a character budget plan
5. the final rebuttal draft

Reviewer cards should include reviewer stance, movability, attitude, and primary concerns.

When the paper artifact is LaTeX, the output target expands to `rebuttal_text` plus `revised_latex_paper`.

## Core Rules

- Read the paper, abstract, or author summary before drafting.
- In draft mode, build the draft bundle first and auto-detect whether each review artifact is PDF or text.
- In draft mode, auto-detect whether the paper artifact is PDF, `.tex`, or a LaTeX project directory.
- In revise mode, build the revision bundle first and auto-detect whether the rebuttal artifact is PDF or text.
- In revise mode, if a paper artifact is provided, auto-detect whether it is PDF, `.tex`, or a LaTeX project directory.
- Do not ask the user to paste review text when review PDF extraction succeeds.
- If a review PDF has no extractable text but can be rendered, run OCR on the rendered pages first.
- If OCR succeeds, continue from the OCR text.
- If OCR fails, keep the rendered-page fallback and inspect the rendered pages before reviewer-card generation. Do not pretend empty text is a usable review.
- If the user already has an existing rebuttal draft or rebuttal PDF and asks to revise or polish it, treat that rebuttal artifact as first-class input and use the `/rebuttal_revise` command surface behavior.
- If a rebuttal PDF has no extractable text, run OCR on its rendered pages first; only fail if OCR also produces no usable text.
- If the paper source type is LaTeX, support two outputs: `rebuttal_text` and `revised_latex_paper`.
- If the paper source type is LaTeX, preserve the detected `entrypoint` and `latex_sources`. Do not claim TeX compilation or arbitrary multi-file rewrite guarantees unless the repo surface actually proves them.
- Build a reviewer outline before writing prose so each reviewer can preserve `W#`, `Q#`, and `M#` structure.
- Build reviewer cards before writing prose.
- Build a strategy memo before reviewer-by-reviewer drafting.
- Build a venue-aware format plan before deciding whether a summary is needed.
- Build a character budget plan before drafting.
- Normalize reviews into atomic concerns before writing prose.
- Use venue rules when available; if the user provides explicit limits, those override bundled defaults.
- Never invent experiments, numerical gains, p-values, baselines, or citations.
- Use placeholders such as `XX`, `[RESULT-TO-FILL]`, `[TABLE-PLACEHOLDER]`, or `[IF-RUN-LATER]` when evidence is missing.
- Keep the tone calm, specific, and non-defensive.
- Prefer direct answers with line, table, or section references when the evidence already exists in the paper.

## Required Workflow

1. Read the paper artifact or the author's summary.
2. In draft mode, read all reviews and convert them into atomic concerns.
3. In revise mode, read the existing rebuttal artifact first, then use the optional paper and review context for validation and cleanup.
4. Summarize the venue or journal constraints.
5. Build a reviewer outline for each reviewer, separating major weaknesses, direct reviewer questions, and minor points whenever those sections are present.
6. Build reviewer cards, including reviewer stance, movability, attitude, and primary concerns.
7. Build a strategy memo that identifies shared issues and a global strategy across reviewers.
8. Merge overlapping concerns across reviewers.
9. Choose a response strategy for each concern:
   - clarify existing evidence
   - acknowledge a limitation
   - promise a revision in wording or structure
   - propose future work
   - insert a result placeholder instead of fabricating a number
   - respectfully decline an unreasonable or out-of-scope request
10. Draft reviewer-by-reviewer responses or a shared response letter, or revise the existing rebuttal draft.
11. If the paper artifact is LaTeX, package the final result as `rebuttal_text` plus `revised_latex_paper`.
12. Run the final compliance check before presenting the draft.

## Venue-Aware Formatting Defaults

- ICLR: brief global summary, then reviewer blocks
- ICML / NeurIPS / AAAI: reviewer blocks only
- CVPR / ICCV / ECCV: brief global summary, then reviewer blocks

Inside each reviewer block, default to `W1 / W2 / W3` point-to-point sections.
Each `W#`, `Q#`, and `M#` label should start on its own line.

Also respond to reviewer questions as `Q1 / Q2 / Q3`.

If the review contains minor weaknesses or minor comments, respond to them as short `M#` items or merge them into one compact minor-points response when they are highly similar.

When reading OpenReview-style reviews, preserve header variants such as `Main Weaknesses`, `Key Questions For Authors`, and `Minor Weaknesses` rather than flattening them into `W#` only.

If a reviewer asks for empirical evidence, include a local experiment placeholder table with `XX` values rather than fabricating results.

## Required Output Structure

Default to this shape unless the user asks for a different format:

1. Constraint summary
2. Concern map
3. Shared issues across reviewers
4. Final rebuttal draft
5. Open placeholders that still need author input

If the user asks for prose only, still do the analysis internally before drafting.

For LaTeX paper inputs, the repo-level package shape may also include:

- `rebuttal_text`
- `revised_latex_paper`
- `entrypoint`

## Non-Fabrication Guardrail

Never write claims like these unless the user already provided the evidence:

- "we improve by 3.2%"
- "the new ablation confirms"
- "the statistical test is significant"
- "we added a new baseline and it outperforms all prior work"

When the evidence is not available, write a bounded placeholder instead:

- "we will report the final number as `XX` once the run is complete"
- "a compact table can be inserted as `[TABLE-PLACEHOLDER]`"
- "if additional runs are completed, we will summarize them under `[RESULT-TO-FILL]`"

## Common Mistakes

- Replying to reviews one by one without merging shared issues.
- Sounding defensive instead of specific.
- Promising experiments the authors cannot realistically deliver.
- Using a venue-default rule after the user already gave an explicit limit.
- Treating journals and conferences as if they share one universal rebuttal format.

## Final Check

Before you finish, confirm all of the following:

- Every substantive reviewer concern has a response.
- Shared issues are handled consistently across reviewers.
- The draft respects the active venue or user constraint.
- Missing evidence is marked with placeholders, not invented.
- The tone is polite and concrete.
