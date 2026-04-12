# SuperRebuttal Revise Mode Design

**Date:** 2026-04-12
**Project:** SuperRebuttal
**Status:** Approved by delegated default

## Goal

Add a second user-facing mode for SuperRebuttal:

- the existing full-auto `/rebuttal` flow still drafts from paper + reviews
- a new `/rebuttal_revies` flow polishes an already-written rebuttal

At the same time, tighten the default rebuttal formatting rule so `W#`, `Q#`, and `M#` labels always start on their own line.

## Problem

The current project only exposes the from-scratch drafting path. When a user already wrote a rebuttal and wants help tightening tone, shortening text, or improving structure, there is no dedicated command surface.

The current generated output also sometimes keeps reviewer labels inline in the same paragraph, for example:

`... We agree with the concern. W1. ... Q1. ...`

That makes the text look less like a human-written rebuttal letter and harder to paste into a submission system.

## Recommended Approach

### 1. Add a dedicated revise/polish command

Create a new command surface:

- `/rebuttal_revies`

This command should describe a workflow where the user provides:

- an existing rebuttal draft
- optional venue / budget constraints
- optional paper/review context for fact checking

The command should explicitly preserve the non-fabrication rule and make clear that this mode edits and tightens an existing rebuttal instead of rebuilding from zero.

### 2. Add an explicit workflow-mode resolver

Extend the response-mode surface so the package can distinguish:

- `draft-from-scratch`
- `revise-existing`

This keeps the command layer and future automation from relying only on prose instructions.

### 3. Add a rebuttal block formatter

Introduce a small helper script that normalizes reviewer labels so:

- `W1`, `W2`, `W3`
- `Q1`, `Q2`, `Q3`
- `M1`, `M2`, `M3`

start on a new line even if an upstream model emits them inline.

The formatter should be conservative:

- do not rewrite ordinary prose
- only insert line breaks before the recognized label pattern
- preserve existing blank lines where possible

## Proposed Files

```text
commands/
  rebuttal.md
  rebuttal_revies.md
skills/super-rebuttal/scripts/
  response_modes.py
  format_rebuttal_blocks.py
tests/
  test_response_modes.py
  test_plugin_surface.py
  test_rebuttal_block_format.py
  test_install_wrappers.py
README.md
README.zh-CN.md
skills/super-rebuttal/SKILL.md
```

## Success Criteria

- the repo exposes `/rebuttal_revies` as a documented command surface
- the package can resolve whether the workflow is drafting or revising
- a helper can normalize inline `W#/Q#/M#` markers into line-start reviewer items
- docs clearly explain the difference between `/rebuttal` and `/rebuttal_revies`
