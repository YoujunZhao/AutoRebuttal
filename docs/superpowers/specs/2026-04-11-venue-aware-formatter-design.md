# SuperRebuttal Venue-Aware Formatter Design

**Date:** 2026-04-11
**Project:** SuperRebuttal
**Status:** Approved by delegated default

## Goal

Make SuperRebuttal venue-aware at the formatting layer so that rebuttal drafts follow venue-specific structure, budgeting defaults, and point-to-point reviewer formatting.

## Required Venue Defaults

- **ICLR**
  - short global summary first
  - then `Reviewer 1 -> W1 / W2 / W3 -> Reviewer 2 -> ...`
- **ICML**
  - no global summary by default
  - per-reviewer formatting
  - default `5000` characters per reviewer when explicit user value is absent
- **NeurIPS**
  - no global summary by default
  - per-reviewer formatting
  - default `10000` characters per reviewer when explicit user value is absent
- **AAAI**
  - no global summary by default
  - per-reviewer formatting
  - project preset `2500` characters per reviewer
- **CVPR / ICCV / ECCV**
  - short summary to all reviewers first
  - then point-to-point reviewer responses
  - overall layout should be planned as a one-page rebuttal-PDF equivalent

## Output Structure

The formatter should default to:

- `Reviewer X`
  - `W1`
  - `W2`
  - `W3`

not one large paragraph per reviewer.

## Experiment Tables

When a reviewer asks for empirical evidence, the corresponding `W#` section should be able to emit a small local experiment placeholder table with `XX` values instead of fabricated numbers.

## Proposed Files

```text
skills/super-rebuttal/scripts/
  build_venue_format_plan.py
  build_experiment_placeholder_table.py
  allocate_rebuttal_budget.py
tests/
  test_venue_format_plan.py
  test_experiment_placeholder_table.py
  test_character_budget.py
```
