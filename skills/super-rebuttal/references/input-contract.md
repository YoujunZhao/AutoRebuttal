# Input Contract

## Preferred Inputs

Best case:

- paper PDF or extracted manuscript text
- all reviewer comments
- venue and year
- global or per-review character / word limit
- author notes on what can and cannot be promised

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
