# AutoRebuttal OCR PDF Support Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add OCR-backed PDF reading for image-based review PDFs and rebuttal PDFs using the OCR libraries already available on this machine.

**Architecture:** Keep native PDF text extraction as the first path, then add OCR on rendered page images through a new helper. Wire that helper into `detect_input_artifact.py` so both draft and revise bundle builders gain OCR support without duplicating logic.

**Tech Stack:** Python 3, `fitz`, `PIL`, `rapidocr_onnxruntime`, unittest

---

### Task 1: Add failing OCR tests

**Files:**
- Modify: `D:\rebuttalskill\.worktrees\autorebuttal-ocr\tests\test_draft_bundle.py`
- Modify: `D:\rebuttalskill\.worktrees\autorebuttal-ocr\tests\test_revision_bundle.py`
- Create: `D:\rebuttalskill\.worktrees\autorebuttal-ocr\tests\test_ocr_rendered_pages.py`

- [ ] **Step 1: Add a failing test for OCR on an image-based review PDF**
- [ ] **Step 2: Add a failing test for OCR on an image-based rebuttal PDF in revise mode**
- [ ] **Step 3: Run focused OCR tests and confirm failure**

### Task 2: Implement OCR helper and integrate it

**Files:**
- Create: `D:\rebuttalskill\.worktrees\autorebuttal-ocr\skills\auto-rebuttal\scripts\ocr_rendered_pages.py`
- Modify: `D:\rebuttalskill\.worktrees\autorebuttal-ocr\skills\auto-rebuttal\scripts\detect_input_artifact.py`

- [ ] **Step 1: Implement OCR for rendered page images**
- [ ] **Step 2: Set `extraction_mode = ocr` when OCR succeeds**
- [ ] **Step 3: Preserve honest fallback when OCR fails**
- [ ] **Step 4: Re-run focused tests**

### Task 3: Update docs and invocation guidance

**Files:**
- Modify: `D:\rebuttalskill\.worktrees\autorebuttal-ocr\commands\rebuttal.md`
- Modify: `D:\rebuttalskill\.worktrees\autorebuttal-ocr\commands\rebuttal_revise.md`
- Modify: `D:\rebuttalskill\.worktrees\autorebuttal-ocr\skills\auto-rebuttal\SKILL.md`
- Modify: `D:\rebuttalskill\.worktrees\autorebuttal-ocr\skills\auto-rebuttal\references\input-contract.md`
- Modify: `D:\rebuttalskill\.worktrees\autorebuttal-ocr\README.md`
- Modify: `D:\rebuttalskill\.worktrees\autorebuttal-ocr\README.zh-CN.md`

- [ ] **Step 1: Document that `/rebuttal` accepts paper PDF plus review PDF or review text**
- [ ] **Step 2: Document that `/rebuttal_revise` accepts rebuttal PDF or rebuttal text, with optional paper PDF**
- [ ] **Step 3: Document OCR behavior and remaining fallback limits**

### Task 4: Verify and finish

- [ ] **Step 1: Run full test suite**
- [ ] **Step 2: Run py_compile for OCR helpers**
- [ ] **Step 3: Request code review**
- [ ] **Step 4: Finish the development branch**
