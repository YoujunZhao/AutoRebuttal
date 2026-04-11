# SuperRebuttal Question and Minor Format Design

**Date:** 2026-04-11
**Project:** SuperRebuttal
**Status:** Approved by delegated default

## Goal

Make the reviewer-by-reviewer output structure explicitly handle:

- major weaknesses as `W1 / W2 / W3`
- reviewer questions as `Q1 / Q2 / Q3`
- minor weaknesses as either short `M#` items or a merged `Minor points` section

## Problem

The current formatter already defaults to `W1 / W2 / W3` point-to-point responses, but it still misses two important human-written patterns:

1. explicit point-to-point answers to reviewer questions
2. explicit handling of minor weaknesses without over-investing budget

That makes the output still feel unlike many real rebuttals, especially in venues where reviewers separate:

- strengths / weaknesses
- questions
- minor weaknesses or minor comments

## Recommended Approach

### Structure layer

Under each reviewer block, the formatter should support:

- `W1 / W2 / W3` for main weaknesses
- `Q1 / Q2 / Q3` for direct questions
- either:
  - `M1 / M2 / M3` for distinct minor points, or
  - one merged `Minor points` section when several minor items are highly similar

### Default minor-point rule

Default to:

- one sentence per minor point
- if two or more minor points are obviously similar, merge them into one short `Minor points` paragraph

This keeps minor issues covered without wasting budget.

## Proposed Files

```text
skills/super-rebuttal/scripts/
  build_reviewer_outline.py
tests/
  test_reviewer_outline.py
```

## Success Criteria

- the project can parse and represent weaknesses, questions, and minor points separately
- docs explicitly mention `W#`, `Q#`, and minor-point handling
- formatter guidance now matches the point-to-point structure used in many human rebuttals
