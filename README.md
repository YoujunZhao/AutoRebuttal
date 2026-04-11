# SuperRebuttal

[Chinese README](README.zh-CN.md)

SuperRebuttal is a rebuttal workflow package for coding agents. It is shaped like a small plugin-first superpower package: the repository contains the installation surfaces, the internal `super-rebuttal` skill, the prompt entrypoint, the policy notes, and the tests that define what the project can honestly claim today.

It is built for one job: help authors turn a paper, reviews, and explicit rebuttal constraints into a structured, evidence-first response without fabricating experiments, gains, or citations.

The current package also supports review PDF ingestion, so a paper PDF and a review PDF can both be part of the working input bundle. If a review PDF is image-based instead of text-based, the bundle now falls back to rendered page images instead of failing outright.

## What It Is

SuperRebuttal is not just a copied skill folder. It is a small rebuttal package that is meant to be installed, then invoked as a workflow.

The package is designed around a few core ideas:

- rebuttals should start with issue extraction, not prose generation
- unsupported venues should fall back to explicit user budgets instead of fake built-in support
- missing evidence should become placeholders such as `XX` or `[RESULT-TO-FILL]`, not invented numbers
- installation claims and venue claims should stay narrower than what the repo can actually prove
- reviewer stance analysis should happen before the final draft
- a global strategy memo should exist before reviewer-by-reviewer prose

## How It Works

SuperRebuttal starts from the moment an author brings a paper and reviews into the session. Instead of jumping straight to final prose, it first identifies the response format, organizes the review concerns, builds a reviewer outline, models reviewer stance and attitude, builds a global strategy memo, and only then drafts.

In practice, the flow is:

1. install the package in the host tool
2. provide manuscript context, paper PDFs, and review PDF files when available
3. determine the response format and budget
4. build a reviewer outline with `W#`, `Q#`, and minor-point structure when the review supports it
5. build reviewer cards with reviewer stance, movability, attitude, and primary concerns
6. cluster shared reviewer concerns
7. produce a global strategy memo before reviewer-by-reviewer prose
8. allocate the character budget before drafting
9. draft the final rebuttal text
10. keep unresolved evidence as explicit placeholders

This keeps the workflow closer to how strong rebuttals are actually written: first understand the concern set, then decide what can be answered directly, what should be acknowledged, and what must stay as a bounded placeholder.

The project now explicitly models reviewer stance and attitude before prose generation. The goal is to sound less like a generic template and more like a targeted rebuttal.

That also means the workflow now tries to identify:

- which reviewers are swing reviewers
- which concerns are global themes across multiple reviewers
- where the draft should reassure, clarify, de-escalate, or sharply distinguish prior work

## Human-Like Rebuttal Layer

SuperRebuttal now includes:

- **reviewer cards** for reviewer stance, movability, attitude, and primary concerns
- a **global strategy memo** to decide what should lead the rebuttal
- explicit **character-budget planning** so the opening, body, and closing are sized before drafting

This is the main difference between the upgraded workflow and the older generic style.

## Venue-Aware Formatting Defaults

- **ICLR**
  uses a brief global summary first, then reviewer blocks
- **ICML**
  uses reviewer blocks only, with a `5000`-character per-reviewer default
- **NeurIPS**
  uses reviewer blocks only, with a `10000`-character per-reviewer default
- **AAAI**
  uses reviewer blocks only, with a `2500`-character per-reviewer project preset
- **CVPR / ICCV / ECCV**
  use a brief summary to all reviewers first, then reviewer blocks, and budget the response like a one-page rebuttal-PDF equivalent

Inside each reviewer block, the formatter should prefer `W1 / W2 / W3` point-to-point responses instead of one merged paragraph.

It should also support:

- `Q1 / Q2 / Q3` for direct reviewer questions
- short `M1 / M2 / M3` responses for minor points
- or one merged `Minor points` section when several minor comments are highly similar

For OpenReview-style review exports, the parser should preserve headers such as `Main Weaknesses`, `Key Questions For Authors`, and `Minor Weaknesses` instead of flattening everything into `W#`.

When a reviewer asks for empirical evidence, the formatter can insert an experiment placeholder table with `XX` values instead of fabricated numbers.

User-supplied parameters always override these venue defaults. If the user gives `per_reviewer=5000`, `shared_total=6000`, or `global_summary=false`, those instructions win even when the venue preset says otherwise.

## Installation

