# AutoRebuttal Codex Install Simplification Design

**Date:** 2026-04-13
**Project:** AutoRebuttal
**Status:** Approved by delegated default

## Goal

Make Codex installation feel as simple as Superpowers installation.

## Problem

The current docs tell users to run:

- `python scripts/autorebuttal_manager.py codex install`

That works, but it is heavier than necessary for Codex native skill discovery. The result is that Codex installation feels more complicated than Superpowers, where the main path is:

- clone the repo
- create one skill symlink/junction
- restart Codex

## Recommended Approach

### Preferred install path

Adopt the Superpowers-style native discovery flow as the **preferred** Codex install path:

1. clone the repo to a stable location
2. create a junction/symlink from `~/.agents/skills/auto-rebuttal` to the repo's skill directory
3. restart Codex

### Quick install copy

Add a “tell Codex” quick-install line in README / Codex docs, mirroring the Superpowers pattern:

- fetch and follow `.codex/INSTALL.md`

### Manager CLI role

Keep the manager CLI, but demote it to:

- advanced / compatibility path
- optional local filesystem helper

That preserves existing automation without forcing every user through Python-based install steps.

## Proposed Files

```text
.codex/INSTALL.md
README.md
README.zh-CN.md
tests/test_install_wrappers.py
```

## Success Criteria

- README and `.codex/INSTALL.md` present clone + junction/symlink as the preferred Codex path
- Quick install copy mirrors the Superpowers pattern
- Update/uninstall instructions use the clone + junction mental model
- Tests lock the new preferred install path so the docs do not regress back to manager-first wording
