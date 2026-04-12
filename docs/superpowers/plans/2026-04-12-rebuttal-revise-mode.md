# SuperRebuttal Revise Mode Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a dedicated rebuttal-polish command and enforce line breaks before `W#`, `Q#`, and `M#` labels.

**Architecture:** Add a new command surface for revise mode, a small workflow-mode resolver in the response-modes script, and a focused formatting helper that normalizes reviewer labels onto their own lines. Reflect the new mode and formatting rule across the skill docs and README surfaces.

**Tech Stack:** Python 3 standard library, Markdown, unittest

---

### Task 1: Add failing tests for the new command and formatter

**Files:**
- Create: `D:\rebuttalskill\.worktrees\rebuttal-revise-mode\tests\test_rebuttal_block_format.py`
- Modify: `D:\rebuttalskill\.worktrees\rebuttal-revise-mode\tests\test_response_modes.py`
- Modify: `D:\rebuttalskill\.worktrees\rebuttal-revise-mode\tests\test_plugin_surface.py`
- Modify: `D:\rebuttalskill\.worktrees\rebuttal-revise-mode\tests\test_install_wrappers.py`

- [ ] **Step 1: Add a failing test that requires inline `W#/Q#/M#` markers to be moved onto new lines**
- [ ] **Step 2: Add a failing response-mode test for `revise-existing`**
- [ ] **Step 3: Add failing surface tests for `commands/rebuttal_revies.md` and README mentions**
- [ ] **Step 4: Run the focused tests and confirm failure**

### Task 2: Implement the formatter and workflow-mode resolver

**Files:**
- Create: `D:\rebuttalskill\.worktrees\rebuttal-revise-mode\skills\super-rebuttal\scripts\format_rebuttal_blocks.py`
- Modify: `D:\rebuttalskill\.worktrees\rebuttal-revise-mode\skills\super-rebuttal\scripts\response_modes.py`

- [ ] **Step 1: Implement block formatting for `W#`, `Q#`, and `M#` labels**
- [ ] **Step 2: Extend response-mode resolution to distinguish drafting from revising**
- [ ] **Step 3: Re-run focused unit tests**

### Task 3: Add the revise command surface and update docs

**Files:**
- Modify: `D:\rebuttalskill\.worktrees\rebuttal-revise-mode\commands\rebuttal.md`
- Create: `D:\rebuttalskill\.worktrees\rebuttal-revise-mode\commands\rebuttal_revies.md`
- Modify: `D:\rebuttalskill\.worktrees\rebuttal-revise-mode\skills\super-rebuttal\SKILL.md`
- Modify: `D:\rebuttalskill\.worktrees\rebuttal-revise-mode\README.md`
- Modify: `D:\rebuttalskill\.worktrees\rebuttal-revise-mode\README.zh-CN.md`
- Modify: `D:\rebuttalskill\.worktrees\rebuttal-revise-mode\skills\super-rebuttal\references\human-rebuttal-style.md`

- [ ] **Step 1: Document the difference between `/rebuttal` and `/rebuttal_revies`**
- [ ] **Step 2: Add the line-break formatting rule to the style guidance**
- [ ] **Step 3: Re-run surface tests**

### Task 4: Verify and finish

- [ ] **Step 1: Run the full test suite**
- [ ] **Step 2: Run `py_compile` on the new Python scripts**
- [ ] **Step 3: Request code review**
- [ ] **Step 4: Finish the development branch**