Installation differs by host tool. Today, the repository only presents two installation surfaces as verified.

### Codex

The repo-level manager CLI performs real filesystem install/update/remove operations against the Codex user-home skill path:

```bash
python scripts/superrebuttal_manager.py codex install
python scripts/superrebuttal_manager.py codex update
python scripts/superrebuttal_manager.py codex remove
```

By default this manages `~/.agents/skills/super-rebuttal`. Manual details and path notes are documented in [`.codex/INSTALL.md`](.codex/INSTALL.md).

### Claude Code

The repository includes a Claude-style plugin shell:

- [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json)
- [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json)

This means the package is structured for Claude plugin installation and local marketplace registration.

Important: the project does **not** currently claim public official marketplace publication. What is verified today is the plugin-shaped repository layout, not a public marketplace listing.

The manager CLI follows the Claude plugin command model and prints the commands you should run:

```bash
python scripts/superrebuttal_manager.py claude install
python scripts/superrebuttal_manager.py claude update
python scripts/superrebuttal_manager.py claude remove
```

If you want to install it through the Claude plugin workflow, use the local marketplace shape that already ships in this repo:

```text
/plugin marketplace add YoujunZhao/SuperRebuttal
/plugin install super-rebuttal@super-rebuttal-dev
```

After that, the quickest Claude-style entrypoint is:

```text
/rebuttal
```

## How To Use It

After installation, there are two practical invocation styles:

- **Use the `rebuttal` command**
- **Use the `super-rebuttal` skill**

The exact UI differs by host tool, but the working intent is the same: tell the agent to enter the SuperRebuttal workflow, then provide the paper, the reviews, and the response budget.

### What is the difference between `rebuttal` and `super-rebuttal`?

- **`rebuttal`**
  This is the easier command-style entrypoint. Use it when you just want to start the workflow quickly.

- **`super-rebuttal`**
  This is the underlying skill / workflow engine. Use it when you want to invoke the skill explicitly.

In short: `rebuttal` is the front door, and `super-rebuttal` is the actual engine behind it.

### Invocation Examples

Use the `rebuttal` command:

```text
Use the `rebuttal` command. I will paste the abstract, the main claims, and three reviewer comments. This is per-reviewer mode with 5000 characters each.
```

Use the `super-rebuttal` skill:

```text
Use the `super-rebuttal` skill. This is a shared-global mode rebuttal with a total limit of 6000 characters. First cluster shared concerns, then draft the final response.
```

If the venue format is unclear, give the budget explicitly:

```text
Use the `super-rebuttal` skill. Ignore venue defaults and use per-reviewer mode with 4000 characters per reviewer.
```

Use the Claude-style command directly:

```text
/rebuttal
```

## The Basic Workflow

1. **Install SuperRebuttal** into Codex or a Claude-style plugin environment.
2. **Provide inputs**: paper PDF, review PDF, manuscript text, or a faithful summary, plus reviews.
   If a review PDF is image-based, SuperRebuttal should continue through rendered page images instead of asking for pasted review text immediately.
3. **Choose a budgeting mode**:
   - `per-reviewer mode`
   - `shared-global mode`
4. **Generate the issue map** before asking for final prose.
   This issue map should build a reviewer outline first, so `W#`, `Q#`, and minor points are preserved in the final draft.
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

- Repo-level manager CLI via [`scripts/superrebuttal_manager.py`](scripts/superrebuttal_manager.py)
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

- [`scripts/superrebuttal_manager.py`](scripts/superrebuttal_manager.py)
- [`.codex/INSTALL.md`](.codex/INSTALL.md)
- [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json)
- [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json)
- [`commands/rebuttal.md`](commands/rebuttal.md)

### Canonical Rebuttal Engine

- [`skills/super-rebuttal/SKILL.md`](skills/super-rebuttal/SKILL.md)
- [`skills/super-rebuttal/scripts/build_input_bundle.py`](skills/super-rebuttal/scripts/build_input_bundle.py)
- [`skills/super-rebuttal/scripts/render_review_pdf_pages.py`](skills/super-rebuttal/scripts/render_review_pdf_pages.py)
- [`skills/super-rebuttal/scripts/build_reviewer_outline.py`](skills/super-rebuttal/scripts/build_reviewer_outline.py)
- [`skills/super-rebuttal/scripts/build_reviewer_cards.py`](skills/super-rebuttal/scripts/build_reviewer_cards.py)
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
