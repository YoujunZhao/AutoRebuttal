# AutoRebuttal Rename and Input Modes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rename the project to AutoRebuttal, replace `/rebuttal_revies` with `/rebuttal_revise`, and add auto-detected PDF/text input bundles for drafting and revision modes.

**Architecture:** Keep the existing rebuttal workflow but rename the package and split artifact preparation into two explicit bundle builders: one for drafting (`paper + review inputs`) and one for revision (`rebuttal input + optional paper`). Update manager/plugin metadata, skill metadata, docs, tests, and GitHub repository state so the rename is consistent.

**Tech Stack:** Python 3 standard library, Markdown, unittest, GitHub REST API via shell

---

### Task 1: Lock the rename and mode contract with failing tests

**Files:**
- Create: `D:\rebuttalskill\.worktrees\autorebuttal-rename-revise\tests\test_draft_bundle.py`
- Create: `D:\rebuttalskill\.worktrees\autorebuttal-rename-revise\tests\test_revision_bundle.py`
- Modify: `D:\rebuttalskill\.worktrees\autorebuttal-rename-revise\tests\test_plugin_surface.py`
- Modify: `D:\rebuttalskill\.worktrees\autorebuttal-rename-revise\tests\test_install_wrappers.py`
- Modify: `D:\rebuttalskill\.worktrees\autorebuttal-rename-revise\tests\test_manager_cli.py`
- Modify: `D:\rebuttalskill\.worktrees\autorebuttal-rename-revise\tests\test_skill_metadata.py`

- [ ] **Step 1: Add failing tests for `/rebuttal_revise` and remove `/rebuttal_revies` from the current contract**
- [ ] **Step 2: Add failing tests for draft-mode review input auto-detection (pdf vs text)**
- [ ] **Step 3: Add failing tests for revise-mode rebuttal input auto-detection (pdf vs text)**
- [ ] **Step 4: Add failing tests for AutoRebuttal naming in manager/plugin/README surfaces**
- [ ] **Step 5: Run focused tests and confirm failure**

### Task 2: Implement input bundle detection helpers

**Files:**
- Create: `D:\rebuttalskill\.worktrees\autorebuttal-rename-revise\skills\auto-rebuttal\scripts\detect_input_artifact.py`
- Create: `D:\rebuttalskill\.worktrees\autorebuttal-rename-revise\skills\auto-rebuttal\scripts\build_draft_bundle.py`
- Create: `D:\rebuttalskill\.worktrees\autorebuttal-rename-revise\skills\auto-rebuttal\scripts\build_revision_bundle.py`

- [ ] **Step 1: Implement pdf-vs-text artifact classification**
- [ ] **Step 2: Implement draft-mode bundle creation for paper + review inputs**
- [ ] **Step 3: Implement revise-mode bundle creation for rebuttal input + optional paper**
- [ ] **Step 4: Re-run focused input-bundle tests**

### Task 3: Rename the package surfaces

**Files:**
- Modify: `D:\rebuttalskill\.worktrees\autorebuttal-rename-revise\scripts\superrebuttal_manager.py`
- Modify or replace: `D:\rebuttalskill\.worktrees\autorebuttal-rename-revise\scripts\autorebuttal_manager.py`
- Rename/update: `D:\rebuttalskill\.worktrees\autorebuttal-rename-revise\skills\super-rebuttal\...`
- Modify: `D:\rebuttalskill\.worktrees\autorebuttal-rename-revise\.claude-plugin\plugin.json`
- Modify: `D:\rebuttalskill\.worktrees\autorebuttal-rename-revise\.claude-plugin\marketplace.json`
- Modify: `D:\rebuttalskill\.worktrees\autorebuttal-rename-revise\commands\rebuttal.md`
- Create: `D:\rebuttalskill\.worktrees\autorebuttal-rename-revise\commands\rebuttal_revise.md`

- [ ] **Step 1: Rename product-facing strings to AutoRebuttal / auto-rebuttal**
- [ ] **Step 2: Replace `/rebuttal_revies` with `/rebuttal_revise`**
- [ ] **Step 3: Point command docs at the new input bundle rules**
- [ ] **Step 4: Re-run command/metadata tests**

### Task 4: Update docs and GitHub metadata

**Files:**
- Modify: `D:\rebuttalskill\.worktrees\autorebuttal-rename-revise\README.md`
- Modify: `D:\rebuttalskill\.worktrees\autorebuttal-rename-revise\README.zh-CN.md`
- Modify: `D:\rebuttalskill\.worktrees\autorebuttal-rename-revise\skills\auto-rebuttal\SKILL.md`

- [ ] **Step 1: Rewrite docs to describe AutoRebuttal and the two final commands**
- [ ] **Step 2: Document auto-detection behavior for review and rebuttal inputs**
- [ ] **Step 3: Rename the GitHub repository metadata and remote target to AutoRebuttal**
- [ ] **Step 4: Re-run full suite**

### Task 5: Verify, review, and finish

- [ ] **Step 1: Run full tests**
- [ ] **Step 2: Run py_compile for new scripts**
- [ ] **Step 3: Request code review**
- [ ] **Step 4: Finish the development branch**
