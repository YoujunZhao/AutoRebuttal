# AutoRebuttal OCR PDF Support Design

**Date:** 2026-04-12
**Project:** AutoRebuttal
**Status:** Approved by delegated default

## Goal

Teach AutoRebuttal to actually read image-based PDFs instead of only preserving them as rendered page images.

This applies to:

- review PDFs in `/rebuttal`
- rebuttal PDFs in `/rebuttal_revise`

## Problem

The current project already renders image-based PDFs into page images, but it does not automatically OCR those images into usable text. That means:

- review PDFs can survive as `image_fallback`, but still need manual image inspection later
- rebuttal PDFs without a text layer fail outright in revise mode

For the user, that still feels like “the project cannot really read PDFs”.

## Recommended Approach

Use the OCR stack that is already installed locally:

- `fitz` for rendering pages
- `PIL` for image loading
- `rapidocr_onnxruntime` for OCR

### OCR behavior

1. Try native PDF text extraction first.
2. If that fails, render the first pages to PNG.
3. Run OCR on the rendered images.
4. If OCR yields usable text:
   - keep the extracted text
   - preserve `page_images`
   - mark the artifact as `extraction_mode = ocr`
5. If OCR also fails:
   - keep current honest fallback for reviews (`image_fallback`)
   - fail clearly for rebuttal PDFs in revise mode

### Scope

- No new dependency install is needed if the already-available OCR stack works.
- No fake success: if OCR does not return usable text, the artifact must remain clearly marked as not parsed.

## Proposed Files

```text
skills/auto-rebuttal/scripts/
  detect_input_artifact.py
  ocr_rendered_pages.py
tests/
  test_draft_bundle.py
  test_revision_bundle.py
README.md
README.zh-CN.md
commands/rebuttal.md
commands/rebuttal_revise.md
skills/auto-rebuttal/SKILL.md
skills/auto-rebuttal/references/input-contract.md
```

## Success Criteria

- image-based review PDFs can produce OCR text automatically
- image-based rebuttal PDFs can produce OCR text automatically when OCR succeeds
- review PDFs still fall back honestly if OCR fails
- revise mode no longer fails on every non-text rebuttal PDF
- docs tell the user the real invocation shape and the real OCR boundary
