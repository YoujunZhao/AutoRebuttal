# AutoRebuttal Autoexperiment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add `autoexperiment` plus a new `/experiment-bridge` workflow lane that can auto-route reviewer experiment requests into a bounded supplementary-evidence workflow.

**Architecture:** Normalize `autoexperiment` in the shared response-mode helpers and bundle builders, add a new command surface plus a script that builds experiment request bundles from review/rebuttal context, and update docs/tests to keep the contract honest.

**Tech Stack:** Python standard library, Markdown docs, unittest.

---

### Task 1: Lock the new contract with tests

**Files:**
- Modify: `tests/test_response_modes.py`
- Modify: `tests/test_draft_bundle.py`
- Modify: `tests/test_revision_bundle.py`
- Modify: `tests/test_plugin_surface.py`
- Modify: `tests/test_install_wrappers.py`

- [ ] Add failing tests for default `autoexperiment=false`, explicit `autoexperiment=true`, and invalid values.
- [ ] Add docs-surface tests for a new `commands/experiment-bridge.md`.
- [ ] Run the targeted tests and confirm they fail for the missing feature, not for syntax errors.

### Task 2: Implement the normalized parameter surface

**Files:**
- Modify: `skills/auto-rebuttal/scripts/response_modes.py`
- Modify: `skills/auto-rebuttal/scripts/build_draft_bundle.py`
- Modify: `skills/auto-rebuttal/scripts/build_revision_bundle.py`

- [ ] Add a shared validator for `autoexperiment=true|false`.
- [ ] Thread the normalized `auto_experiment` field into draft and revision bundles.
- [ ] Extend CLI arguments for both bundle builders.

### Task 3: Add the experiment bridge lane

**Files:**
- Create: `commands/experiment-bridge.md`
- Create: `skills/auto-rebuttal/scripts/build_experiment_request_bundle.py`

- [ ] Define the command contract for `/experiment-bridge`.
- [ ] Build a helper that extracts experiment requests into a structured bundle.
- [ ] Keep the behavior bounded and blocker-aware when no runnable experiment workspace exists.

### Task 4: Update skill and README surfaces

**Files:**
- Modify: `skills/auto-rebuttal/SKILL.md`
- Modify: `skills/auto-rebuttal/references/input-contract.md`
- Modify: `commands/rebuttal.md`
- Modify: `commands/rebuttal_revise.md`
- Modify: `README.md`
- Modify: `README.zh-CN.md`

- [ ] Document `autoexperiment`.
- [ ] Document `/experiment-bridge`.
- [ ] Explain that the feature auto-runs the supplementary-evidence lane, not fabricated results.

### Task 5: Verify and review

**Files:**
- No additional source files expected

- [ ] Run targeted tests.
- [ ] Run the full suite.
- [ ] Request code review on the branch diff.
- [ ] If clean, merge back to `main` and push.
