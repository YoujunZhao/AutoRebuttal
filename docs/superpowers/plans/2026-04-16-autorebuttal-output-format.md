# AutoRebuttal Output Format Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an `output=text|md` parameter, defaulting to `text`, for both `/rebuttal` and `/rebuttal_revise`.

**Architecture:** Normalize the user-facing parameter once into bundle-building helpers and expose a small validator in `response_modes.py`. Then document the new parameter in the command surfaces, skill contract, and README.

**Tech Stack:** Python standard library, unittest, Markdown docs.

---

### Task 1: Lock the parameter behavior with tests

**Files:**
- Modify: `tests/test_draft_bundle.py`
- Modify: `tests/test_revision_bundle.py`
- Modify: `tests/test_response_modes.py`
- Modify: `tests/test_plugin_surface.py`
- Modify: `tests/test_install_wrappers.py`

- [ ] Add failing tests for default `text`, explicit `md`, and invalid values.
- [ ] Run the targeted test files and confirm the new assertions fail for the right reason.

### Task 2: Implement the normalized output-format surface

**Files:**
- Modify: `skills/auto-rebuttal/scripts/build_draft_bundle.py`
- Modify: `skills/auto-rebuttal/scripts/build_revision_bundle.py`
- Modify: `skills/auto-rebuttal/scripts/response_modes.py`

- [ ] Add a validator that accepts only `text` and `md`.
- [ ] Thread `output` through both bundle builders as `output_format`.
- [ ] Keep default behavior backward compatible by using `text` when omitted.
- [ ] Run the targeted bundle/response tests until green.

### Task 3: Document the parameter everywhere users will look

**Files:**
- Modify: `commands/rebuttal.md`
- Modify: `commands/rebuttal_revise.md`
- Modify: `skills/auto-rebuttal/SKILL.md`
- Modify: `skills/auto-rebuttal/references/input-contract.md`
- Modify: `README.md`
- Modify: `README.zh-CN.md`

- [ ] Add `output=text|md` examples to both command surfaces.
- [ ] Explain the default `text` behavior and optional `md` override in the skill/reference docs.
- [ ] Add the parameter to the README parameter table and example invocations.

### Task 4: Verify and review

**Files:**
- No new source files expected

- [ ] Run targeted tests first.
- [ ] Run the full test suite.
- [ ] Request code review on the branch diff.
- [ ] If review is clean, integrate back to `main` and push.
