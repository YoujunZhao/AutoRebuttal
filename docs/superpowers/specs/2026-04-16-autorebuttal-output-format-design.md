# AutoRebuttal Output Format Design

## Goal

Add a small user-facing `output` parameter to AutoRebuttal so callers can choose either plain `text` or Markdown `md` output. The default remains `text`.

## Scope

This change applies to both command surfaces:

- `/rebuttal`
- `/rebuttal_revise`

It also applies to the internal bundle builders so downstream steps can read one normalized output-format field instead of re-parsing user intent from prose.

## Recommended Approach

Use a normalized `output_format` field in the draft and revision bundles.

Why this approach:

- it keeps the command surface simple: `output=text|md`
- it preserves backward compatibility because callers who omit the parameter still get `text`
- it gives downstream workflow code one stable field to inspect

Rejected alternative:

- infer Markdown output only from the user’s free-form prompt
  - rejected because it is brittle and hard to test

## Behavior

- accepted values: `text`, `md`
- default: `text`
- aliases are intentionally out of scope for now
- invalid values should fail clearly with a `ValueError`

## Output Expectations

- `text` means prose-first plain text output with no Markdown-only formatting requirement
- `md` means Markdown-friendly output is allowed and should be preserved through the workflow contract

This does not change the existing artifact contract names such as `rebuttal_text` or `revised_latex_paper`; it only controls presentation format.

## Files To Touch

- `skills/auto-rebuttal/scripts/build_draft_bundle.py`
- `skills/auto-rebuttal/scripts/build_revision_bundle.py`
- `skills/auto-rebuttal/scripts/response_modes.py`
- `commands/rebuttal.md`
- `commands/rebuttal_revise.md`
- `skills/auto-rebuttal/SKILL.md`
- `skills/auto-rebuttal/references/input-contract.md`
- `README.md`
- `README.zh-CN.md`
- tests covering bundle behavior, response mode helpers, plugin/README truth surfaces

## Risks

- doc drift if the parameter is implemented in code but not reflected in command examples
- hidden assumptions if downstream code reads `output` in one place and `output_format` in another

## Success Criteria

- callers can pass `output=md` for both draft and revise flows
- omitting `output` still yields `text`
- invalid output values fail clearly
- README and command docs show the parameter consistently
