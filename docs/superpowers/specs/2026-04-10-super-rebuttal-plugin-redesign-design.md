# SuperRebuttal Plugin-First Redesign

**Date:** 2026-04-10
**Project:** SuperRebuttal
**Status:** Approved by delegated default

## Why Redesign

The current repository is shaped like a standalone skill package with install wrappers. That is no longer the desired product shape.

The new goal is to make SuperRebuttal look and install more like `superpowers`:

- a plugin-first repository
- clear installation surfaces per host tool
- a workflow-focused README
- reusable internal skills rather than a lone skill folder presented as the whole product

## Product Direction

SuperRebuttal should become a **rebuttal workflow plugin / superpower package**, not merely a skill repository.

The repository itself should be the installable unit. Inside it, the rebuttal logic can still live as skills or prompts, but the user-facing product should be:

- "Install this plugin / package"
- "Use this workflow"

not:

- "Copy this one skill folder manually"

## Supported Installation Surfaces

### Verified first-class targets

These are the only installation targets we should advertise as first-class in the README unless we validate more:

1. **Codex**
   - install by telling Codex to fetch and follow a repo-local `.codex/INSTALL.md`
   - mirror the `superpowers` pattern

2. **Claude Code plugin**
   - install via `.claude-plugin/plugin.json`
   - optionally via `.claude-plugin/marketplace.json` for local marketplace testing

### Non-first-class targets

Do not advertise other agent ecosystems as supported unless we verify them end to end.

That means:

- remove or downplay current OpenClaw claims unless we can truly verify them
- avoid broad claims like "works everywhere that supports skills"

## README Truthfulness Rules

The README should only claim:

- installation flows we have actually tested
- venue / rebuttal formats we can actually explain and validate
- workflow steps that exist in the repository

Do not say "supports X conference" unless the repo contains:

- explicit logic or references for that format
- tests or fixtures proving the expected behavior

For anything not verified, the README should instead say:

- users can supply explicit per-review or global character budgets
- the workflow can still operate in generic mode

## Rebuttal Format Support Model

The project should distinguish between:

### 1. Verified format templates

These are venue/form families where we can justify a built-in template because we have:

- official public rules
- repository fixtures
- tests covering the budgeting / output mode selection

### 2. Generic manual-budget mode

For all other venues, the workflow should ask for:

- per-reviewer budget, for example "5000 characters each"
- or one shared rebuttal budget, for example "total 6000 characters"

This generic mode should also cover CV-style shared responses where all reviewers are answered in one block.

## Recommended Verified Support Scope for v2

Keep the verified scope intentionally small:

- `per-reviewer response mode`
- `shared global response mode`
- venue-policy references for a small set of public ML venues

Do **not** market these venue references as full support unless the workflow actually uses them in a testable way.

In practice, README language should shift from:

- "supports ICLR / NeurIPS / ICML / ARR"

to something like:

- "includes checked reference notes for ICLR, NeurIPS, ICML, and ARR-style author responses"
- "tested output modes today are per-reviewer budgeting and shared-global budgeting"

## New Repository Shape

```text
SuperRebuttal/
  README.md
  .codex/
    INSTALL.md
  .claude-plugin/
    plugin.json
    marketplace.json
  commands/
    rebuttal.md
  skills/
    super-rebuttal/
      SKILL.md
      references/
      examples/
      scripts/
  tests/
    ...
```

Optional future folders:

- `agents/`
- `hooks/`
- `docs/`

## Workflow Story for README

The README should explain the product as a workflow:

1. Install the plugin / package
2. Provide manuscript and reviews
3. Choose or infer rebuttal mode
4. Normalize reviewer concerns
5. Select budgeting mode
6. Draft strategy
7. Produce final rebuttal text
8. Mark unresolved evidence with placeholders instead of fabricating results

This flow is more important than listing file paths.

## Internal Architecture

Keep the rebuttal engine layered:

- **plugin shell**: installation, commands, marketplace metadata
- **workflow skill**: analysis + drafting instructions
- **references**: venue notes, playbook, truthfulness rules
- **tests**: installation surfaces and format selection logic

## Test Strategy for the Redesign

We should add tests for:

- Codex install docs and path assumptions
- Claude plugin manifest presence and basic validity
- local marketplace metadata presence
- command file presence
- supported rebuttal mode selection:
  - per-reviewer mode
  - shared-global mode

If a venue mode is named in README as supported, add a fixture or test that demonstrates how it resolves.

## Documentation Rules

The rewritten README must:

- explain the superpower/plugin workflow
- distinguish verified support from generic fallback
- stop overselling venue support
- clearly explain the two budgeting styles:
  - per reviewer
  - one shared rebuttal
- state that unsupported or unverified venues should be driven by explicit user limits

## Scope Boundary

This redesign does **not** add:

- automatic experiment execution
- venue submission automation
- guaranteed support for every conference format

It mainly changes product shape, installation model, truthfulness, and documentation clarity.
