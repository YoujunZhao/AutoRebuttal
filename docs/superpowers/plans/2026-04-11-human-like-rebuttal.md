# SuperRebuttal Human-Like Rebuttal Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade SuperRebuttal from a generic rebuttal drafter into a more human-like rebuttal workflow with reviewer stance analysis, shared-issue strategy, and stronger runtime continuation after review-PDF ingestion.

**Architecture:** Keep the existing PDF ingestion and mode selection, then add a structured analysis layer on top: reviewer cards, global strategy memo, and explicit human-style drafting guidance. Make the command and skill entrypoints require those intermediate artifacts so the workflow does not stop at raw extraction.

**Tech Stack:** Markdown, Python 3 standard library, JSON, git

---

### Task 1: Add failing tests for reviewer-card generation and human-style workflow requirements

**Files:**
- Create: `D:\rebuttalskill\.worktrees\rebuttal-quality-humanize\tests\test_reviewer_cards.py`
- Modify: `D:\rebuttalskill\.worktrees\rebuttal-quality-humanize\tests\test_plugin_surface.py`
- Modify: `D:\rebuttalskill\.worktrees\rebuttal-quality-humanize\tests\test_skill_metadata.py`
- Modify: `D:\rebuttalskill\.worktrees\rebuttal-quality-humanize\tests\test_install_wrappers.py`

- [ ] **Step 1: Write the failing reviewer-card script test**
- [ ] **Step 2: Extend command-surface tests so `commands/rebuttal.md` must mention reviewer cards, strategy memo, and continuing after review-PDF extraction**
- [ ] **Step 3: Extend skill-metadata tests so `SKILL.md` must mention reviewer stance, reviewer cards, strategy memo, and not stopping after extraction**
- [ ] **Step 4: Extend README tests so the README must mention reviewer attitude / stance analysis and shared-issue strategy**
- [ ] **Step 5: Run the focused tests and confirm failure**
- [ ] **Step 6: Commit the red phase**

### Task 2: Implement reviewer-card generation and reference material

**Files:**
- Create: `D:\rebuttalskill\.worktrees\rebuttal-quality-humanize\skills\super-rebuttal\scripts\build_reviewer_cards.py`
- Create: `D:\rebuttalskill\.worktrees\rebuttal-quality-humanize\skills\super-rebuttal\references\reviewer-model.md`
- Create: `D:\rebuttalskill\.worktrees\rebuttal-quality-humanize\skills\super-rebuttal\references\human-rebuttal-style.md`
- Modify: `D:\rebuttalskill\.worktrees\rebuttal-quality-humanize\tests\test_reviewer_cards.py`

- [ ] **Step 1: Implement a minimal reviewer-card builder over extracted review text**
- [ ] **Step 2: Document reviewer stance axes and human-style rebuttal rules in new reference files**
- [ ] **Step 3: Re-run reviewer-card tests and confirm pass**
- [ ] **Step 4: Commit the reviewer-card layer**

### Task 3: Upgrade runtime entrypoints and skill instructions

**Files:**
- Modify: `D:\rebuttalskill\.worktrees\rebuttal-quality-humanize\commands\rebuttal.md`
- Modify: `D:\rebuttalskill\.worktrees\rebuttal-quality-humanize\skills\super-rebuttal\SKILL.md`
- Modify: `D:\rebuttalskill\.worktrees\rebuttal-quality-humanize\skills\super-rebuttal\references\rebuttal-playbook.md`
- Modify: `D:\rebuttalskill\.worktrees\rebuttal-quality-humanize\skills\super-rebuttal\references\input-contract.md`

- [ ] **Step 1: Make the command entrypoint require reviewer-card generation and strategy memo creation**
- [ ] **Step 2: Make the skill require reviewer stance analysis, shared-issue memo, and human-style draft rules**
- [ ] **Step 3: Update playbook and input contract to reflect runtime continuation after PDF extraction**
- [ ] **Step 4: Re-run plugin-surface and skill-metadata tests**
- [ ] **Step 5: Commit the runtime workflow upgrade**

### Task 4: Rewrite product docs around human-like rebuttal quality

**Files:**
- Modify: `D:\rebuttalskill\.worktrees\rebuttal-quality-humanize\README.md`
- Modify: `D:\rebuttalskill\.worktrees\rebuttal-quality-humanize\README.zh-CN.md`
- Modify: `D:\rebuttalskill\.worktrees\rebuttal-quality-humanize\tests\test_install_wrappers.py`

- [ ] **Step 1: Update README sections so they explain reviewer stance analysis, global strategy memo, and human-style drafting**
- [ ] **Step 2: Add explicit wording that review PDF ingestion continues into reviewer analysis rather than stopping**
- [ ] **Step 3: Re-run README tests**
- [ ] **Step 4: Commit the doc upgrade**

### Task 5: Verify, review, and finish the branch

**Files:**
- Modify: `D:\rebuttalskill\.worktrees\rebuttal-quality-humanize\docs\superpowers\plans\2026-04-11-human-like-rebuttal.md`

- [ ] **Step 1: Run the full test suite**
- [ ] **Step 2: Run `py_compile` on new Python files**
- [ ] **Step 3: Request code review**
- [ ] **Step 4: Apply any required fixes and re-run tests**
- [ ] **Step 5: Finish the development branch**
