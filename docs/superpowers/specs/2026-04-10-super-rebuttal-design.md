# SuperRebuttal Design

**Date:** 2026-04-10
**Project:** SuperRebuttal
**Status:** Approved by default via user delegation

## Goal

Build a reusable rebuttal-writing skill package named `super-rebuttal` that can be installed into Codex, Claude Code, and OpenClaw. The skill should accept a paper PDF or extracted manuscript text, reviewer comments, venue or journal constraints, and optional per-review length requirements, then produce high-quality rebuttal text without fabricating experiments or numbers.

## Problem Statement

Existing rebuttal workflows are fragmented:

- Venue rules differ across ICLR, NeurIPS, ICML, ARR, and journals.
- Users often need to manually convert reviews into a coherent response plan.
- One-shot prompts tend to hallucinate experiments, overclaim, or miss reviewer concerns.
- Cross-tool reuse is poor; a prompt written for one coding agent is not packaged for others.

SuperRebuttal should solve this by packaging a repeatable, venue-aware, evidence-first rebuttal workflow into an installable skill.

## Success Criteria

- Installable in Codex, Claude Code, and OpenClaw with documented steps.
- Produces rebuttals from paper + reviews + constraints with no fabricated numeric results.
- Supports reviewer-by-reviewer drafting and global shared-issue handling.
- Uses explicit placeholders like `XX`, `[TO-BE-RUN]`, or `[TABLE-PLACEHOLDER]` for missing experiment results.
- Contains built-in venue policy references and a generic fallback when the venue is unknown.
- Includes validation helpers for structure and character budgeting.
- Ships with a detailed bilingual README.

## Non-Goals

- Running experiments automatically.
- Logging into conference systems automatically.
- Scraping private reviews from external services.
- Guaranteeing score improvement or acceptance.
- Providing legal or publication-policy advice beyond cited public references.

## User Inputs

The skill should support these input combinations:

1. Paper PDF + raw reviews + venue name.
2. Paper markdown/text + structured reviews + venue name.
3. Reviews only + user-provided manuscript summary.
4. Venue unknown + explicit user constraints such as "5000 characters per reviewer".

Optional user input:

- Desired tone.
- Response language.
- Per-review or global character/word budget.
- Reviewer IDs and scores.
- Author strategy notes, for example "do not promise new experiments" or "emphasize theory".

## Product Approach Options

### Option A: Prompt-only skill

Pros:

- Fastest to build.
- Minimal files and maintenance.

Cons:

- Weak on venue compliance.
- Hard to validate and reuse.
- Poor cross-tool packaging story.

### Option B: Structured workflow skill with references and scripts

Pros:

- Strong balance of reliability and simplicity.
- Fits the Agent Skills model used by Codex, Claude Code, and OpenClaw.
- Lets us separate core workflow, venue rules, examples, and validation helpers.

Cons:

- More files and testing than a prompt-only approach.

### Option C: Full autonomous rebuttal system with retrieval and external services

Pros:

- Highest potential capability ceiling.

Cons:

- Too large for v1.
- Violates current scope around experiments and simple installability.

## Recommended Approach

Use Option B.

SuperRebuttal will be a canonical shared skill folder with:

- One main `SKILL.md` that defines the workflow.
- Reference documents for venue policies, rebuttal tactics, and output formats.
- Lightweight helper scripts for install, packaging, and budget validation.
- Tool-specific installation adapters for Codex, Claude Code, and OpenClaw.

## Core Workflow

The skill should guide the agent through these stages:

1. Intake and normalize artifacts.
2. Infer or load venue constraints.
3. Extract paper contributions, claims, evidence, and limitations.
4. Convert reviews into atomic concerns.
5. Build reviewer personas and concern priorities.
6. Merge overlapping concerns across reviewers.
7. Choose a response strategy per concern:
   - clarify existing evidence
   - acknowledge limitation
   - promise revision text
   - propose future work
   - add placeholder experiment note
   - respectfully decline unreasonable request
8. Draft reviewer-specific responses.
9. Draft shared summary or meta-response when useful.
10. Run compliance checks:
   - no fabricated numbers
   - no unsupported claims
   - no prohibited links if venue disallows them
   - length budget respected
   - tone remains polite and specific

## Reviewer Persona Layer

The skill should use reviewer personas as a reasoning scaffold, not as output text. Initial personas:

