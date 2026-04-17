# Input Contract

## Preferred Inputs

Best case:

- paper PDF, LaTeX file, LaTeX directory, or extracted manuscript text
- zero or more review PDFs, or extracted reviewer text
- an existing rebuttal PDF or rebuttal text when using revise mode
- all reviewer comments
- venue and year
- global or per-review character / word limit
- desired output format: `text` or `md`
- desired supplementary-experiment behavior: `autoexperiment=true|false`
- desired project code path: `code=<path>` or `code=false`
- author notes on what can and cannot be promised

When artifact files are provided, treat them as first-class source artifacts:

- exactly one paper PDF may supply the manuscript context
- exactly one paper LaTeX file or one LaTeX project directory may supply the manuscript context
- review PDFs may be repeated and should preserve caller order
- revise mode may receive one rebuttal PDF instead of review inputs
- text extraction is best-effort and limited to text-based PDFs
- if a review PDF has no text layer but can be rendered, OCR the rendered pages first
- if a rebuttal PDF has no text layer but can be rendered, OCR the rendered pages first
- image-fallback reviews need image-derived text or a prebuilt reviewer outline before reviewer-card generation

Auto-detection rules:

- existing filesystem path ending in `.pdf` -> treat as PDF artifact
- existing filesystem path ending in `.tex` -> treat as LaTeX artifact
- existing directory containing `.tex` files -> treat as LaTeX project artifact
- existing filesystem path with any other suffix -> treat as text-file artifact
- non-path string -> treat as raw text

OCR rules:

- text-layer PDF -> `extraction_mode = text`
- image-based PDF with OCR success -> `extraction_mode = ocr`
- image-based review PDF with OCR failure -> `extraction_mode = image_fallback`
- image-based rebuttal PDF with OCR failure -> explicit error

LaTeX paper rules:

- if `paper_input` is a single `.tex` file, preserve that file as the LaTeX source artifact
- if `paper_input` is a directory, it must contain at least one `.tex` file
- prefer `main.tex`, `paper.tex`, `ms.tex`, or `manuscript.tex` as the LaTeX `entrypoint`; otherwise fall back to the first `.tex` file found
- preserve `latex_sources` and the combined paper `text`
- when the paper source type is `latex`, the expected outputs are `rebuttal_text` and `revised_latex_paper`
- this contract does not by itself prove TeX compilation or automatic multi-file patching

## Accepted Fallbacks

If the paper PDF is missing, use:

- abstract
- contribution summary
- method summary
- known limitations

If the venue is unknown, use:

1. explicit user constraints if provided
2. the closest bundled venue pattern if the user names a family such as "ICML-like"
3. a generic fallback draft plus a note that the exact official rule still needs verification

## Useful Optional Inputs

- reviewer IDs and scores
- meta-review or area-chair note
- author preference on tone
- author preference on response shape:
  - strategy first
  - reviewer-by-reviewer prose
  - journal response letter
- a prebuilt input bundle with:
  - `paper.path`
  - `paper.text`
  - optional `paper.entrypoint`
  - optional `paper.latex_sources`
  - optional `paper.expected_outputs`
  - `reviews[].path`
  - `reviews[].text`
  - `reviews[].page_images`
  - `reviews[].extraction_mode`
  - `source_files.paper_pdf`
  - `source_files.review_pdfs`
- a prebuilt revision bundle with:
  - `rebuttal.source_type`
  - `rebuttal.path`
  - `rebuttal.text`
  - optional `paper.path`
  - optional `paper.text`
  - optional `paper.entrypoint`
  - optional `paper.latex_sources`

When the paper source type is `latex`, the expected output contract becomes:

- `rebuttal_text`
- `revised_latex_paper`
- optional `entrypoint` in the final `latex-dual` package

Presentation format rules:

- `output=text` -> plain-text style output
- `output=md` -> Markdown-friendly output
- omit `output` -> default to `text`

Supplementary experiment rules:

- `autoexperiment=false` -> keep placeholders and do not auto-run experiments
- `autoexperiment=true` -> route reviewer experiment requests through `/experiment-bridge`
- `code=false` -> no project code path is available, so experiments remain blocked
- `code=<path>` -> treat the path as the project code root for supplementary evidence
- if no runnable experiment workspace exists, report blockers clearly and keep placeholders

## Default Output Modes

- `strategy-first`: return the issue map and response plan before prose
- `reviewer-by-reviewer`: return separate replies per reviewer
- `shared-letter`: return one integrated response letter
- `prose-only`: return the final text only

Default to `strategy-first` when the input is complex, the venue is unknown, or the budget is tight.

## Minimal Clarification Rule

Ask a clarifying question only when a critical constraint is missing and cannot be inferred safely. Prefer the smallest possible question, for example:

- "What is the per-review character limit?"
- "Should I avoid promising new experiments?"

If the user has already delegated product decisions, make a conservative assumption and state it.
