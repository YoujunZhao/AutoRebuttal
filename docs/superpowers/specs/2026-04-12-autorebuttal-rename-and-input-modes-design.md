# AutoRebuttal Rename and Input Modes Design

**Date:** 2026-04-12
**Project:** AutoRebuttal
**Status:** Approved by delegated default

## Goal

Rename the project from `SuperRebuttal` to `AutoRebuttal` and tighten the product contract around two user-facing modes:

- `/rebuttal` for drafting from paper + reviews
- `/rebuttal_revise` for polishing an existing rebuttal

Both modes should automatically distinguish PDF-based versus text-based inputs for the artifacts they accept.

## Product Rules

### `/rebuttal`

The drafting mode must support:

- `paper PDF`
- `review PDF`
- `review text`

The system should auto-detect whether a provided review artifact is a PDF or text source and then route it through the correct handling path.

### `/rebuttal_revise`

The revise mode must support:

- `rebuttal PDF`
- `rebuttal text`
- optional `paper PDF`

The system should auto-detect whether the provided rebuttal artifact is PDF or text and then route it through the correct handling path.

## Recommended Approach

### 1. Rename the package consistently

Rename product-facing surfaces from `SuperRebuttal` / `super-rebuttal` to:

- `AutoRebuttal`
- `auto-rebuttal`

This includes:

- README and README.zh-CN
- command docs
- skill metadata and folder naming
- manager CLI strings and defaults
- plugin metadata
- tests
- GitHub repository metadata and remote URL

### 2. Replace the mistyped revise command

The temporary `/rebuttal_revies` surface should be replaced by the final command:

- `/rebuttal_revise`

The old typo should be removed from docs and tests so the wrong spelling stops spreading.

### 3. Add real artifact-detection helpers

Introduce concrete scripts that normalize input bundles instead of leaving detection entirely in prompt text.

Recommended split:

- drafting bundle builder for `/rebuttal`
- revision bundle builder for `/rebuttal_revise`

Each bundle builder should:

- accept PDF paths and text-file paths
- classify inputs as `pdf` or `text`
- extract or preserve content accordingly
- keep enough metadata for downstream reasoning

### 4. Preserve current honest fallback behavior

For image-based PDFs:

- drafting mode should keep review PDFs through rendered page images
- revise mode should keep rebuttal PDFs through extracted text when available, or fail clearly if the rebuttal PDF has no usable text layer and no image-derived path exists yet

The key rule is honesty: the package should never pretend it parsed a document that it actually did not parse.

## Proposed Files

```text
commands/
  rebuttal.md
  rebuttal_revise.md
scripts/
  autorebuttal_manager.py
skills/
  auto-rebuttal/
    SKILL.md
    scripts/
      build_draft_bundle.py
      build_revision_bundle.py
      detect_input_artifact.py
tests/
  test_draft_bundle.py
  test_revision_bundle.py
  test_manager_cli.py
  test_plugin_surface.py
  test_install_wrappers.py
  test_skill_metadata.py
README.md
README.zh-CN.md
```

## Success Criteria

- the product name is `AutoRebuttal` across user-facing surfaces
- `/rebuttal` supports paper PDF plus review PDF or review text with auto-detection
- `/rebuttal_revise` supports rebuttal PDF or rebuttal text, with optional paper PDF
- the typo `/rebuttal_revies` is removed from current docs/tests
- GitHub repository metadata is renamed to `AutoRebuttal`