- empirical skeptic
- theory skeptic
- clarity/style focused reviewer
- novelty/significance reviewer
- baseline/ablation reviewer
- reproducibility reviewer
- scope/limitation reviewer

The workflow should map each reviewer to one or more personas and then tailor the reply emphasis accordingly.

## Venue Policy Layer

The skill should include a curated venue policy reference file with dated notes and source links. v1 should cover at least:

- ICLR 2025
- ICLR 2026
- NeurIPS 2025
- ICML 2025
- ICML 2026
- ARR / ACL / EMNLP guidance
- Generic OpenReview rebuttal form defaults

Policy behavior:

- If a venue is known and covered, use that rule set.
- If a venue is known but uncaptured or year-specific guidance is missing, use the closest known template and tell the agent to verify the current official rules if internet access exists.
- If the user gives explicit constraints, those override built-in defaults.

## Hallucination Guardrails

The skill must explicitly forbid:

- inventing experiments
- inventing numerical gains
- inventing statistical significance
- inventing extra baselines
- inventing citations not present in the paper or user-provided references

Instead, it should require placeholders such as:

- `XX`
- `[RESULT-TO-FILL]`
- `[TABLE-PLACEHOLDER]`
- `[IF-RUN-LATER]`

## Output Modes

The skill should support multiple output shapes:

1. Reviewer-by-reviewer rebuttal.
2. Shared concerns matrix.
3. Final polished rebuttal only.
4. Strategy-first output before full prose.

Default output should include:

- constraint summary
- issue map
- final rebuttal draft
- optional revision promises section

## Cross-Tool Packaging

### Canonical source

Keep one canonical skill directory in the repository, then install or mirror it into tool-specific locations.

### Codex

- Support repo-local or user-local installation.
- Include `agents/openai.yaml` for UI metadata.

### Claude Code

- Support `.claude/skills/super-rebuttal/`.
- Also provide a compatibility wrapper command if users prefer direct slash-command invocation.

### OpenClaw

- Support workspace `skills/` and shared `~/.openclaw/skills/`.
- Keep frontmatter compatible with Agent Skills and OpenClaw metadata expectations.

## Proposed Repository Layout

```text
SuperRebuttal/
  README.md
  LICENSE
  .gitignore
  docs/
    superpowers/
      specs/
      plans/
  skill/
    super-rebuttal/
      SKILL.md
      agents/
        openai.yaml
      references/
        venue-policies.md
        rebuttal-playbook.md
        input-contract.md
        source-notes.md
      examples/
        sample-input.md
        sample-output.md
      scripts/
        install_skill.py
        validate_budget.py
        package_skill.py
  install/
    install-codex.ps1
    install-codex.sh
    install-claude-code.ps1
    install-claude-code.sh
    install-openclaw.ps1
    install-openclaw.sh
  tests/
    test_install_skill.py
    test_validate_budget.py
    test_skill_metadata.py
```

## Testing Strategy

We should test:

- skill metadata validity
- install script copy behavior
- character budgeting logic
- packaging output structure
- required reference files exist
- sample fixtures produce expected budget calculations

Manual verification should also cover:

- Codex install path
- Claude Code install path
- OpenClaw install path
- README bilingual navigation

## Documentation Strategy

The README should be bilingual in one file with anchor-based language toggles:

- English section
- Chinese section

It should cover:

- what the skill does
- design principles
- install instructions for each tool
- invocation examples
- input formats
- output modes
- venue support
- known limitations
- citations and research basis

## Risks

### Policy drift

Venue rules change yearly. Mitigation:

- include dated source links
- include explicit note that user-provided constraints override defaults
- document the last verified date

### Tool compatibility drift

Codex, Claude Code, and OpenClaw may evolve their skill loaders. Mitigation:

- keep one canonical skill
- keep installer logic simple file-copy based
- validate metadata in tests

### Overly aggressive claims

LLMs can overpromise. Mitigation:

- strong non-fabrication section in `SKILL.md`
- sample outputs showing placeholder usage
- validation checklist

## Open Assumptions

- The user wants a public repository structure but a private GitHub repository.
- The first release should prefer portability and clarity over heavy automation.
- Python 3 is available for helper scripts.
- PDF understanding will primarily rely on the host agent's native file capabilities, not a bundled PDF parser dependency.

## Implementation Decision

Proceed with:

- a single canonical skill package
- bilingual root README
- Python-based helper tooling with standard library only
- venue rules embedded as references
- no external API dependency
- no experiment execution layer in v1
