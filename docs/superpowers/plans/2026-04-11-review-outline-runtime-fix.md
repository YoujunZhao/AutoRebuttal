# SuperRebuttal Review Outline Runtime Fix Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make real OpenReview-style review PDFs usable in the rebuttal workflow and ensure the default reviewer outline preserves `W#`, `Q#`, and `M#` structure.

**Architecture:** Add an image fallback path to review-PDF ingestion, then harden reviewer-outline parsing for real OpenReview section headers. Update runtime entrypoints so image-based review PDFs and `W/Q/M` outline generation are part of the default workflow instead of optional guidance.

**Tech Stack:** Python 3 standard library, PyMuPDF (`fitz`) when available in the local environment, Markdown, unittest

---

### Task 1: Lock the broken behavior with failing tests

**Files:**
- Create: `D:\rebuttalskill\.worktrees\review-outline-runtime-fix\tests\test_render_review_pdf_pages.py`
- Modify: `D:\rebuttalskill\.worktrees\review-outline-runtime-fix\tests\test_input_bundle.py`
- Modify: `D:\rebuttalskill\.worktrees\review-outline-runtime-fix\tests\test_reviewer_outline.py`
- Modify: `D:\rebuttalskill\.worktrees\review-outline-runtime-fix\tests\test_plugin_surface.py`
- Modify: `D:\rebuttalskill\.worktrees\review-outline-runtime-fix\tests\test_skill_metadata.py`

- [ ] **Step 1: Add a failing test that requires review PDFs without text layers to fall back to rendered page images**
- [ ] **Step 2: Add a failing parser test that uses OpenReview-style headers such as `Strengths And Weaknesses`, `Main Weaknesses`, and `Key Questions For Authors`**
- [ ] **Step 3: Add failing surface tests that require image-fallback and reviewer-outline wording in the command and skill docs**
- [ ] **Step 4: Run focused tests and confirm they fail for the expected reasons**

### Task 2: Implement review-PDF image fallback

**Files:**
- Create: `D:\rebuttalskill\.worktrees\review-outline-runtime-fix\skills\super-rebuttal\scripts\render_review_pdf_pages.py`
- Modify: `D:\rebuttalskill\.worktrees\review-outline-runtime-fix\skills\super-rebuttal\scripts\build_input_bundle.py`

- [ ] **Step 1: Implement page rendering for review PDFs**
- [ ] **Step 2: Update bundle construction so review PDFs that fail text extraction continue with `page_images` and `extraction_mode=image_fallback`**
- [ ] **Step 3: Re-run focused ingestion tests**

### Task 3: Implement real-review outline parsing

**Files:**
- Modify: `D:\rebuttalskill\.worktrees\review-outline-runtime-fix\skills\super-rebuttal\scripts\build_reviewer_outline.py`

- [ ] **Step 1: Expand section-header recognition for OpenReview review variants**
- [ ] **Step 2: Stop strengths from leaking into `W#`**
- [ ] **Step 3: Preserve question and minor numbering when those sections exist**
- [ ] **Step 4: Re-run focused outline tests**

### Task 4: Update runtime guidance and verify

**Files:**
- Modify: `D:\rebuttalskill\.worktrees\review-outline-runtime-fix\commands\rebuttal.md`
- Modify: `D:\rebuttalskill\.worktrees\review-outline-runtime-fix\skills\super-rebuttal\SKILL.md`
- Modify: `D:\rebuttalskill\.worktrees\review-outline-runtime-fix\README.md`
- Modify: `D:\rebuttalskill\.worktrees\review-outline-runtime-fix\README.zh-CN.md`

- [ ] **Step 1: Update runtime docs so image-based review PDFs continue via rendered pages instead of asking for pasted review text**
- [ ] **Step 2: Make `build reviewer outline` an explicit required step before drafting**
- [ ] **Step 3: Re-run surface tests**

### Task 5: Verify, review, and finish

- [ ] **Step 1: Run the relevant focused tests**
- [ ] **Step 2: Run the full test suite**
- [ ] **Step 3: Request code review**
- [ ] **Step 4: Finish the development branch**
