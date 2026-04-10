# SuperRebuttal Human-Like Rebuttal Design

**Date:** 2026-04-11
**Project:** SuperRebuttal
**Status:** Approved by delegated default

## Goal

Make SuperRebuttal produce rebuttals that feel materially closer to strong human-written ICLR/ICML rebuttals, not just polite generic LLM answers.

## Problem

The current system can ingest paper PDFs and review PDFs and can manage lifecycle commands, but the generated rebuttal still feels unlike a strong human rebuttal in three ways:

1. it answers concerns too locally instead of building a global strategy
2. it lacks reviewer-specific stance and persuasion modeling
3. it tends to sound like a safe template instead of a targeted rebuttal letter

## External Reference Signals

### Public ICLR rebuttal style

The strongest public patterns from ICLR-oriented rebuttal advice and retrospective studies are:

- first build an issue inventory, not prose
- answer shared concerns consistently across reviewers
- use direct answers plus grounded evidence
- maintain a calm but confident tone
- focus attention on swing reviewers and borderline concerns

### ARIS / Auto-claude-code-research-in-sleep

The most useful part of the ARIS rebuttal workflow is not the surface prompt, but the pipeline shape:

- parse reviews
- atomize concerns
- build strategy
- draft
- run safety gates
- stress test
- finalize

This is the main structural inspiration for the redesign.

## Recommended Approach

Upgrade SuperRebuttal from a single-stage drafting workflow into a structured rebuttal pipeline with explicit intermediate artifacts.

### New internal artifacts

1. **Review packet**
   - raw review text
   - normalized concern units
2. **Reviewer card**
   - reviewer stance
   - likely persuasion target
   - tone sensitivity
   - confidence / uncertainty
3. **Global strategy memo**
   - top 2-4 themes
   - consistency constraints across reviewers
   - what to emphasize
   - what to concede narrowly
4. **Human-style rebuttal draft**
   - short global opener
   - reviewer-by-reviewer sections
   - optional closing for AC / meta-reviewer framing
5. **Stress-test notes**
   - unsupported claims
   - overpromises
   - weakly answered issues

## Reviewer Modeling

Each reviewer should be analyzed on at least these axes:

- sentiment: positive / mixed / negative
- movability: fixed / swing / supportive
- concern mix: novelty / evidence / writing / reproducibility / scope / theory
- tone target: reassure / clarify / de-escalate / sharpen distinction

This is not for show. It should directly influence the draft:

- swing reviewers get the clearest direct answers first
- negative reviewers get narrower, more evidence-bound claims
- supportive reviewers still get reinforcement, but with lower budget

## Human-Style Output Constraints

The new draft style should prefer:

- very short opener
- explicit issue framing
- one strong point per paragraph
- fewer generic gratitude phrases
- fewer broad promises
- more reviewer-specific prioritization

It should avoid:

- same-tone repetition across all reviewers
- over-apologetic language
- generic "we thank the reviewer" loops with low information density
- burying the real answer after too much framing

## Runtime Behavior Change

When the system receives:

- one paper PDF
- one or more review PDFs

it should not stop at "reviews extracted." It should continue through:

1. review packet creation
2. reviewer card generation
3. strategy memo generation
4. draft generation

unless extraction fails or a critical constraint is missing.

## Proposed File Changes

```text
skills/super-rebuttal/
  references/
    human-rebuttal-style.md
    reviewer-model.md
  scripts/
    build_reviewer_cards.py
commands/
  rebuttal.md
tests/
  test_reviewer_cards.py
  test_plugin_surface.py
  test_skill_metadata.py
```

## Testing Strategy

We cannot fully unit test natural-language quality, but we can test:

- the workflow requires reviewer cards and a strategy memo
- reviewer analysis artifacts are generated from extracted review inputs
- command and skill entrypoints describe the human-style pipeline explicitly
- docs include the human-style distinction from generic rebuttal generation

## Success Criteria

- generated workflow explicitly models reviewer stance and attitude
- shared issues are surfaced before reviewer-by-reviewer drafting
- runtime no longer stops after raw extraction when enough inputs are present
- docs and command entrypoints reflect the stronger workflow
