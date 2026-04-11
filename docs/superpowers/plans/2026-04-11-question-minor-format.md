# SuperRebuttal Question and Minor Format Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extend point-to-point rebuttal formatting so each reviewer block can explicitly contain `W#`, `Q#`, and minor-point sections, with short or merged handling for minor issues.

**Architecture:** Add a reviewer-outline builder that parses extracted review text into weaknesses, questions, and minor items. Then update the command, skill, and docs so the formatter requires `W/Q/M`-aware structure before final drafting.

**Tech Stack:** Python 3 standard library, Markdown, git

---

### Task 1: Add failing tests for W/Q/minor-aware formatting

**Files:**
- Create: `D:\rebuttalskill\.worktrees\question-minor-format\tests\test_reviewer_outline.py`
- Modify: `D:\rebuttalskill\.worktrees\question-minor-format\tests\test_plugin_surface.py`
- Modify: `D:\rebuttalskill\.worktrees\question-minor-format\tests\test_skill_metadata.py`
- Modify: `D:\rebuttalskill\.worktrees\question-minor-format\tests\test_install_wrappers.py`

- [ ] **Step 1: Add a failing reviewer-outline test**
- [ ] **Step 2: Require command and skill docs to mention `Q#` and minor handling**
- [ ] **Step 3: Require README to mention `W#`, `Q#`, and minor-point behavior**
- [ ] **Step 4: Run focused tests and confirm failure**

### Task 2: Implement reviewer-outline parsing

**Files:**
- Create: `D:\rebuttalskill\.worktrees\question-minor-format\skills\super-rebuttal\scripts\build_reviewer_outline.py`

- [ ] **Step 1: Implement outline parsing for weaknesses / questions / minor points**
- [ ] **Step 2: Re-run outline tests**

### Task 3: Reflect the new structure in entrypoints and docs

**Files:**
- Modify: `D:\rebuttalskill\.worktrees\question-minor-format\commands\rebuttal.md`
- Modify: `D:\rebuttalskill\.worktrees\question-minor-format\skills\super-rebuttal\SKILL.md`
- Modify: `D:\rebuttalskill\.worktrees\question-minor-format\skills\super-rebuttal\references\human-rebuttal-style.md`
- Modify: `D:\rebuttalskill\.worktrees\question-minor-format\README.md`
- Modify: `D:\rebuttalskill\.worktrees\question-minor-format\README.zh-CN.md`

- [ ] **Step 1: Update formatter rules to include `Q#` and minor-point handling**
- [ ] **Step 2: Re-run README / surface tests**

### Task 4: Verify and finish

- [ ] **Step 1: Run full test suite**
- [ ] **Step 2: Run `py_compile` on new Python files**
- [ ] **Step 3: Finish the development branch**
