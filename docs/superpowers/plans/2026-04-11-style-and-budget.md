# SuperRebuttal Style and Budget Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Encode stronger initial rebuttal style rules and explicit character-budget planning so SuperRebuttal writes more like a strong human rebuttal under venue limits.

**Architecture:** Keep the current reviewer-card and strategy-memo pipeline, then add a style-plan layer and a stronger budget allocator layer. Document both in the skill references so the runtime flow can use them consistently.

**Tech Stack:** Markdown, Python 3 standard library, git

---

### Task 1: Lock style-plan and budget expectations with failing tests

**Files:**
- Create: `D:\rebuttalskill\.worktrees\rebuttal-quality-humanize\tests\test_style_plan.py`
- Modify: `D:\rebuttalskill\.worktrees\rebuttal-quality-humanize\tests\test_character_budget.py`
- Modify: `D:\rebuttalskill\.worktrees\rebuttal-quality-humanize\tests\test_install_wrappers.py`

- [ ] **Step 1: Add a failing style-plan test**
- [ ] **Step 2: Strengthen the character-budget test to require opener/body/closing allocation**
- [ ] **Step 3: Require docs to mention initial rebuttal style and budget planning**
- [ ] **Step 4: Run the focused tests and confirm failure**
- [ ] **Step 5: Commit the red phase**

### Task 2: Implement style-plan and stronger budget logic

**Files:**
- Create: `D:\rebuttalskill\.worktrees\rebuttal-quality-humanize\skills\super-rebuttal\scripts\build_style_plan.py`
- Create: `D:\rebuttalskill\.worktrees\rebuttal-quality-humanize\skills\super-rebuttal\references\initial-rebuttal-style.md`
- Modify: `D:\rebuttalskill\.worktrees\rebuttal-quality-humanize\skills\super-rebuttal\scripts\allocate_rebuttal_budget.py`

- [ ] **Step 1: Implement a style-plan builder for initial rebuttal rounds**
- [ ] **Step 2: Strengthen character budget allocation**
- [ ] **Step 3: Re-run focused tests**
- [ ] **Step 4: Commit the style-and-budget layer**

### Task 3: Reflect the new style and budget rules in docs

**Files:**
- Modify: `D:\rebuttalskill\.worktrees\rebuttal-quality-humanize\README.md`
- Modify: `D:\rebuttalskill\.worktrees\rebuttal-quality-humanize\README.zh-CN.md`
- Modify: `D:\rebuttalskill\.worktrees\rebuttal-quality-humanize\skills\super-rebuttal\SKILL.md`
- Modify: `D:\rebuttalskill\.worktrees\rebuttal-quality-humanize\skills\super-rebuttal\references\human-rebuttal-style.md`

- [ ] **Step 1: Document how the initial rebuttal round should be written**
- [ ] **Step 2: Document how user-supplied character limits are planned before drafting**
- [ ] **Step 3: Re-run README and metadata tests**
- [ ] **Step 4: Commit the doc alignment**

### Task 4: Verify and finish

- [ ] **Step 1: Run the full test suite**
- [ ] **Step 2: Run `py_compile` on new Python files**
- [ ] **Step 3: Finish the development branch**
