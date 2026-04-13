# AutoRebuttal LaTeX Input and README Upgrade Design

**Date:** 2026-04-13
**Project:** AutoRebuttal
**Status:** Approved by delegated default

## Goal

Add three missing capabilities:

1. accept LaTeX paper input
2. when the paper input is LaTeX, support a dual output contract:
   - rebuttal text
   - modified LaTeX paper
3. upgrade the GitHub README with:
   - a complete workflow diagram
   - a parameter table explaining the supported inputs and controls

## Product Rules

### Paper input

`/rebuttal` should accept:

- paper PDF
- paper LaTeX file
- paper LaTeX project directory

`/rebuttal_revise` should accept:

- rebuttal PDF or rebuttal text
- optional paper PDF
- optional paper LaTeX file
- optional paper LaTeX project directory

### LaTeX output rule

If the paper input source type is LaTeX, the workflow must explicitly support two outputs:

- `rebuttal_text`
- `revised_latex_paper`

The codebase does not itself generate those final model-written outputs, but it should expose the contract clearly in the bundle/output helpers and in the command/skill docs.

## Recommended Approach

### 1. Add a paper-artifact detector

Keep review/rebuttal artifact detection separate from paper detection.

Paper detection should recognize:

- `.pdf` paper
- single `.tex` file
- directory containing `.tex` files

For LaTeX directories, collect all `.tex` files in deterministic order and preserve:

- root path
- detected entrypoint
- combined plain-text view
- per-file source map

### 2. Extend the draft and revision bundles

Both bundle builders should accept a generic `paper_input`.

For LaTeX paper input, the bundle should mark:

- `source_type = latex`
- `entrypoint`
- `latex_sources`
- `expected_outputs = ["rebuttal_text", "revised_latex_paper"]`

### 3. Add an explicit output helper

Add a small helper that packages the dual output contract for LaTeX workflows.

This gives the repo a concrete artifact-level definition of “output rebuttal and modified LaTeX paper”, rather than only describing it in prose.

### 4. Upgrade README surfaces

Add to README:

- a Mermaid workflow diagram
- a markdown parameter table

The table should cover both commands and the main inputs:

- command
- paper input
- review/rebuttal input
- venue
- budget controls
- phase / revise mode

The style can be informed by the ARIS README, but the capability claims must remain accurate to AutoRebuttal.

## Proposed Files

```text
skills/auto-rebuttal/scripts/
  detect_paper_artifact.py
  build_draft_bundle.py
  build_revision_bundle.py
  build_latex_output_package.py
tests/
  test_draft_bundle.py
  test_revision_bundle.py
  test_latex_output_package.py
  test_install_wrappers.py
  test_plugin_surface.py
README.md
README.zh-CN.md
commands/rebuttal.md
commands/rebuttal_revise.md
skills/auto-rebuttal/SKILL.md
skills/auto-rebuttal/references/input-contract.md
```

## Success Criteria

- `/rebuttal` accepts LaTeX paper input
- `/rebuttal_revise` accepts optional LaTeX paper input
- LaTeX paper bundles expose the dual output contract
- README includes a full workflow diagram
- README includes a parameter table
