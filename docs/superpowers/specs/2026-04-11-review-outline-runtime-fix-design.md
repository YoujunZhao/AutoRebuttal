# SuperRebuttal Review Outline Runtime Fix Design

**Date:** 2026-04-11
**Project:** SuperRebuttal
**Status:** Approved by delegated default

## Goal

Make SuperRebuttal correctly handle real OpenReview-style review PDFs like `general3d_review.pdf`, including:

- image-based review PDFs that do not expose a text layer
- `Main Weaknesses` / `Weaknesses`
- `Key Questions For Authors`
- optional `Minor Weaknesses` or `Minor comments`

The final runtime goal is that the default formatter can produce reviewer blocks with `W#`, `Q#`, and `M#` structure instead of degrading to `W#` only.

## Problem

The current repository has two separate gaps:

1. `build_input_bundle.py` assumes review PDFs are text-extractable. Real OpenReview review exports can be image-based, so the current path fails before structured parsing begins.
2. `build_reviewer_outline.py` only recognizes a narrow set of section headers. Real reviews often use headers such as `Strengths And Weaknesses`, `Main Weaknesses`, and `Key Questions For Authors`, which are currently missed or partially misclassified.

This combination means the runtime can still produce reviewer-by-reviewer prose with only `W#` items, even though the product docs already promise `Q#` and minor-point handling.

## Recommended Approach

### 1. Add a review-PDF image fallback

When text extraction fails for a review PDF:

- render the first review pages to PNG images
- keep the review entry in the input bundle instead of failing the whole bundle
- mark the review entry with an explicit extraction mode so the runtime knows it must inspect rendered pages

This keeps the review artifact usable for downstream reasoning in Codex/Claude-style environments.

### 2. Upgrade reviewer-outline parsing for real OpenReview layouts

Expand the outline parser so it can:

- ignore strengths instead of turning them into `W#`
- recognize `Main Weaknesses` and similar weakness headers
- recognize `Key Questions For Authors` and related question headers
- recognize minor-point headers when present
- preserve `W#`, `Q#`, and `M#` numbering in a stable structure

### 3. Tighten runtime instructions

The command and skill entrypoints should require this order:

1. build the input bundle
2. if a review PDF is image-based, inspect rendered page images instead of re-asking for pasted review text
3. build a reviewer outline with `W/Q/M`
4. only then draft the rebuttal

## Proposed Files

```text
skills/super-rebuttal/scripts/
  build_input_bundle.py
  build_reviewer_outline.py
  render_review_pdf_pages.py
commands/
  rebuttal.md
skills/super-rebuttal/
  SKILL.md
tests/
  test_input_bundle.py
  test_plugin_surface.py
  test_reviewer_outline.py
  test_skill_metadata.py
  test_render_review_pdf_pages.py
```

## Success Criteria

- `general3d_review.pdf` no longer causes review-bundle construction to hard fail
- image-based review PDFs produce a usable fallback artifact with rendered page images
- OpenReview-style section headers produce `Q#` when questions are present
- strengths are not mislabeled as weaknesses
- runtime docs explicitly require `W/Q/M` outline construction before drafting
