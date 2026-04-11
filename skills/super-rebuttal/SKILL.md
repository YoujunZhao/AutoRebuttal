---
name: super-rebuttal
description: Use when drafting a conference or journal rebuttal from a paper, reviews, and venue constraints, especially when the response must stay polite, venue-aware, evidence-based, and free of fabricated experiments, gains, or citations.
---

# Super Rebuttal

## Overview

Turn a manuscript, a review set, and venue constraints into a rebuttal strategy and final response text.

First-class input artifacts include one paper PDF plus zero or more review PDFs. When PDFs are used, extract text on a best-effort basis for text-based files and keep each review as a separate source item.

Load the detailed references only when needed:

- `references/input-contract.md` for accepted inputs and fallback modes
- `references/venue-policies.md` for dated venue rules
- `references/rebuttal-playbook.md` for issue extraction and drafting tactics
- `references/source-notes.md` for research basis and source links
- `scripts/build_input_bundle.py` when the user provides paper PDF and review PDF files together
- `scripts/build_reviewer_cards.py` to create reviewer cards before drafting
- `scripts/build_venue_format_plan.py` to resolve venue-specific structure
- `scripts/build_strategy_memo.py` to summarize shared issues and the global strategy
- `scripts/build_style_plan.py` to decide how the initial rebuttal should sound
- `scripts/allocate_rebuttal_budget.py` to plan characters before drafting
- `scripts/build_experiment_placeholder_table.py` when a reviewer asks for new empirical evidence
- `references/reviewer-model.md` for reviewer stance and attitude analysis
- `references/human-rebuttal-style.md` for a more human-like rebuttal rhythm

## Supported Inputs

- one paper PDF, or extracted manuscript text
- zero or more review PDFs, or copied review text
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

## Core Rules

- Read the paper, abstract, or author summary before drafting.
- If one paper PDF and one or more review PDF files are available, build the input bundle first and treat extracted review text as the working review source.
- Do not ask the user to paste review text when review PDF extraction succeeds.
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
2. Read all reviews and convert them into atomic concerns.
3. Summarize the venue or journal constraints.
4. Build reviewer cards, including reviewer stance, movability, attitude, and primary concerns.
5. Build a strategy memo that identifies shared issues and a global strategy across reviewers.
6. Merge overlapping concerns across reviewers.
7. Choose a response strategy for each concern:
   - clarify existing evidence
   - acknowledge a limitation
   - promise a revision in wording or structure
   - propose future work
   - insert a result placeholder instead of fabricating a number
   - respectfully decline an unreasonable or out-of-scope request
8. Draft reviewer-by-reviewer responses or a shared response letter.
9. Run the final compliance check before presenting the draft.

## Venue-Aware Formatting Defaults

- ICLR: brief global summary, then reviewer blocks
- ICML / NeurIPS / AAAI: reviewer blocks only
- CVPR / ICCV / ECCV: brief global summary, then reviewer blocks

Inside each reviewer block, default to `W1 / W2 / W3` point-to-point sections.

Also respond to reviewer questions as `Q1 / Q2 / Q3`.

If the review contains minor weaknesses or minor comments, respond to them as short `M#` items or merge them into one compact minor-points response when they are highly similar.

If a reviewer asks for empirical evidence, include a local experiment placeholder table with `XX` values rather than fabricating results.

## Required Output Structure

Default to this shape unless the user asks for a different format:

1. Constraint summary
2. Concern map
3. Shared issues across reviewers
4. Final rebuttal draft
5. Open placeholders that still need author input

If the user asks for prose only, still do the analysis internally before drafting.

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
