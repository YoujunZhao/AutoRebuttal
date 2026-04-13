# AutoRebuttal LaTeX Input and README Upgrade Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add LaTeX paper input support, define a rebuttal-plus-revised-LaTeX output contract, and upgrade the README with a workflow diagram and parameter table.

**Architecture:** Add a dedicated paper-artifact detector, extend the draft and revision bundle builders to accept generic paper input, introduce a small LaTeX output-package helper, and update the command/skill/docs surfaces to reflect the new workflow clearly.

**Tech Stack:** Python 3 standard library, Markdown, Mermaid, unittest

---

### Task 1: Add failing tests for LaTeX paper input and README structure

**Files:**
- Modify: `D:\rebuttalskill\.worktrees\autorebuttal-latex-readme\tests\test_draft_bundle.py`
- Modify: `D:\rebuttalskill\.worktrees\autorebuttal-latex-readme\tests\test_revision_bundle.py`
- Create: `D:\rebuttalskill\.worktrees\autorebuttal-latex-readme\tests\test_latex_output_package.py`
- Modify: `D:\rebuttalskill\.worktrees\autorebuttal-latex-readme\tests\test_install_wrappers.py`

- [ ] **Step 1: Add a failing test for single-file LaTeX paper input**
- [ ] **Step 2: Add a failing test for LaTeX project-directory input**
- [ ] **Step 3: Add a failing test for the LaTeX dual output package**
- [ ] **Step 4: Add failing README tests for a Mermaid flowchart and parameter table**
- [ ] **Step 5: Run focused tests and confirm failure**

### Task 2: Implement paper detection and LaTeX output packaging

**Files:**
- Create: `D:\rebuttalskill\.worktrees\autorebuttal-latex-readme\skills\auto-rebuttal\scripts\detect_paper_artifact.py`
- Create: `D:\rebuttalskill\.worktrees\autorebuttal-latex-readme\skills\auto-rebuttal\scripts\build_latex_output_package.py`
- Modify: `D:\rebuttalskill\.worktrees\autorebuttal-latex-readme\skills\auto-rebuttal\scripts\build_draft_bundle.py`
- Modify: `D:\rebuttalskill\.worktrees\autorebuttal-latex-readme\skills\auto-rebuttal\scripts\build_revision_bundle.py`

- [ ] **Step 1: Implement LaTeX paper detection for `.tex` files and directories**
- [ ] **Step 2: Extend bundle builders to accept generic `paper_input`**
- [ ] **Step 3: Emit expected LaTeX outputs when the paper source type is `latex`**
- [ ] **Step 4: Re-run focused tests**

### Task 3: Update commands, skill docs, and README

**Files:**
- Modify: `D:\rebuttalskill\.worktrees\autorebuttal-latex-readme\commands\rebuttal.md`
- Modify: `D:\rebuttalskill\.worktrees\autorebuttal-latex-readme\commands\rebuttal_revise.md`
- Modify: `D:\rebuttalskill\.worktrees\autorebuttal-latex-readme\skills\auto-rebuttal\SKILL.md`
- Modify: `D:\rebuttalskill\.worktrees\autorebuttal-latex-readme\skills\auto-rebuttal\references\input-contract.md`
- Modify: `D:\rebuttalskill\.worktrees\autorebuttal-latex-readme\README.md`
- Modify: `D:\rebuttalskill\.worktrees\autorebuttal-latex-readme\README.zh-CN.md`

- [ ] **Step 1: Document LaTeX paper input for both commands**
- [ ] **Step 2: Document the rebuttal + revised LaTeX output contract**
- [ ] **Step 3: Add the Mermaid workflow diagram**
- [ ] **Step 4: Add the parameter table**
- [ ] **Step 5: Re-run README and surface tests**

### Task 4: Verify and finish

- [ ] **Step 1: Run the full test suite**
- [ ] **Step 2: Run py_compile on the new scripts**
- [ ] **Step 3: Request code review**
- [ ] **Step 4: Finish the development branch**
