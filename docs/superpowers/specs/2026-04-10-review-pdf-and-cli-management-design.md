# SuperRebuttal Review PDF and CLI Management Design

**Date:** 2026-04-10
**Project:** SuperRebuttal
**Status:** Approved by delegated default

## Goal

Extend SuperRebuttal so it can:

1. accept review PDFs as first-class input, not just paper PDFs
2. provide a real command-line management surface for install, update, and removal on Codex and Claude Code

## Problem

Today the project has two clear gaps:

- the input contract and tooling mention paper PDF, but review PDF is not handled as a first-class path
- installation is documented, but lifecycle management is not implemented as a unified CLI

## Recommended Approach

Use a two-part implementation:

### Part 1: PDF intake tooling

Add a standard-library PDF extraction helper plus an input-bundle builder.

The helper should:

- accept one paper PDF
- accept zero or more review PDFs
- extract best-effort text from each
- produce a structured JSON bundle for the rebuttal workflow

This is better than only updating prompt text because it gives the repo a real implementation surface.

### Part 2: Host management CLI

Add a repo-level management CLI with subcommands for:

- `codex install`
- `codex update`
- `codex remove`
- `claude install`
- `claude update`
- `claude remove`

Codex commands should directly manage the local discovery path.

Claude commands should follow the official plugin workflow model by surfacing or automating the marketplace/install/uninstall commands as far as the local environment allows.

## Alternatives Considered

### Option A: Prompt-only review PDF support

Only update docs and skill text to say review PDFs are accepted.

Why not:

- too weak
- does not create a testable implementation
- easy to regress

### Option B: Add external PDF dependency

Use `pypdf`, `pdfplumber`, or `PyMuPDF`.

Why not:

- repo guidance discourages new dependencies without explicit need
- current project is intentionally standard-library-first

### Option C: Standard-library best-effort extractor

Implement a best-effort extractor for text-based PDFs and clearly document limitations.

Why this is recommended:

- no new dependency
- testable
- materially improves support over the current state

## New User-Facing Capabilities

### Review PDF support

Supported inputs should become:

- paper PDF
- paper text
- review text
- review PDF
- mixed inputs, for example paper PDF plus review text plus one review PDF

### CLI lifecycle support

Users should be able to run commands like:

```bash
python scripts/superrebuttal_manager.py codex install
python scripts/superrebuttal_manager.py codex update
python scripts/superrebuttal_manager.py codex remove
python scripts/superrebuttal_manager.py claude install
python scripts/superrebuttal_manager.py claude update
python scripts/superrebuttal_manager.py claude remove
```

## Constraints

- keep runtime dependencies to Python standard library only
- keep Codex management real and file-system based
- keep Claude management aligned with official plugin command model
- do not pretend PDF extraction is perfect for every PDF generator
- continue forbidding fabricated experimental results

## Proposed Files

```text
scripts/
  superrebuttal_manager.py
skills/
  super-rebuttal/
    scripts/
      extract_pdf_text.py
      build_input_bundle.py
      response_modes.py
tests/
  test_pdf_extract.py
  test_input_bundle.py
  test_manager_cli.py
```

## Behavior Design

### PDF extraction

The extractor should:

- attempt text extraction from common text-based PDF streams
- work for many normal conference review PDFs
- fail clearly when extraction is not possible

### Input bundle builder

The builder should emit a JSON object with fields like:

- `paper`
- `reviews`
- `mode`
- `budget`
- `source_files`

### Codex management

- `install`: create or refresh the Codex skill link/junction
- `update`: validate that the existing target points at the current repo and refresh if needed
- `remove`: remove the installed link/junction

### Claude management

- `install`: print or execute the official `/plugin marketplace add` and `/plugin install` flow
- `update`: print or execute the install/update flow again
- `remove`: print or execute `/plugin uninstall ...`

If direct execution is not feasible from the local shell, the CLI should still provide exact commands for the user to paste into Claude Code.

## Documentation Changes

Update both READMEs to explain:

- review PDF is now a first-class supported input
- the new manager CLI exists
- exact install / update / remove commands for Codex and Claude
- current PDF extraction limitations

## Risks

### PDF parsing quality

Some PDFs will be image-based or encoded in a way that the best-effort extractor cannot recover.

Mitigation:

- fail clearly
- keep allowing direct review text as fallback
- document limitations

### Claude command execution

Claude plugin management happens through Claude's own command surface.

Mitigation:

- make the CLI produce exact official commands
- only execute them automatically if the environment safely supports it

## Success Criteria

- tests prove review PDF input files are accepted and bundled
- tests prove the management CLI exposes install/update/remove for both hosts
- README documents the new commands and input mode clearly
