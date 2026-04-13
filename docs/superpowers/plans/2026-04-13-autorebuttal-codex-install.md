# AutoRebuttal Codex Install Simplification Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make Codex installation docs match the lightweight Superpowers-style install flow while preserving the existing manager CLI as an optional path.

**Architecture:** Rewrite `.codex/INSTALL.md` and README install sections around native skill discovery (clone + junction/symlink), then update tests to enforce the new preferred path and quick-install copy.

**Tech Stack:** Markdown, unittest

---

### Task 1: Add failing install-doc tests

**Files:**
- Modify: `D:\rebuttalskill\.worktrees\autorebuttal-codex-install\tests\test_install_wrappers.py`

- [ ] **Step 1: Add a failing assertion for a Quick Install line that points to `.codex/INSTALL.md`**
- [ ] **Step 2: Add failing assertions for clone + junction/symlink instructions**
- [ ] **Step 3: Add failing assertions that manager CLI is documented as optional, not primary**
- [ ] **Step 4: Run the focused test and confirm failure**

### Task 2: Rewrite Codex installation docs

**Files:**
- Modify: `D:\rebuttalskill\.worktrees\autorebuttal-codex-install\.codex\INSTALL.md`
- Modify: `D:\rebuttalskill\.worktrees\autorebuttal-codex-install\README.md`
- Modify: `D:\rebuttalskill\.worktrees\autorebuttal-codex-install\README.zh-CN.md`

- [ ] **Step 1: Rewrite `.codex/INSTALL.md` around clone + junction/symlink**
- [ ] **Step 2: Add Quick Install copy to README**
- [ ] **Step 3: Keep manager CLI as an alternative path**
- [ ] **Step 4: Re-run the focused tests**

### Task 3: Verify and finish

- [ ] **Step 1: Run the relevant README/install tests**
- [ ] **Step 2: Request code review**
- [ ] **Step 3: Finish the development branch**
