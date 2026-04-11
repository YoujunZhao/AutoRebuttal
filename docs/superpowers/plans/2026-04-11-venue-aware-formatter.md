# SuperRebuttal Venue-Aware Formatter Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a venue-aware formatting layer that encodes venue-specific rebuttal structure, default budgets, `W1 / W2 / W3` point-to-point layout, and experiment placeholder tables.

**Architecture:** Add a formatter plan script that resolves venue defaults, extend budget allocation to become venue-sensitive, and add a helper for local experiment placeholder tables. Reflect the new rules in the command, skill, and docs.

**Tech Stack:** Python 3 standard library, Markdown, git

---

### Task 1: Add failing tests for venue-aware formatting and experiment tables

**Files:**
- Create: `D:\rebuttalskill\.worktrees\venue-aware-formatter\tests\test_venue_format_plan.py`
- Create: `D:\rebuttalskill\.worktrees\venue-aware-formatter\tests\test_experiment_placeholder_table.py`
- Modify: `D:\rebuttalskill\.worktrees\venue-aware-formatter\tests\test_character_budget.py`
- Modify: `D:\rebuttalskill\.worktrees\venue-aware-formatter\tests\test_install_wrappers.py`

- [ ] **Step 1: Add failing venue-format-plan tests for ICLR / ICML / NeurIPS / AAAI / CVPR / ICCV / ECCV**
- [ ] **Step 2: Add a failing experiment-placeholder-table test**
- [ ] **Step 3: Strengthen character-budget tests for reviewer-count-sensitive shared-global plans**
- [ ] **Step 4: Require docs to mention `W1 / W2 / W3`, AAAI, and CV-family summary behavior**
- [ ] **Step 5: Run focused tests and confirm failure**

### Task 2: Implement the venue-aware formatter and budget updates

**Files:**
- Create: `D:\rebuttalskill\.worktrees\venue-aware-formatter\skills\super-rebuttal\scripts\build_venue_format_plan.py`
- Create: `D:\rebuttalskill\.worktrees\venue-aware-formatter\skills\super-rebuttal\scripts\build_experiment_placeholder_table.py`
- Modify: `D:\rebuttalskill\.worktrees\venue-aware-formatter\skills\super-rebuttal\scripts\allocate_rebuttal_budget.py`

- [ ] **Step 1: Implement venue-aware format defaults**
- [ ] **Step 2: Implement experiment placeholder table generation**
- [ ] **Step 3: Make shared-global budgeting reviewer-count sensitive**
- [ ] **Step 4: Re-run formatter and budget tests**

### Task 3: Reflect the formatter rules in skill docs and README

**Files:**
- Modify: `D:\rebuttalskill\.worktrees\venue-aware-formatter\skills\super-rebuttal\references\venue-policies.md`
- Modify: `D:\rebuttalskill\.worktrees\venue-aware-formatter\skills\super-rebuttal\references\human-rebuttal-style.md`
- Modify: `D:\rebuttalskill\.worktrees\venue-aware-formatter\commands\rebuttal.md`
- Modify: `D:\rebuttalskill\.worktrees\venue-aware-formatter\skills\super-rebuttal\SKILL.md`
- Modify: `D:\rebuttalskill\.worktrees\venue-aware-formatter\README.md`
- Modify: `D:\rebuttalskill\.worktrees\venue-aware-formatter\README.zh-CN.md`

- [ ] **Step 1: Document venue defaults and `W1 / W2 / W3` output rules**
- [ ] **Step 2: Document experiment placeholder tables with `XX` values**
- [ ] **Step 3: Re-run README and metadata tests**

### Task 4: Verify and finish

- [ ] **Step 1: Run the full test suite**
- [ ] **Step 2: Run `py_compile` on new Python files**
- [ ] **Step 3: Finish the development branch**
