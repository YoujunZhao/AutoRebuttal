# SuperRebuttal Review PDF and CLI Management Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add first-class review PDF support and a command-line lifecycle manager for Codex and Claude Code while keeping the project standard-library-first.

**Architecture:** Add a best-effort PDF extractor and a bundle builder under `skills/super-rebuttal/scripts/`, then add a repo-level management CLI under `scripts/`. Keep the CLI split by host: Codex performs real filesystem link management, while Claude follows the official plugin command model and emits exact commands when direct local execution is not appropriate.

**Tech Stack:** Python 3 standard library, Markdown, JSON, PowerShell, git

---

### Task 1: Lock the new support surface with failing tests

**Files:**
- Create: `D:\rebuttalskill\.worktrees\review-pdf-cli-management\tests\test_pdf_extract.py`
- Create: `D:\rebuttalskill\.worktrees\review-pdf-cli-management\tests\test_input_bundle.py`
- Create: `D:\rebuttalskill\.worktrees\review-pdf-cli-management\tests\test_manager_cli.py`
- Modify: `D:\rebuttalskill\.worktrees\review-pdf-cli-management\tests\test_install_wrappers.py`

- [ ] **Step 1: Write the failing PDF extractor test**
- [ ] **Step 2: Write the failing input-bundle test**
- [ ] **Step 3: Write the failing manager-CLI test**
- [ ] **Step 4: Update README tests to require review-PDF and CLI usage docs**
- [ ] **Step 5: Run the focused tests and confirm failure**
- [ ] **Step 6: Commit the red phase**

### Task 2: Implement best-effort PDF extraction and review bundle building

**Files:**
- Create: `D:\rebuttalskill\.worktrees\review-pdf-cli-management\skills\super-rebuttal\scripts\extract_pdf_text.py`
- Create: `D:\rebuttalskill\.worktrees\review-pdf-cli-management\skills\super-rebuttal\scripts\build_input_bundle.py`
- Modify: `D:\rebuttalskill\.worktrees\review-pdf-cli-management\skills\super-rebuttal\references\input-contract.md`
- Modify: `D:\rebuttalskill\.worktrees\review-pdf-cli-management\skills\super-rebuttal\SKILL.md`

- [ ] **Step 1: Implement the minimal extractor to satisfy the new tests**
- [ ] **Step 2: Implement the bundle builder with paper PDF plus review PDF inputs**
- [ ] **Step 3: Update the input contract and skill instructions**
- [ ] **Step 4: Re-run PDF and bundle tests**
- [ ] **Step 5: Commit the extraction layer**

### Task 3: Implement the host lifecycle manager CLI

**Files:**
- Create: `D:\rebuttalskill\.worktrees\review-pdf-cli-management\scripts\superrebuttal_manager.py`
- Modify: `D:\rebuttalskill\.worktrees\review-pdf-cli-management\.codex\INSTALL.md`
- Modify: `D:\rebuttalskill\.worktrees\review-pdf-cli-management\README.md`
- Modify: `D:\rebuttalskill\.worktrees\review-pdf-cli-management\README.zh-CN.md`

- [ ] **Step 1: Implement Codex install / update / remove commands**
- [ ] **Step 2: Implement Claude install / update / remove command rendering**
- [ ] **Step 3: Update both READMEs with CLI examples**
- [ ] **Step 4: Re-run CLI and README tests**
- [ ] **Step 5: Commit the lifecycle manager**

### Task 4: Verify, review, and branch completion

**Files:**
- Modify: `D:\rebuttalskill\.worktrees\review-pdf-cli-management\docs\superpowers\plans\2026-04-10-review-pdf-and-cli-management.md`

- [ ] **Step 1: Run the full test suite**
- [ ] **Step 2: Run `py_compile` on new Python files**
- [ ] **Step 3: Request code review**
- [ ] **Step 4: Apply any required fixes and re-run tests**
- [ ] **Step 5: Finish the development branch**
