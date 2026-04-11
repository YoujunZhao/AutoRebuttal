# SuperRebuttal Style and Budget Design

**Date:** 2026-04-11
**Project:** SuperRebuttal
**Status:** Approved by delegated default

## Goal

Improve SuperRebuttal so that:

1. the initial rebuttal draft follows a stronger human-like style inspired by strong ICLR / NeurIPS rebuttals
2. character control is treated as a first-class planning step rather than a final truncation step

## Problem

Current output is better structured than before, but still differs from strong human rebuttals in two ways:

- it is often too generic in tone and paragraph rhythm
- character control is not yet central enough to the actual writing strategy

## Sample Constraints

The user provided several rebuttal-style PDF examples. Locally, these PDFs are renderable but not directly text-extractable with the current extractor. That means:

- they are still useful as human style references
- but the project should encode the style as rules and templates, not depend on direct text extraction from these examples

## Recommended Approach

### Part 1: Initial rebuttal style guide

Encode the expected human style for **initial rebuttal rounds**:

- short opener
- direct answer first
- reviewer-specific focus
- shared issues resolved consistently
- no repetitive generic gratitude loops
- evidence before rhetoric
- narrow concessions instead of defensive denial

### Part 2: Budget-first planning

Make character budgeting explicit in the workflow:

- if `per-reviewer`, allocate opener / main answer / closing within each reviewer response
- if `shared-global`, allocate opener / shared themes / reviewer sections / closing globally

This must shape the draft, not only validate it afterward.

## Initial Rebuttal Writing Rules

For the first rebuttal round:

1. open with a compact global acknowledgment
2. address the highest-leverage concern immediately
3. answer with concrete evidence or bounded concession
4. avoid repeating the same gratitude sentence for every reviewer
5. keep paragraphs short and information-dense
6. close with a brief statement of what was clarified or strengthened

## Character Control Rules

Character control should produce a **budget plan** before drafting:

- opener budget
- reviewer body budget
- optional closing budget

The draft should then be written to those budgets, not cut down blindly afterward.

## Proposed Files

```text
skills/super-rebuttal/
  references/
    initial-rebuttal-style.md
  scripts/
    build_style_plan.py
    allocate_rebuttal_budget.py
tests/
  test_character_budget.py
  test_style_plan.py
```

## Success Criteria

- initial rebuttal style is explicitly documented as a workflow rule
- budget planning is explicit and testable
- the docs explain both:
  - how initial rebuttal should be written
  - how character constraints are handled
