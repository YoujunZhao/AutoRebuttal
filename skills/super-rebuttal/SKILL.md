---
name: super-rebuttal
description: Use when drafting a conference or journal rebuttal from a paper, reviews, and venue constraints, especially when the response must stay polite, venue-aware, evidence-based, and free of fabricated experiments, gains, or citations.
---

# Super Rebuttal

## Overview

Turn a manuscript, a review set, and venue constraints into a rebuttal strategy and final response text.

Load the detailed references only when needed:

- `references/input-contract.md` for accepted inputs and fallback modes
- `references/venue-policies.md` for dated venue rules
- `references/rebuttal-playbook.md` for issue extraction and drafting tactics
- `references/source-notes.md` for research basis and source links

## Core Rules

- Read the paper, abstract, or author summary before drafting.
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
4. Map each reviewer to one or more likely personas such as empirical skeptic, novelty skeptic, clarity reviewer, or reproducibility reviewer.
5. Merge overlapping concerns across reviewers.
6. Choose a response strategy for each concern:
   - clarify existing evidence
   - acknowledge a limitation
   - promise a revision in wording or structure
   - propose future work
   - insert a result placeholder instead of fabricating a number
   - respectfully decline an unreasonable or out-of-scope request
7. Draft reviewer-by-reviewer responses or a shared response letter.
8. Run the final compliance check before presenting the draft.

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
