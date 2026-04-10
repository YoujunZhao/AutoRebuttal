# SuperRebuttal

[中文文档](README.zh-CN.md)

SuperRebuttal is a rebuttal workflow package for coding agents. It is shaped like a small plugin-first superpower package: the repository contains the installation surfaces, the internal `super-rebuttal` skill, the prompt entrypoint, the policy notes, and the tests that define what the project can honestly claim today.

It is built for one job: help authors turn a paper, reviews, and explicit rebuttal constraints into a structured, evidence-first response without fabricating experiments, gains, or citations.

## What It Is

SuperRebuttal is not just a copied skill folder. It is a small rebuttal package that is meant to be installed, then invoked as a workflow.

The package is designed around a few core ideas:

- rebuttals should start with issue extraction, not prose generation
- unsupported venues should fall back to explicit user budgets instead of fake built-in support
- missing evidence should become placeholders such as `XX` or `[RESULT-TO-FILL]`, not invented numbers
- installation claims and venue claims should stay narrower than what the repo can actually prove

## How It Works

SuperRebuttal starts from the moment an author brings a paper and reviews into the session. Instead of jumping straight to final prose, it first identifies the response format, then organizes the review concerns, then drafts.

In practice, the flow is:

1. install the package in the host tool
2. provide manuscript context and reviews
3. determine the response format and budget
4. cluster shared reviewer concerns
5. produce a strategy-first response map
6. draft the final rebuttal text
7. keep unresolved evidence as explicit placeholders

This keeps the workflow closer to how strong rebuttals are actually written: first understand the concern set, then decide what can be answered directly, what should be acknowledged, and what must stay as a bounded placeholder.

## Installation

Installation differs by host tool. Today, the repository only presents two installation surfaces as verified.

### Codex

Tell Codex:

```text
Fetch and follow instructions from https://raw.githubusercontent.com/YoujunZhao/SuperRebuttal/refs/heads/codex/plugin-first-redesign/.codex/INSTALL.md
```

Manual Codex setup is documented in [`.codex/INSTALL.md`](.codex/INSTALL.md).

### Claude Code

The repository includes a Claude-style plugin shell:

- [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json)
- [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json)

This means the package is structured for Claude plugin installation and local marketplace registration.

Important: the project does **not** currently claim public official marketplace publication. What is verified today is the plugin-shaped repository layout, not a public marketplace listing.

## The Basic Workflow

1. **Install SuperRebuttal** into Codex or a Claude-style plugin environment.
2. **Provide inputs**: paper PDF, manuscript text, or a faithful summary, plus reviews.
3. **Choose a budgeting mode**:
   - `per-reviewer mode`
   - `shared-global mode`
4. **Generate the issue map** before asking for final prose.
5. **Draft the rebuttal** with evidence-first language.
6. **Mark missing evidence explicitly** with placeholders instead of fabrication.

### The Two Tested Budgeting Modes

- **`per-reviewer mode`**
  Use this when each reviewer gets a separate response budget, for example "5000 characters per reviewer."

- **`shared-global mode`**
  Use this when all reviewers are answered in one shared response, for example "6000 characters total."

The shared-global path is the correct generic fallback for many CV-style or forum-style rebuttals where the response is one combined block rather than separate reviewer slots.

## Verified Support Today

These are the only things the project should present as verified support today:

- Codex installation via [`.codex/INSTALL.md`](.codex/INSTALL.md)
- Claude plugin shell metadata via [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json)
- Local Claude marketplace metadata via [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json)
- A command entrypoint via [`commands/rebuttal.md`](commands/rebuttal.md)
- `per-reviewer mode`
- `shared-global mode`

## Checked Reference Notes

The repository also includes checked public reference notes for:

- ICLR
- NeurIPS
- ICML
- ARR-style author responses

Those notes live in [`skills/super-rebuttal/references/venue-policies.md`](skills/super-rebuttal/references/venue-policies.md).

That is intentionally weaker than saying "full venue support." These notes are reference material, not a promise that every year and every venue-specific rebuttal form is fully automated or fully tested.

## What's Inside

### Package Shell

- [`.codex/INSTALL.md`](.codex/INSTALL.md)
- [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json)
- [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json)
- [`commands/rebuttal.md`](commands/rebuttal.md)

### Canonical Rebuttal Engine

- [`skills/super-rebuttal/SKILL.md`](skills/super-rebuttal/SKILL.md)
- [`skills/super-rebuttal/scripts/response_modes.py`](skills/super-rebuttal/scripts/response_modes.py)
- [`skills/super-rebuttal/scripts/install_skill.py`](skills/super-rebuttal/scripts/install_skill.py)
- [`skills/super-rebuttal/scripts/package_skill.py`](skills/super-rebuttal/scripts/package_skill.py)
- [`skills/super-rebuttal/scripts/validate_budget.py`](skills/super-rebuttal/scripts/validate_budget.py)

### Reference Material

- [`skills/super-rebuttal/references/input-contract.md`](skills/super-rebuttal/references/input-contract.md)
- [`skills/super-rebuttal/references/rebuttal-playbook.md`](skills/super-rebuttal/references/rebuttal-playbook.md)
- [`skills/super-rebuttal/references/venue-policies.md`](skills/super-rebuttal/references/venue-policies.md)
- [`skills/super-rebuttal/references/source-notes.md`](skills/super-rebuttal/references/source-notes.md)

### Tests

- [`tests/test_plugin_surface.py`](tests/test_plugin_surface.py)
- [`tests/test_response_modes.py`](tests/test_response_modes.py)
- [`tests/test_install_wrappers.py`](tests/test_install_wrappers.py)

## Generic Fallback for Unsupported Venues

If the venue is not clearly covered, or if the venue rules for the current year are uncertain, do not pretend the package has a built-in template. Instead, provide an explicit budget and continue in generic mode:

- `per-reviewer mode`
- `shared-global mode`

This is the intended fallback behavior for unsupported or unverified venues.

## Limitations

- It does not run experiments.
- It does not fetch private reviews from submission systems.
- It does not claim support for every conference rebuttal format.
- It does not claim that checked venue notes are the same as tested venue automation.
- It does not claim public official Claude marketplace publication.
- It does not guarantee score improvement.

## Research Basis

The workflow is grounded in:

- public venue instructions
- public rebuttal studies and datasets
- explicit non-fabrication rules

Start here:

- [`skills/super-rebuttal/references/source-notes.md`](skills/super-rebuttal/references/source-notes.md)
- [`skills/super-rebuttal/references/rebuttal-playbook.md`](skills/super-rebuttal/references/rebuttal-playbook.md)
- [`skills/super-rebuttal/references/input-contract.md`](skills/super-rebuttal/references/input-contract.md)

## Project Status

- private-first
- plugin-first
- narrow by design in what it claims
- stronger on workflow discipline than on venue-specific automation
